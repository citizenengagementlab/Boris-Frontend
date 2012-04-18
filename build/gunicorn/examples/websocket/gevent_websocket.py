# -*- coding: utf-8 -
#
# This file is part of gunicorn released under the MIT license. 
# See the NOTICE for more information.
#
# Example code from Eventlet sources

import collections
import errno
import re
from hashlib import md5
import socket
import struct

import gevent
from gevent.pool import Pool
from gunicorn.workers.async import ALREADY_HANDLED

# Parts adapted from http://code.google.com/p/pywebsocket/
# mod_pywebsocket/handshake/handshake.py

class WebSocketWSGI(object):
    def __init__(self, handler):
        self.handler = handler
    
    def verify_client(self, ws):
        pass

    def _get_key_value(self, key_value):
        if not key_value:
            return
        key_number = int(re.sub("\\D", "", key_value))
        spaces = re.subn(" ", "", key_value)[1]
        if key_number % spaces != 0:
            return
        part = key_number / spaces
        return part

    def __call__(self, environ, start_response):
        if not (environ['HTTP_CONNECTION'] == 'Upgrade' and
            environ['HTTP_UPGRADE'] == 'WebSocket'):
            # need to check a few more things here for true compliance
            start_response('400 Bad Request', [('Connection','close')])
            return []
                    
        sock = environ['gunicorn.socket']

        ws = WebSocket(sock, 
            environ.get('HTTP_ORIGIN'),
            environ.get('HTTP_WEBSOCKET_PROTOCOL'),
            environ.get('PATH_INFO'))

        key1 = self._get_key_value(environ.get('HTTP_SEC_WEBSOCKET_KEY1'))
        key2 = self._get_key_value(environ.get('HTTP_SEC_WEBSOCKET_KEY2'))

        handshake_reply = ("HTTP/1.1 101 Web Socket Protocol Handshake\r\n"
                   "Upgrade: WebSocket\r\n"
                   "Connection: Upgrade\r\n")

        if key1 and key2:
            challenge = ""
            challenge += struct.pack("!I", key1)  # network byteorder int
            challenge += struct.pack("!I", key2)  # network byteorder int
            challenge += environ['wsgi.input'].read()
            handshake_reply +=  (
                       "Sec-WebSocket-Origin: %s\r\n"
                       "Sec-WebSocket-Location: ws://%s%s\r\n"
                       "Sec-WebSocket-Protocol: %s\r\n"
                       "\r\n%s" % (
                            environ.get('HTTP_ORIGIN'), 
                            environ.get('HTTP_HOST'), 
                            ws.path,
                            environ.get('HTTP_SEC_WEBSOCKET_PROTOCOL'), 
                            md5(challenge).digest()))

        else:

            handshake_reply += (
                       "WebSocket-Origin: %s\r\n"
                       "WebSocket-Location: ws://%s%s\r\n\r\n" % (
                            environ.get('HTTP_ORIGIN'), 
                            environ.get('HTTP_HOST'), 
                            ws.path))

        sock.sendall(handshake_reply)

        try:
            self.handler(ws)
        except socket.error, e:
            if e[0] != errno.EPIPE:
                raise
        # use this undocumented feature of grainbows to ensure that it
        # doesn't barf on the fact that we didn't call start_response
        return ALREADY_HANDLED

def parse_messages(buf):
    """ Parses for messages in the buffer *buf*.  It is assumed that
    the buffer contains the start character for a message, but that it
    may contain only part of the rest of the message. NOTE: only understands
    lengthless messages for now.
    
    Returns an array of messages, and the buffer remainder that didn't contain 
    any full messages."""
    msgs = []
    end_idx = 0
    while buf:
        assert ord(buf[0]) == 0, "Don't understand how to parse this type of message: %r" % buf
        end_idx = buf.find("\xFF")
        if end_idx == -1:
            break
        msgs.append(buf[1:end_idx].decode('utf-8', 'replace'))
        buf = buf[end_idx+1:]
    return msgs, buf
        
def format_message(message):
    # TODO support iterable messages
    if isinstance(message, unicode):
        message = message.encode('utf-8')
    elif not isinstance(message, str):
        message = str(message)
    packed = "\x00%s\xFF" % message
    return packed


class WebSocket(object):
    def __init__(self, sock, origin, protocol, path):
        self.sock = sock
        self.origin = origin
        self.protocol = protocol
        self.path = path
        self._buf = ""
        self._msgs = collections.deque()
    
    def send(self, message):
        packed = format_message(message)
        # if two greenthreads are trying to send at the same time
        # on the same socket, sendlock prevents interleaving and corruption
        self.sock.sendall(packed)
            
    def wait(self):
        while not self._msgs:
            # no parsed messages, must mean buf needs more data
            delta = self.sock.recv(1024)
            if delta == '':
                return None
            self._buf += delta
            msgs, self._buf = parse_messages(self._buf)
            self._msgs.extend(msgs)
        return self._msgs.popleft()


# demo app
import os
import random
def handle(ws):
    """  This is the websocket handler function.  Note that we 
    can dispatch based on path in here, too."""
    if ws.path == '/echo':
        while True:
            m = ws.wait()
            if m is None:
                break
            ws.send(m)
            
    elif ws.path == '/data':
        for i in xrange(10000):
            ws.send("0 %s %s\n" % (i, random.random()))
            gevent.sleep(0.1)
                            
wsapp = WebSocketWSGI(handle)
def app(environ, start_response):
    """ This resolves to the web page or the websocket depending on
    the path."""
    if environ['PATH_INFO'] == '/' or environ['PATH_INFO'] == "":
        data = open(os.path.join(
                     os.path.dirname(__file__), 
                     'websocket.html')).read()
        data = data % environ
        start_response('200 OK', [('Content-Type', 'text/html'),
                                 ('Content-Length', len(data))])
        return [data]
    else:
        return wsapp(environ, start_response)
