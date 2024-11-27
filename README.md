<h1 align="left">
Python3 script to check WildFly for Icinga2
</h1>

Initially the script was planned to be used only for the Argus application but allows you to check any object-name and attribute.
</br>

**ℹ️ Need installed openjdk**

**ℹ️ Need jboss-client.jar - update path to file in 14 line**

<h2 align="left">
⚙️ How to work 
</h2>  

**ℹ️ You can assign your own object names and attributes in the corresponding arguments.**

Warning and Critical arguments are optional

```bash
./check_wildfly_jm.py
  --url "service:jmx:remote+http://localhost:9990" \
  --username "admin" \
  --password "password" \
  --object-name "java.lang:type=Memory" \
  --attribute "HeapMemoryUsage" \
  --warning 100000000 \
  --critical 200000000
```

<h3 align="left">
⚙️ Icinga2 Add
</h3>  

- **commands.conf** 
```bash
object CheckCommand "check_wildfly_jm" {
  import "plugin-check-command"
  command = [ PluginDir + "/check_wildfly_jm.py" ]
  arguments = {
                "--url" = "$host.vars.wildfly_full_server_url$"
                "--username" = "$host.vars.wildfly_username$"
                "--password" = "$host.vars.wildfly_pass$"
                "--object-name" = "$service.vars.object_name$"
                "--attribute" = "$service.vars.attribute$"
                "--warning" = "$service.vars.warning$"
                "--critical" = "$service.vars.critical$"
                }
}
```

- **service.conf**

```bash
apply Service "Wildfly-HeapMemoryUsage" {
  display_name = "Wildfly HeapMemoryUsage"
  import "generic-service"
  check_command = "check_wildfly_jm"

  vars.object_name = "java.lang:type=Memory"
  vars.attribute = "HeapMemoryUsage"
  vars.warning = "1234567"
  vars.critical = "2345678"
  
  assign where host.vars.wildfly_enable == "true"
}
```

- **Add to host config**
```bash
object Host "servername" {
.....
vars.wildfly_enable = "true"
vars.wildfly_full_server_url = "service:jmx:remote+http://IP or Hostname:9990"
vars.wildfly_username = "username"
vars.wildfly_pass = "password"

.....
```
