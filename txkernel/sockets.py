# txkernel
# Copyright (C) 2018  guysv

# This file is part of txkernel which is released under GPLv3.
# See file LICENSE or go to https://www.gnu.org/licenses/gpl-3.0.txt
# for full license details.

"""
This module implements the different ZeroMQ
sockets used in the Jupyter protocol

The sockets provide a simple API for the
kernel to communicate with the frontend
"""
import txzmq
from twisted.internet import defer

class HearbeatConnection(txzmq.ZmqREPConnection):
    def gotMessage(self, messageId, *messageParts):
        self.reply(messageId, *messageParts)

class ShellConnection(txzmq.ZmqRouterConnection):
    def __init__(self, message_handler, *args, **kwargs):
        self.message_handler = message_handler
        super().__init__(*args, **kwargs)
    
    def gotMessage(self, sender_id, *messageParts):
        self.message_handler(self, sender_id, messageParts)
    
class IOPubConnection(txzmq.ZmqPubConnection):
    def publish(self, message):
        self.send(message)

class StdinConnection(txzmq.ZmqRouterConnection):
    pass
