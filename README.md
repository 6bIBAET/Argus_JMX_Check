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
