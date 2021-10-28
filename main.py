from http.server import HTTPServer, BaseHTTPRequestHandler
import re

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def _send_response(self, response_text : str = 'Empty', code : int = 200):
        self.send_response(code)
        self.end_headers()
        self.wfile.write(bytes(response_text, 'utf-8'))

    def do_GET(self):
        
        self._send_response(a)


a = 'hi dude'

httpd = HTTPServer(('localhost', 8000), SimpleHTTPRequestHandler)
httpd.serve_forever()