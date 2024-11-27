#!/usr/bin/python3
"""
Need installed open-jdk of youre version of Java
Update with the actual path to your jboss-client.jar file in line 14
"""

import jpype
import jpype.imports
from jpype.types import *
import argparse
import sys

# Path to jboss-client.jar
JBOSS_CLIENT_JAR_PATH = "/usr/lib/nagios/plugins/lib/jboss-client.jar"

def get_jmx_attribute(jmx_service_url, username, password, object_name, attribute):
    # Connect to WildFly JMX and fetch the specified attribute value, handling nested attributes.
    try:
        # Import Java classes (must happen after JVM starts)
        from javax.management.remote import JMXServiceURL
        from javax.management.remote import JMXConnectorFactory
        from javax.management import ObjectName
        from java.util import HashMap

        # Establish JMX connection
        service_url = JMXServiceURL(jmx_service_url)

        # Convert credentials to Java String array
        credentials = JArray(JString)([username, password])

        # Set up the environment map
        environment = HashMap()
        environment.put("jmx.remote.credentials", credentials)

        # Connect to JMX server
        connector = JMXConnectorFactory.connect(service_url, environment)
        mbean_server_connection = connector.getMBeanServerConnection()

        # Query the MBean attribute (possibly a nested attribute)
        object_name = ObjectName(object_name)

        # Fetch the main attribute (which could be a composite)
        main_value = mbean_server_connection.getAttribute(object_name, attribute)

        # If the attribute is like HeapMemoryUsage, access the 'used' field
        if attribute == "HeapMemoryUsage":
            used_value = main_value.get("used")
            return used_value

        # If the attribute is NonHeapMemoryUsage, access the 'used' field
        if attribute == "NonHeapMemoryUsage":
            used_value = main_value.get("used")
            return used_value

        return main_value
    except Exception as e:
        print(f"Failed to fetch JMX attribute: {e}")
        return None
    finally:
        if connector is not None:
            try:
                connector.close()
            except Exception as e:
                print(f"Warning: failed to close JMX connector: {e}")

def evaluate_thresholds(value, warning, critical, attribute):
    # Evaluate the value against warning and critical thresholds.
    if value is None:
        print("[UNKNOWN] value is None")
        sys.exit(3)

    if critical is not None and value >= critical:
        print(f"[CRITICAL] {attribute}: {value} | {attribute}={value}")
        sys.exit(2)

    if warning is not None and value >= warning:
        print(f"[WARNING] {attribute}: {value} | {attribute}={value}")
        sys.exit(1)

    print(f"OK - {attribute}: {value} | {attribute}={value}")
    sys.exit(0)

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Fetch JMX attributes from WildFly and evaluate thresholds.")
    parser.add_argument("--url", required=True, help="JMX Service URL (e.g., service:jmx:remote+http://localhost:9990)")
    parser.add_argument("--username", required=True, help="Username for JMX connection")
    parser.add_argument("--password", required=True, help="Password for JMX connection")
    parser.add_argument("--object-name", required=True, help="JMX Object Name (e.g., java.lang:type=Memory)")
    parser.add_argument("--attribute", required=True, help="Attribute to fetch from the JMX Object (e.g., HeapMemoryUsage)")
    parser.add_argument("--warning", type=int, help="Optional warning threshold for the attribute value")
    parser.add_argument("--critical", type=int, help="Optional critical threshold for the attribute value")

    args = parser.parse_args()

    # Path to your JDK/JRE
    JVM_PATH = jpype.getDefaultJVMPath()

    # Start JVM in silent mode with minimal logging (no JBoss specific dependencies)
    if not jpype.isJVMStarted():
        jpype.startJVM(
            JVM_PATH,
            # Disable all logging for the JVM
            "-Djava.util.logging.ConsoleHandler.level=OFF",  # Disable all console logging
            "-Djava.util.logging.FileHandler.level=OFF",     # Disable file-based logging
            "-Djava.util.logging.ConsoleHandler.formatter=java.util.logging.SimpleFormatter",  # Simple format for logging
            "-Djava.util.logging.config.class=java.util.logging.ConsoleHandler",  # Use a simple console handler
            "-Djava.util.logging.manager=java.util.logging.LogManager",  # Use default Java logging manager
            f"-Djava.class.path={JBOSS_CLIENT_JAR_PATH}",  # Use the variable defined at the top
        )

    # Fetch the JMX attribute
    attribute_value = get_jmx_attribute(
        jmx_service_url=args.url,
        username=args.username,
        password=args.password,
        object_name=args.object_name,
        attribute=args.attribute,
    )

    # Evaluate thresholds if provided
    evaluate_thresholds(attribute_value, args.warning, args.critical, args.attribute)

    # Shutdown JVM
    jpype.shutdownJVM()

if __name__ == "__main__":
    main()
