# FritzScraper

### This is my take on a scraper for data from my AVM FritzBox.

It utilizes the awesome [fritzconnection](https://bitbucket.org/kbr/fritzconnection) library by Klaus Bremer.

It then uses the [paho-mqtt](http://www.eclipse.org/paho/) library to send the data via MQTT to my HomeMonitoring system.

#### Infrastructure

There is a docker-compose file that builds the Dockerfile, binds the volume and runs the script.

The [startup script](src/startup.sh) handles sigterm and the requirements (for faster startup this is commented out by default in the shell script) and tails the output to std::out.

#### Configuration

The scrape interval is defined in the [fritzscraper.py](src/fritzscraper.py) file. It is by default set to `5` seconds.

The ip address and port of the FritzBox connection is defined in the [scraper.py](src/scraper.py) file. It is by default set to `192.168.0.1` and port `49000`.

The ip address and port of the MQTT server is defined in the [mqttconnection.py](src/mqttconnection.py) file.
It is by default set to `192.168.0.48` and port `1883`.
The MQTT id and topic is by default set to `FritzScraper` and `fritzscraper/fritz_1`.
The MQTT username and pw can also be set in this file.
