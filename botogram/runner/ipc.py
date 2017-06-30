# Copyright (c) 2015-2017 The Botogram Authors (see AUTHORS)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
#   FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
#   DEALINGS IN THE SOFTWARE.

import os
import select
import socket
import random
import struct
import pickle
import hashlib

import logbook


PACKET_LENGTH_SECTION_SIZE = 4
READ_MAX_CHUNK = 4096
PORTS_RANGE = 49152, 65535
MAX_CONNECT_TRIES = 20


class IPCError(Exception):
    pass


class IPCServerCrashedError(IPCError):
    pass


class IPCServer:
    """Main server for the IPC"""

    def __init__(self):
        self.logger = logbook.Logger("botogram IPC server")

        self.commands = {}

        self.auth_key = hashlib.sha1(os.urandom(64)).hexdigest()
        self.stop_key = hashlib.sha1(os.urandom(64)).hexdigest()

        self.stop = False
        self.port, self.conn = self._get_connection()

    def _get_connection(self):
        """Create a new server connection"""
        count = 0
        tried = []
        # Let's try until an empty port is found
        while count < MAX_CONNECT_TRIES:
            # The port is chosen at random from the public range
            port = random.randint(*PORTS_RANGE)

            # Don't try the same port every time
            if port in tried:
                continue
            tried.append(port)

            # Create the socket and try to bind it to the port
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                sock.bind(("localhost", port))
            except socket.error:
                sock.close()
                # This will try with another port
                count += 1
                continue

            return port, sock

        # If the code reaches this state, no free port was found
        raise RuntimeError("Can't find an open port to bind the IPC socket")

    def register_command(self, name, func):
        """Register a new command"""
        if not callable(func):
            raise RuntimeError("Commands must be callable!")

        self.commands[name] = func

    def run(self):
        """Run the IPC server"""
        read_from = [self.conn]
        needs_authentication = []

        self.conn.listen(5)
        while not self.stop:

            # This is needed because sometimes the system call stops when
            # sending to the process the interruption signal
            # In this case, we'll just call the system call again
            try:
                readable, *_ = select.select(read_from, [], [])
            except InterruptedError:
                continue

            for conn in readable:
                # If the connection we can read is the server one, accept the
                # new connection and add it to the read_from list
                if conn is self.conn:
                    new_conn, addr = conn.accept()
                    needs_authentication.append(new_conn)
                    read_from.append(new_conn)

                    self.logger.debug("New IPC connection from %s:%s" % addr)
                else:
                    try:
                        request = read_packet(conn)
                    # If the socket is broken, remove the connection
                    except EOFError:
                        read_from.remove(conn)
                        try:
                            conn.shutdown(socket.SHUT_RDWR)
                        except OSError:
                            pass
                        conn.close()
                        continue

                    # If the connection isn't authenticated, check auth code
                    if conn in needs_authentication:
                        # Allow only the __authenticate__ command
                        if request["command"] != "__authenticate__":
                            write_packet(conn, {
                                "ok": False,
                                "data": "Please authenticate",
                            })
                            continue

                        # Match the authentication key
                        if request["data"] != self.auth_key:
                            write_packet(conn, {
                                "ok": False,
                                "data": "Authentication failed",
                            })
                            continue

                        write_packet(conn, {
                            "ok": True,
                            "data": "Welcome!"
                        })

                        needs_authentication.remove(conn)
                        continue

                    # __stop__ will stop the IPC server
                    if request["command"] == "__stop__":
                        # Allow only matching stop keys
                        if request["data"] != self.stop_key:
                            write_packet(conn, {
                                "ok": False,
                                "data": "Wrong stop key",
                            })
                            continue

                        self.stop = True
                        write_packet(conn, {
                            "ok": True,
                            "data": "Bye!",
                        })
                        break

                    self.process(conn, request)

        # Gracefully close all the connections
        for conn in read_from:
            try:
                conn.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            conn.close()

    def process(self, conn, request):
        """Process a single request"""
        command = request["command"]
        request_data = request["data"]

        self.logger.debug("Received IPC command %s" % command)

        def reply(data, ok=True):
            response = {"ok": ok, "data": data}
            write_packet(conn, response)

        if command not in self.commands:
            reply("Command not supported!", False)
            return

        self.commands[command](request_data, reply)

    def stop(self):
        """Stop the server"""
        self.stop = True


class IPCClient:
    """Client for the Inter-Process Communication"""

    def __init__(self, port, auth_key):
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn.connect(("localhost", port))

        self.command("__authenticate__", auth_key)

    def command(self, command, data):
        """Send a command to the IPC server"""
        packet = {"command": command, "data": data}
        try:
            write_packet(self.conn, packet)
        except BrokenPipeError:
            raise IPCServerCrashedError("The IPC server just crashed")

        response = read_packet(self.conn)
        if response["ok"]:
            return response["data"]

        raise IPCError(response["data"])

    def close(self):
        """Close the connection to the IPC server"""
        try:
            self.conn.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.conn.close()


def _read_from_socket(conn, length):
    """Read a chunk of data from a connection"""
    chunks = []
    remaining = length
    while remaining > 0:
        # Read a maximum of READ_MAX_CHUNK each iteration
        chunk = remaining
        if chunk > READ_MAX_CHUNK:
            chunk = READ_MAX_CHUNK

        # In Python 3.4, when the process received a signal every system call
        # is interrupted, so it's better to retry sending the data instead of
        # crashing when someone signals the process
        try:
            resp = conn.recv(chunk)
        except InterruptedError:
            continue

        if len(resp) == 0:
            raise EOFError("Broken socket!")

        chunks.append(resp)
        remaining -= len(resp)

    return b''.join(chunks)


def _write_on_socket(conn, data):
    """Write a chunk of data on a connection"""
    remaining = len(data)
    while remaining > 0:
        # In Python 3.4, when the process received a signal every system call
        # is interrupted, so it's better to retry sending the data instead of
        # crashing when someone signals the process
        try:
            sent = conn.send(data[len(data) - remaining:])
        except InterruptedError:
            continue

        if sent == 0:
            raise EOFError("Broken socket!")

        remaining -= sent


def read_packet(conn):
    """Read a packet from a connection"""
    size_raw = _read_from_socket(conn, PACKET_LENGTH_SECTION_SIZE)
    size = struct.unpack("I", size_raw)[0]

    result_raw = _read_from_socket(conn, size)
    return pickle.loads(result_raw)


def write_packet(conn, data):
    """Write a packet to a connection"""
    pickled = pickle.dumps(data)
    size = struct.pack("I", len(pickled))

    _write_on_socket(conn, size)
    _write_on_socket(conn, pickled)
