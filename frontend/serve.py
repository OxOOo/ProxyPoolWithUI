# encoding: utf-8

from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8000

def main():
    FILE_DIR = os.path.dirname(__file__)
    os.chdir(os.path.join(FILE_DIR, 'deployment'))
    httpd = HTTPServer(('0.0.0.0', PORT), SimpleHTTPRequestHandler)
    print(f'Running web server at http://localhost:{PORT}')
    httpd.serve_forever()

if __name__ == '__main__':
    main()
