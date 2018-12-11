import socket
import time
import threading

isNormar = True


def rev_message(username, s):
    global isNormar

    s.send(username.encode())
    print("正在登陆......")
    #  获取返回消息
    return_msg = s.recv(1024).decode()
    if return_msg == "login success":
        print("登陆成功！")

        #  启动心跳包
        threading.Thread(target=heart_beat, args=[s]).start()

        while isNormar:
            data = s.recv(1024).decode()
            sendAccount = data.split("@")[0]
            sendTime = data.split("@")[1]
            messageContent = data.split("@")[2]
            print("[%s]: \"%s\" 给你发送了一条消息: %s" % (sendTime, sendAccount, messageContent))
    else:
        print("登陆失败......")


#  心跳包
def heart_beat(s):
    global isNormar

    while isNormar:
        s.send("-".encode())
        time.sleep(0.5)


def main():
    global isNormar

    s = socket.socket()

    try:
        username = input('请输入您的用户名:')
        s.connect(("112.74.168.99", 8888))
        t = threading.Thread(target=rev_message, args=(username, s))
        t.start()

    except Exception as e:
        print(e)
        print("连接异常......")
        isNormar = False
    finally:
        pass

    while isNormar:
        msg = input("输入要发送的对象和内容，以@间隔\n")  # 接受用户输入
        if msg == "exit":
            isNormar = False
        else:
            s.send(msg.encode())  # 编码消息并发送

    s.close()

main()