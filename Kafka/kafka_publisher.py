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

from kafka3 import KafkaProducer


class KafkaPublisher:
    def __init__(self,
                 bootstrap_servers,
                 security_protocol,
                 sasl_mechanism,
                 ssl_ca_cert_file=None,
                 sasl_username=None,
                 sasl_password=None):
        self.class_name = "KafkaPublisher"
        self.bootstrap_servers = bootstrap_servers
        self.security_protocol = security_protocol
        self.ssl_check_hostname = True
        self.ssl_ca_cert_file = ssl_ca_cert_file  # e.g. './CARoot.pem'
        self.sasl_mechanism = sasl_mechanism
        self.sasl_username = sasl_username
        self.sasl_password = sasl_password

    def __open_kafka_producer_connection(self):
        return KafkaProducer(bootstrap_servers=self.bootstrap_servers,
                             api_version=(0, 10),
                             security_protocol=self.security_protocol,
                             # ssl_context=context,
                             ssl_check_hostname=self.ssl_check_hostname,
                             ssl_cafile=self.ssl_ca_cert_file,
                             sasl_mechanism=self.sasl_mechanism,
                             sasl_plain_username=self.sasl_username,
                             sasl_plain_password=self.sasl_password)

    def publish(self, topic, json_payload):
        log = logging.getLogger(self.class_name + ".publish")

        producer = self.__open_kafka_producer_connection()
        log.info('Kafka Producer has been initiated...')

        producer.send(topic, json_payload)
        producer.flush()
        producer.close()
        log.info("Message successfully published to Kafka topic: {0}".format(topic))
