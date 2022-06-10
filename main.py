#!/usr/bin python3

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import ssl
import json
import sys
from src.Manager.DialogManager import DialogManager
from tests.testServerConnection import testJSONExtractor

from src.Manager.RequestManager import RequestManager
from src.Manager.AutoFillManager import getStationNames

configFile = open('config.txt', 'r')
config = {}
for line in configFile.readlines():
    key, value = line.split(':')
    if "\n" in value:
        value= value[:-1]
    config[key] = value

HOSTNAME = "localhost" if config['develop'] == 'true' else ""
SERVERPORT = 8080 if config['develop'] == 'true' else 3000
DM = DialogManager(config)


class ThreadingSimpleServer(ThreadingMixIn, HTTPServer):
    pass


class MyServer(BaseHTTPRequestHandler):
    def __init__(self, request, client_address, server):
        self.DM = DM
        super().__init__(request, client_address, server)

    def do_OPTIONS(self):
        print("###############################")
        self.send_response(200, "ok")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods",
                         "GET, POST, OPTIONS, HEAD")
        self.send_header(
            "Access-Control-Allow-Headers", "X-Requested-With, Content-Type"
        )
        self.end_headers()

    def do_POST(self):
        content_length = int(self.headers["Content-Length"])
        try:
            # print(self.rfile.read(content_length))
            body = json.loads(self.rfile.read(content_length))
        except ValueError:
            print("has no body")
            body = "{}"

        if self.path == r"/request":
            print("request")
            req_man = RequestManager()
            req_man.setFromDict(body["informationPackage"])
            res = req_man.makeRequest()
            result = res.encode()
        elif self.path == r"/autofill":
            print("autofill")
            result = json.dumps(getStationNames(
                body), ensure_ascii=False).encode()
        else:
            print("NLU: ")
            if testJSONExtractor(body, self.DM.jsm):
                answer = self.DM.processRequest(body)
                print("everything seems fine")
                result = answer.encode()
            else:
                print("didnt worked")
                result = json.dumps(
                    {"Error": "json could not get extracted"}).encode()

        self.send_response(200)
        self.send_header("Access-Control-Allow-Credentials", "true")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-type", "application/json")
        self.send_header("Content-length", str(len(result)))
        self.end_headers()
        self.wfile.write(result)
        print("###############################")


if __name__ == "__main__":
    server = ThreadingSimpleServer((HOSTNAME, SERVERPORT), MyServer)
    if config['develop'] != 'true':
        server.socket = ssl.wrap_socket(server.socket,
                                        keyfile=r'/etc/letsencrypt/live/travel-catbot.de/privkey.pem',
                                        certfile=r'/etc/letsencrypt/live/travel-catbot.de/fullchain.pem')
    print("\nServer started http://%s:%s" % (HOSTNAME, SERVERPORT))
    try:
        while 1:
            sys.stdout.flush()
            server.handle_request()
    except KeyboardInterrupt:
        print('Server stopped...')
