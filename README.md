# Arduino Ciao DDP Meteor Connector

A DDP Connector to call remote functions of a [Meteor](http://www.meteor.com/) server from an Arduino sketch.

You can install **Ciao** in your Arduino following [this guide](http://labs.arduino.org/Ciao+setup) 

## Installation and configuration of the connector

1) Insert the host address and port of your Meteor server in the file [ddp/ddp.json.conf](ddp/ddp.json.conf)

2) Copy the DDP Connector folder named [ddp](ddp) to the Arduino Ciao **connectors** folder (/usr/lib/python2.7/ciao/connectors)

3) Copy the DDP Connector configuration file named [ddp.json.conf](ddp.json.conf) to the Arduino Ciao **conf** folder (/usr/lib/python2.7/ciao/conf)

## Examples

In all examples you need to include the Arduino Ciao Library and start it on the **setup()**:

```c++
#include <Ciao.h>

void setup() {
  Ciao.begin();
}

```

1) **Insert** a document into a collection named "Sensors"

```c++
void loop() {
  int val = analogRead(0);
  
  String id = "ArduinoSensor";
  String remoteFunction = "/Sensors/insert";
  String parameter = "[{\"_id\": \""+id+"\", \"value\": \""+val+"\"}]";

  Ciao.write("ddp", remoteFunction, parameter);

  delay(500);
}

```

2) **Update** a document with id "ArduinoSensor" into a collection named "Sensors"

```c++
void loop() {
  int val = analogRead(0);
  
  String id = "ArduinoSensor";
  String remoteFunction = "/Sensors/update";
  String parameter = "[{\"_id\": \""+id+"\"}, {\"$set\": {\"value\": \""+val+"\"}}]";

  Ciao.write("ddp", remoteFunction, parameter);

  delay(500);
}

```

3) **Update or Insert** a document with id "ArduinoSensor" into a collection named "Sensors"

```c++
void loop() {
  int val = analogRead(0);
  
  String id = "ArduinoSensor";
  String remoteFunction = "/Sensors/update";
  String parameter = "[{\"_id\": \""+id+"\"}, {\"$set\": {\"value\": \""+val+"\"}}, {\"upsert\": true}]";

  Ciao.write("ddp", remoteFunction, parameter);

  delay(500);
}

```

4) **Remove** a document into with id "ArduinoSensor" into a collection named "Sensors"

```c++
void loop() {
  int val = analogRead(0);
  
  String id = "ArduinoSensor";
  String remoteFunction = "/Sensors/remove";
  String parameter = "[{\"_id\": \""+id+"\"}]";

  Ciao.write("ddp", remoteFunction, parameter);

  delay(500);
}

```

## History

**Version** 0.0.1

- Initial implementation, add ability to remote call

## TODO

- Add implementation of read method to receive information from Meteor


