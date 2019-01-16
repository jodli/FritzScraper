
import paho.mqtt.client as mqtt

class MqttConnection(object):
  _client = None
  _address = ''
  _port = 0
  _user = ''
  _pw = ''
  _id = ''
  _base_topic = ''
  _connected = False

  def __init__(self, address, port, user, pw, id, base_topic):
    self._address = address
    self._port = port
    self._user = user
    self._pw = pw
    self._id = id
    self._base_topic = base_topic
    self._connected = False

    self._client = mqtt.Client(self._id)
    self._client.on_connect = self.on_connect
    self._client.on_disconnect = self.on_disconnect

  def on_connect(self, client, userdata, flags, rc):
    connack_string = {0:'Connection successful',
                      1:'Connection refused - incorrect protocol version',
                      2:'Connection refused - invalid client identifier',
                      3:'Connection refused - server unavailable',
                      4:'Connection refused - bad username or password',
                      5:'Connection refused - not authorised'}

    if rc:
      print(connack_string[rc])
    else:
      print("Connection status: " + connack_string[rc])
      self._connected = True

  def on_disconnect(self, client, userdata, rc):
    if rc != 0:
      print("Unexpected disconnection")
    print("Disconnected from MQTT Broker.")
    self._connected = False
    self._client.loop_stop()

  def connect(self):
    if not self._connected:
      print("Connecting to MQTT Broker.")
      try:
        self._client.username_pw_set(self._user, self._pw)
        self._client.connect(self._address, self._port, 60)
      except:
        print("Error connecting...")
      self._client.loop_start()

  def disconnect(self):
    self._client.disconnect()

  def publish(self, fscargo):
    if self._connected:
      for name, value in fscargo.cargo.items():

        # Construct topic
        topic = self._base_topic + '/' + str(name)
        payload = str(value)

        print("Publishing: " + topic + " " + payload)
        result, mid = self._client.publish(topic, payload=payload, qos=2, retain=False)

        if result == 4:
          print("Publishing error with id: " + str(mid))
