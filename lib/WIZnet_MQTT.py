import machine
import network
import time
from simple import MQTTClient

class WIZnetMQTT:
    def __init__(self, username, broker_ip, pub_topic, sub_topic, keep_alive, callback=None):
        self.username = username
        self.broker_ip = broker_ip
        self.pub_topic = pub_topic
        self.sub_topic = sub_topic
        self.keep_alive = keep_alive
        self.callback = callback

    def init_mqtt(self):
        self.client = MQTTClient(self.username, self.broker_ip, keepalive=self.keep_alive)
        self.client.set_callback(self.sub_cb)
        self.client.connect()
        self.client.subscribe(self.sub_topic)

    def sub_cb(self, sub_topic, msg):
        if self.callback:
            self.callback(sub_topic, msg)
            return None
        else:            
            return topic, msg

    def publish(self, message):
        self.client.publish(self.pub_topic, message)
        print('Published message:', message)

    def check_msg(self):
        msg = self.client.check_msg()
        return None

    def disconnect(self):
        self.client.disconnect()
