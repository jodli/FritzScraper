#!/usr/bin/env python

import fritzconnection as fc
import fritzscrapercargo as fsc

import time

class Scraper(object):
  _connection = None
  _address = ''
  _port = 0
  _last_bytes_sent = 0
  _last_bytes_received = 0
  _last_traffic_call = 0.0
  _fscargo = {}

  def __init__(self, address, port):
    self._address = address
    self._port = port
    self._connection = fc.FritzConnection(address=self._address, port=self._port)
    print("Connected to FritzBox")

    self._last_bytes_sent = self.bytes_sent 
    self._last_bytes_received = self.bytes_received
    self._last_traffic_call = time.time()

  @property
  def modelname(self):
    return self._connection.modelname

  @property
  def is_linked(self):
    status = self._connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    return status['NewPhysicalLinkStatus'] == 'Up'

  @property
  def is_connected(self):
    status = self._connection.call_action('WANIPConnection', 'GetStatusInfo')
    return status['NewConnectionStatus'] == 'Connected'

  @property
  def wan_access_type(self):
    return self._connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')['NewWANAccessType']

  @property
  def external_ip(self):
    return self._connection.call_action('WANIPConnection', 'GetExternalIPAddress')['NewExternalIPAddress']

  @property
  def uptime(self):
    return self._connection.call_action('WANIPConnection', 'GetStatusInfo')['NewUptime']

  @property
  def bytes_received(self):
    return self._connection.call_action('WANCommonInterfaceConfig', 'GetTotalBytesReceived')['NewTotalBytesReceived']

  @property
  def bytes_sent(self):
    return self._connection.call_action('WANCommonInterfaceConfig', 'GetTotalBytesSent')['NewTotalBytesSent']

  @property
  def transmission_rate(self):
    # Convert to bits
    sent = self.bytes_sent * 8
    received = self.bytes_received * 8

    traffic_call = time.time()
    time_delta = traffic_call - self._last_traffic_call
    upstream = int(1.0 * (sent - self._last_bytes_sent)/time_delta)
    downstream = int(1.0 * (received - self._last_bytes_received)/time_delta)
    self._last_bytes_sent = sent
    self._last_bytes_received = received
    self._last_traffic_call = traffic_call
    return upstream, downstream

  @property
  def max_bitrate(self):
    status = self._connection.call_action('WANCommonInterfaceConfig', 'GetCommonLinkProperties')
    downstream = status['NewLayer1DownstreamMaxBitRate']
    upstream = status['NewLayer1UpstreamMaxBitRate']
    return upstream, downstream

  def get_cargo(self):
    self.update_data()
    return self._fscargo

  def update_data(self):
    cargo = {}
    #cargo["model_name"] = self.modelname
    cargo["is_linked"] = int(self.is_linked)
    cargo["is_connected"] = int(self.is_connected)
    #cargo["wan_access_type"] = self.wan_access_type
    #cargo["external_ip"] = self.external_ip
    cargo["uptime"] = self.uptime
    cargo["bytes_received"] = self.bytes_received
    cargo["bytes_sent"] = self.bytes_sent
    transmission_rate_upstream, transmission_rate_downstream = self.transmission_rate
    cargo["transmission_rate_upstream"] = transmission_rate_upstream
    cargo["transmission_rate_downstream"] = transmission_rate_downstream
    max_bitrate_upstream, max_bitrate_downstream = self.max_bitrate
    cargo["max_bitrate_upstream"] = max_bitrate_upstream
    cargo["max_bitrate_downstream"] = max_bitrate_downstream

    self._fscargo = fsc.FritzScraperCargo(cargo)

  def print_status(self):
    print("time: " + str(self._fscargo.timestamp))
    for name, value in self._fscargo.cargo.items():
      print(name + ": " + str(value))
