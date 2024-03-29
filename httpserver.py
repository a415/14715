from socket import *
import sys 
import re
from threading import Thread 
from setting import *
import time 

class HTTPServer(object):
    def __init__(self,addr = ('0.0.0.0',80)):
        self.sockfd = socket()
        self.sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1) 
        self.addr = addr
        self.bind(addr) 

    def bind(self,addr):
        self.ip = addr[0]
        self.port = addr[1]
        self.sockfd.bind(addr)

    #HTTP服务器启动
    def serve_forever(self):
        self.sockfd.listen(10)
        print("Listen the port %d..."%self.port)
        while True:
            connfd,addr = self.sockfd.accept()
            print("Connect from",addr)
            handle_client = Thread\
            (target = self.handle_request,args = (connfd,))
            handle_client.setDaemon(True)
            handle_client.start()

    def handle_request(self,connfd):
        #接收浏览器请求
        request = connfd.recv(4096)
        request_lines = request.splitlines()
        #获取请求行
        request_line = request_lines[0].decode()

        #正则提取请求方法和请求内容
        pattern = r'(?P<METHOD>[A-Z]+)\s+(?P<PATH>/\S*)'
        try:
            env = re.match(pattern,request_line).groupdict()
        except:
            response_headlers = "HTTP/1.1 500 Server Error\r\n"
            response_headlers += '\r\n'
            response_body = "Server Error"
            response = response_handlers + response_body
            connfd.send(response.encode())
            return
        #讲请求发给frame
        status,response_body = self.send_resquest(env['METHOD'],env['PATH'])
        response_headlers = self.get_headlers(status)
        #将结果组织为http_response发送给客户端
        connfd.send(response.encode())
        connfd.close() 
    #和frame交互
    def send_resquest(self,methon,path):
        s=socket()
        s.connect(frame_addr)
        s.send(method.encode())
        time.sleep(0.1)
        s.send(path.encode())

        status = s.recv(128).decode()
        response_body = s.recv(4096 * 10).decode()

        return status,response_body


    def get_headlers(self,status):
        if status == '200':
            response_headlers = 'HTTP/1.1 200 OK\r\n'
            response_headlers += '\r\n'
        elif status == '404':
            response_headlers = 'HTTP/1.1 404 Not Found\r\n'
            response_headlers += '\r\n'

        return response_headlers





if __name__ == "__main__":
    httpd = HTTPServer(ADDR)
    httpd.serve_forever()
