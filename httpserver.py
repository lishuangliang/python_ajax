from socket import *
from threading import Thread
import re
import sys
from config import *


class HTTPServer(object):
    def __init__(self, app):
        s = socket()
        s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        s.bind(('0.0.0.0', 8888))
        s.listen(10)

        self.s = s
        self.app = app

    def serve_forever(self):
        while True:
            try:
                connd, addr = self.s.accept()
                print('connect from ', addr)

                t = Thread(target=self.handler, args=(connd, ))
                t.setDaemon(True)
                t.start()
            except KeyboardInterrupt:
                self.s.close()
                sys.exit('服务端退出')
            except Exception as e:
                print('server error-->', e)
                continue


    def handler(self, c):
        request = c.recv(4096)
        request = request.splitlines()

        print(request)
        print('--------------')

        try:
            request_header = request[0].decode('utf-8')
        except:
            sys.exit('thread退出')

        # print(request_header)
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>\/\S*)'

        try:
            env = re.match(pattern, request_header).groupdict()
            response = self.app(env, request[len(request)-1])

        except Exception as e:
            print('error -->', e)
            response_header = 'HTTP/1.1 500 SERVER ERROR\r\n'
            response_header += '\r\n'
            response_body = 'server error'
            response = response_header + response_body

        c.send(response.encode())
        c.close()


def main():
    sys.path.insert(1, MODULE_PATH)
    m = __import__(MODULE)
    app = getattr(m, APP)

    httpd = HTTPServer(app)
    httpd.serve_forever()


if __name__ == '__main__':
    main()
