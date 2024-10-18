from http.server import HTTPServer
from handlers import MyHandler

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, MyHandler)
    print('Starting server on port 8000...')
    httpd.serve_forever()