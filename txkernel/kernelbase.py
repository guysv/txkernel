# txkernel
# Copyright (C) 2018  guysv

# This file is part of txkernel which is released under GPLv2.
# See file LICENSE or go to https://www.gnu.org/licenses/gpl-2.0.txt
# for full license details.

import txzmq
from twisted.internet import reactor, defer, task
from twisted.logger import Logger
from . import sockets, message

class KernelBase(object):
    # default kernel_info
    protocol_version = '5.3.0' # TODO: duplicate var in message.py??
    # calm down linter
    implementation = None
    implementation_version = None
    language_info = None
    banner = None

    help_links = []

    log = Logger()

    def __init__(self, connection_props):
        self.connection_props = connection_props

        sign_scheme = self.connection_props["signature_scheme"]
        key = self.connection_props["key"]
        self.message_manager = message.MessageManager(sign_scheme, key)

        self.zmq_factory = txzmq.ZmqFactory()
        self.zmq_factory.registerForShutdown()
        self.execution_count = 0
        
        transport = self.connection_props["transport"]
        addr = self.connection_props["ip"]

        # the shell_sock is circular-referencing
        # it is only allocated once on app up and down tho
        shell_endpoint = self._endpoint(transport, addr,
                                        self.connection_props["shell_port"])
        self.shell_sock = sockets.ShellConnection(self.handle_message,
                                                  self.zmq_factory,
                                                  shell_endpoint)

        ctrl_endpoint = self._endpoint(transport, addr,
                                       self.connection_props["control_port"])
        self.ctrl_sock = sockets.ShellConnection(self.handle_message,
                                                 self.zmq_factory,
                                                 ctrl_endpoint)
        
        iopub_endpoint = self._endpoint(transport, addr,
                                        self.connection_props["iopub_port"])
        self.iopub_sock = sockets.IOPubConnection(self.zmq_factory,
                                                  iopub_endpoint)
        
        stdin_endpoint = self._endpoint(transport, addr,
                                        self.connection_props["stdin_port"])
        self.stdin_sock = sockets.StdinConnection(self.zmq_factory,
                                                  stdin_endpoint)
        
        hb_endpoint = self._endpoint(transport, addr,
                                     self.connection_props["hb_port"])
        self.hb_sock = sockets.HearbeatConnection(self.zmq_factory,
                                                  hb_endpoint)
        
        self.send_update("status", {'execution_state': 'starting'})

    def run(self):
        self.stop_deferred = defer.Deferred()
        @defer.inlineCallbacks
        def do_init(reactor):
            self.send_update("status", {'execution_state': 'idle'})
            val = yield self.stop_deferred
            defer.returnValue(val)

        task.react(do_init)

    @defer.inlineCallbacks
    def handle_message(self, request_socket, sender_id, message_parts):
        try:
            self.send_update("status", {'execution_state': 'busy'})

            # extra ids? probebly will never be used
            # TODO: catch parsing errors
            msg, _ = self.message_manager.parse(message_parts)

            msg_type = msg['header']['msg_type']
            if msg_type == 'kernel_info_request':
                resp_type = 'kernel_info_reply'
                content = yield self.do_kernel_info(**msg['content'])
            elif msg_type == 'execute_request':
                resp_type = "execute_reply"
                
                # TODO: currently we can't stop on error, so no way
                # to handle that..
                msg['content'].pop('stop_on_error', None)
                content = yield self.do_execute(**msg['content'])
            elif msg_type == 'is_complete_request':
                resp_type = "is_complete_reply"
                content = yield self.do_is_complete(**msg['content'])
            else:
                self.log.error("Unknown request type {req_type}",
                               req_type=msg_type)
                defer.returnValue(None)
            
            msg_bin = self.message_manager.build(resp_type, content,
                                                msg['header'])
            request_socket.sendMultipart(sender_id, msg_bin)

            self.send_update("status", {'execution_state': 'idle'})
        except Exception as e:
            self.stop_deferred.errback(e)

    def do_kernel_info(self):
        return {
            'protocol_version': self.protocol_version,
            'implementation': self.implementation,
            'implementation_version': self.implementation_version,
            'language_info': self.language_info,
            'banner': self.banner,
            'help_links': self.help_links
        }
    
    def do_execute(self, code, silent, store_history=True,
                   user_expressions=None, allow_stdin=False):
        raise NotImplementedError

    def do_is_complete(self, code):
        raise NotImplementedError

    def send_update(self, msg_type, content):
        msg = self.message_manager.build(msg_type, content)
        self.iopub_sock.publish(msg)

    @staticmethod
    def _endpoint(transport, addr, port,
                  type=txzmq.ZmqEndpointType.bind):
        url = "{}://{}:{}".format(transport, addr, port)
        return txzmq.ZmqEndpoint(type, url)
