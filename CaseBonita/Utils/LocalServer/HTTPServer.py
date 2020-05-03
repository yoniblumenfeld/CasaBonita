import http.server
import socketserver


class LocalServer(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = 'index.html'
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


if __name__ == '__main__':
    handler_object = LocalServer
    PORT = 7000
    my_server = socketserver.TCPServer(("", PORT), handler_object)
    my_server.serve_forever()
