import socketserver
import time

#  全局变量 用户信息
''' 类型:Dict
    构成:String(ip:port): String userAccount '''
userInfoDict = {"admin": "0"}

#  全局变量 消息列表
'''类型:Dict
   构成:(接收方账号)String revAccount:{
    String sendAccount: "",
    String sendTime: "",
    String messageContent: "",
    } 
'''
messageListDict = {
    "admin": {
        "sendAccount": "",
        "sendTime": "",
        "messageContent": "",
    }
}


class MyHandler(socketserver.BaseRequestHandler):

    def handle(self):

        global userInfoDict
        global messageListDict

        try:
            while True:
                # 接收指令
                data = self.request.recv(1024).decode()

                if not data:
                    print("Connection Lost!")
                    break

                # 用户ip信息
                # 判断用户是否为新用户
                userInfo = str(self.client_address[0]) + "-" + str(self.client_address[1])

                if userInfoDict.get(userInfo, "True") == "True":
                    # 将 用户信息 加入 userInfoDict
                    userInfoDict[userInfo] = data

                    # 发送消息提示
                    msg = "login success"
                    print(msg)
                    self.request.sendall(msg.encode())
                    continue

                #  判断是否为心跳包
                if data == "-":
                    message_need_to_send = messageListDict.get(userInfoDict[userInfo], None)
                    if message_need_to_send is not None:

                        cur = messageListDict[userInfoDict[userInfo]]
                        sendAccount = cur["sendAccount"]
                        sendTime = cur["sendTime"]
                        messageContent = cur["messageContent"]
                        msg = ("%s@%s@%s" % (sendAccount, sendTime, messageContent)).encode()
                        self.request.sendall(msg)
                        messageListDict.pop(userInfoDict[userInfo])
                    continue
                # 接受指令
                print("{} send:\n".format(userInfoDict[userInfo]), data)

                # 处理指令
                revAccount = data.split("@")[0]
                messageContent = data.split("@")[1]
                sendTime = self.get_now_time()
                sendAccount = userInfoDict[userInfo]

                infoDict = {"sendAccount": sendAccount, "sendTime": sendTime, "messageContent": messageContent}
                messageListDict[revAccount] = infoDict
                msg = "admin@%s@已发送" % sendTime
                self.request.sendall(msg.encode())
        except Exception as e:
            print(e)
            print(self.client_address, "连接断开")
        finally:
            self.request.close()

    def setup(self):
        print("新客户端接入----" + str(self.client_address[0]) + ":" + str(self.client_address[1]))

    def finish(self):
        # 用户ip信息
        userInfo = str(self.client_address[0]) + "-" + str(self.client_address[1])
        if userInfoDict.get(userInfo, False):
            del userInfoDict[userInfo]
        print("完成处理")

    def get_now_time(self):
        now = time.time()
        str_millis = str(round(now * 1000))
        return str_millis


HOST, PORT = "0.0.0.0", 8888
server = socketserver.ThreadingTCPServer((HOST, PORT), MyHandler)
server.serve_forever()

