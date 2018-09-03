from ifHandler import InterferHandler


STATIC_PATH = '/static'


class application(object):
    def __init__(self, interfaces):
        self.interfaces = interfaces

    def __call__(self, env, args):
        method = env.get('METHOD', 'GET')
        path = env.get('PATH', '/404.html')

        if method == 'GET':
            if path.find('?') > -1:
                _list = path.split('?')
                path = _list[0]
                params = _list[1]

            # 通过get方式获取静态资源
            if path == '/' or path[-5:] == '.html' \
                    or path[-3:] == '.js' or path[-4:] == '.css':
                return self.get_page(path)

        elif method == 'POST':
            # 通过post方式获取接口

            if path[-3:] == '.rc':
                
                return self.get_data(path, args)

    def get_page(self, path):
        
        if path == '/':
            path = '/index.html'
        try:
            f = open('./' + STATIC_PATH + path)
        except Exception:
            response_header = 'HTTP/1.1 404 Not Found\r\n'
            response_header += '\r\n'
            response_body = 'not found the page'
        else:
            response_header = 'HTTP/1.1 200 OK\r\n'
            response_header += '\r\n'
            response_body = f.read()
            f.close()
        return response_header + response_body

    def get_data(self, path, args):
        for rc, handler in self.interfaces:
            if path == rc:
                response_header = 'HTTP/1.1 200 OK\r\n'
                response_header += '\r\n'
                response_body = getattr(if_handler, handler)(args)
                return response_header + response_body
                
        else:
            response_header = 'HTTP/1.1 404 Not Found\r\n'
            response_header += '\r\n'
            response_body = '{"code":404, "data":{}, "msg":"未定义接口"}'
            return response_header + response_body

interfaces = [
    ('/login.rc', 'do_login'),
    ('/regist.rc', 'do_regist'),
    ('/searchWord.rc', 'do_search_word'),
    ('/searchHist.rc', 'do_search_hist'),
]

if_handler = InterferHandler()
app = application(interfaces)
