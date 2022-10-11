# MIT License
# Copyright (c) 2022 Andrej988
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
# documentation files (the "Software"), to deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of
# the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
# THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import logging

import paho.mqtt.client as mqtt


class MqttPublisher:
    def __init__(self,
                 broker_hostname,
                 port=1883,
                 keepalive=60,
                 connection_type='MQTT',
                 username=None,
                 password=None,
                 tls_config=None):
        self.class_name = "MqttPublisher"
        self.broker_hostname = broker_hostname
        self.port = port
        self.keepalive = keepalive
        self.connection_type = connection_type
        self.username = username
        self.password = password
        self.tls_config = tls_config
        self.client = None

    def __connect(self):
        self.client = mqtt.Client()
        self.client.on_connect = self.__on_connect
        self.client.on_log = self.__on_log
        if self.connection_type == 'TLS' and self.tls_config is not None:
            self.client.tls_set(ca_certs=self.tls_config.get('ca_certs'),
                                certfile=self.tls_config.get('certfile'),
                                keyfile=self.tls_config.get('keyfile'),
                                cert_reqs=self.tls_config.get('cert_reqs'),
                                tls_version=self.tls_config.get('tls_version'),
                                ciphers=self.tls_config.get('ciphers'),
                                keyfile_password=self.tls_config.get('keyfile_password'))
        if self.username is not None and self.password is not None:
            self.client.username_pw_set(username=self.username,
                                        password=self.password)
        self.client.connect(host=self.broker_hostname,
                            port=self.port,
                            keepalive=self.keepalive)

    def __disconnect(self):
        self.client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code {rc}")

    def __on_log(self, client, userdata, level, buf):
        print("log: ", buf)

    def publish(self, topic, json_payload, qos, retain_msg):
        log = logging.getLogger(self.class_name + ".publish")
        log.info("Connecting to MQTT Broker {0}".format(self.broker_hostname))
        self.__connect()
        log.info("Connection successful")
        log.info("Publishing to topic {0}".format(topic))
        self.client.publish(topic=topic,
                            payload=json_payload,
                            qos=qos,
                            retain=retain_msg)
        log.info("Message successfully published")
        self.__disconnect()
        log.info("Client disconnected")

