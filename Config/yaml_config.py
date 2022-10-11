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

import yaml
import logging

log = logging.getLogger("Config")


class Config:
    def __init__(self, filename):
        self.filename = filename
        self.__open_config_file()

    def __open_config_file(self):
        try:
            with open(self.filename, "r") as config_file:
                self.data = yaml.load(config_file, Loader=yaml.FullLoader)
        except FileNotFoundError:
            raise Exception("File {} does not exist!!!".format(self.filename))

    def getSchedulerDelay(self):
        return self.data.get('scheduler').get('delay')

    def getAirthingsWavePlusBluetoothMACAddress(self):
        return self.data.get('airthings_wave_plus').get('bluetooth').get('mac_address')

    def getAirthingsWavePlusSerialNumber(self):
        return self.data.get('airthings_wave_plus').get('serial_number')

    def getPublishToKafka(self):
        return self.data.get('publishers').get('kafka').get('enabled')

    def getKafkaBootstrapServers(self):
        return self.data.get('publishers').get('kafka').get('bootstrap_servers')

    def getKafkaTopic(self):
        return self.data.get('publishers').get('kafka').get('topic')

    def getKafkaSecurityProtocol(self):
        return self.data.get('publishers').get('kafka').get('security_protocol')

    def getKafkaSSLCAFile(self):
        return self.data.get('publishers').get('kafka').get('ssl_ca_cert_file')

    def getKafkaSASLMechanism(self):
        return self.data.get('publishers').get('kafka').get('sasl_mechanism')

    def getKafkaSASLUsername(self):
        return self.data.get('publishers').get('kafka').get('sasl_username')

    def getKafkaSASLPassword(self):
        return self.data.get('publishers').get('kafka').get('sasl_password')

    def getPublishToMQTT(self):
        return self.data.get('publishers').get('mqtt').get('enabled')

    def getMQTTHostname(self):
        return self.data.get('publishers').get('mqtt').get('hostname')

    def getMQTTPort(self):
        return self.data.get('publishers').get('mqtt').get('port')

    def getMQTTConnectionType(self):
        return self.data.get('publishers').get('mqtt').get('connection_type')

    def getMQTTUsername(self):
        return self.data.get('publishers').get('mqtt').get('username')

    def getMQTTPassword(self):
        return self.data.get('publishers').get('mqtt').get('password')

    def getMQTTConfigTLS(self):
        return self.data.get('publishers').get('mqtt').get('tls')

    def getMQTTPublishTopic(self):
        return self.data.get('publishers').get('mqtt').get('topic')

    def getMQTTPublishQOS(self):
        return self.data.get('publishers').get('mqtt').get('qos')

    def getMQTTPublishRetainMsg(self):
        return self.data.get('publishers').get('mqtt').get('retain_msg')

    def getLoglevel(self):
        return self.data.get('log').get('level')


