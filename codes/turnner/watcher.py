# 监听服务，接收参数，进行分拣模块的转向动作控制
import socket

from turnner import TurnController

from http.server import BaseHTTPRequestHandler, HTTPServer

HOST_NAME = 'localhost'
PORT_NUMBER = 8080 

class MyHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        print("1/ 执行分拣模块初始化\r\n")
        self.wfile.write(b'1 initialize sort \x3c\x5c\x62\x72\x3e')
        turnner = TurnController()

        print("2/ 执行分拣模块转向动作: 左转\r\n")
        self.wfile.write(b'2 sort turn left \x3c\x5c\x62\x72\x3e')
        turnner.run("left", 1)
        self.wfile.write(b'Hello, World!')

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        print(post_data)
        # 解析参数 进行控制操作
        turnner = TurnController()
        turnner.run("left", 1)
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(b'Hello, World!')

if __name__ == '__main__':
    server = HTTPServer((HOST_NAME, PORT_NUMBER), MyHandler)
    print('Server started http://%s:%s' % (HOST_NAME, PORT_NUMBER))

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    
    turnner = TurnController()
    turnner.stop()
    server.server_close()
    print('Server stopped.')



