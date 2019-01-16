import scraper as fs
import mqttconnection as mqtt
import signal
import sys
import time
import os

class FritzScraper(object):
  _exit = False
  _interval = 0.0

  def __init__(self):
    self._exit = False
    self._interval = os.environ['SCRAPE_INTERVAL']
    signal.signal(signal.SIGTERM, self._sigterm_handler)

    self._scraper = fs.Scraper(os.environ['FRITZ_IP_ADDRESS'], os.environ['FRITZ_TCP_PORT'])
    self._mqttConnection = mqtt.MqttConnection(os.environ['MQTT_ADDRESS'], os.environ['MQTT_PORT'], os.environ['MQTT_ID'], os.environ['MQTT_BASE_TOPIC'], os.environ['MQTT_USER'], os.environ['MQTT_PASSWORD'])

  def _sigterm_handler(self, signal, frame):
    print("SIGTERM received")
    self._exit = True

  def run(self):
    while not self._exit:
      self._mqttConnection.connect()
      fscargo = self._scraper.get_cargo()
      self._mqttConnection.publish(fscargo)

      print("Sleep for " + str(_interval) + "s")
      sys.stdout.flush()
      time.sleep(_interval)

  def close(self):
    print("Cleaning up...")
    self._mqttConnection.disconnect()

if __name__ == '__main__':

  try:
    print("Creating FritzScraper...")
    fritzScraper = FritzScraper()
  except Exception as e:
    sys.exit("Could not create FritzScraper: " + str(e))
  else:
    fritzScraper.run()

    fritzScraper.close()
