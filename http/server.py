#!/usr/bin/env python
#--coding:utf-8--

from http.server import BaseHTTPRequestHandler, HTTPServer
from os import path
from urllib.parse import urlparse

class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
	# GET
	def do_GET(self):

		querypath = urlparse(self.path)
		print(querypath)
		filepath, query = querypath.path, querypath.query
		print(query)
		try:
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(bytes(query,'utf-8'))
		except IOError:
			self.send_error(404,'Bad Page.')

def run():
	port = 8000
	print('starting server, port', port)

	# Server settings
	server_address = ('', port)
	httpd = HTTPServer(server_address, testHTTPServer_RequestHandler)
	print('running server...')
	httpd.serve_forever()

if __name__ == '__main__':
	run()