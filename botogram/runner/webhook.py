from http.server import BaseHTTPRequestHandler, HTTPServer
from ipaddress import IPv4Network, IPv6Address, collapse_addresses,\
    ip_address, ip_network
from json import loads
from socketserver import _ServerSelector, selectors
from typing import List, Union

# Needed for parameters and return hints
from logbook import Logger

from . import jobs
from ..objects import Update


class HttpServer(HTTPServer):
    def serve_single(self, poll_interval=0.5):
        """Handle one request at a time until shutdown.

                Polls for shutdown every poll_interval seconds. Ignores
                self.timeout. If you need to do periodic tasks, do them in
                another thread.
                """
        self.__shutdown_request = False
        try:
            # XXX: Consider using another file descriptor or connecting to the
            # socket to wake this up instead of polling. Polling reduces our
            # responsiveness to a shutdown request and wastes cpu at all other
            # times.
            with _ServerSelector() as selector:
                selector.register(self, selectors.EVENT_READ)
                ready = selector.select(poll_interval)
                if ready:
                    self._handle_request_noblock()

                self.service_actions()
        finally:
            self.__shutdown_request = False


class WebHookHandler(BaseHTTPRequestHandler):
    # Handler for the Post requests
    def do_POST(self):
        path = self.path.split("/")[1:]
        ip_client = ip_address(self.client_address[0])
        if path[0] != "bot":
            self.send_response(501)
            return
        for filter_ip_network in self.server.filter:
            if ip_client in filter_ip_network:
                break
        else:
            self.send_response(401)
            return
        if path in self.server.bots.keys():
            length = int(self.headers['Content-Length'])
            data = loads(self.rfile.read(length).decode("utf-8"))
            update = Update(data)
            update.set_api(None)
            result = [jobs.Job(self.server.bots[path], jobs.process_update, {
                "update": update,
            })]
            self.server.ipc.command("jobs.bulk_put", result)
            self.send_response(200)
        else:
            self.send_response(404)


class WebHook:
    # ip telegram server
    ip_filter = [ip_network("149.154.160.0/20"),
                 ip_network("91.108.4.0/22")]

    def __init__(self,
                 final_url: str,
                 destroy_at_stop: bool = True,
                 ip_filters: Union[None, List[str, IPv4Network,
                                              IPv6Address],
                                   str, IPv4Network, IPv6Address] = None,
                 port: int = 88,
                 keyfile: Union[None, str] = None,
                 certfile: Union[None, str] = None):

        self.logger = Logger("botogram runner")
        if final_url.endswith("/"):
            self.final_url = final_url
        else:
            self.final_url = final_url + "/"
        if not self.final_url.startswith("https"):
            if self.final_url.startswith("http"):
                self.final_url.replace("http", "https")
                self.logger.warn("")
            else:
                self.final_url = "https://" + self.final_url

        self.destroy_at_stop = destroy_at_stop

        if ip_filters is not None:
            if not isinstance(ip_filters, list):
                ip_filters = [ip_filters]
            for ip_filter in ip_filters:
                if isinstance(ip_filter, str):
                    ip_filter = ip_network(ip_filter)
                    self.ip_filter.append(ip_filter)
                elif isinstance(ip_filter, IPv4Network):
                    self.ip_filter.append(ip_filter)
                elif isinstance(ip_filter, IPv6Address):
                    self.ip_filter.append(ip_filter)
                else:
                    raise ValueError(
                        "%r does not appear to be an IPv4 or IPv6 network",
                        ip_filter)
        self.ip_filters = [ipaddr for ipaddr in
                           collapse_addresses(self.ip_filters)]
        self.port = port

        if None in (keyfile, certfile):
            self.crypto = False
        else:
            self.crypto = True
            self.keyfile = keyfile
            self.certfile = certfile
