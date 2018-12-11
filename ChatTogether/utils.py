import random
import hashlib
from django.core.mail import send_mail


class Utils:

    @staticmethod
    def send_register_emails(verify_code, to_email):
        subject = '欢迎注册TG聊天软件，本次的验证码为：' + verify_code
        message = 'TG--本次的验证码为：' + verify_code + '，\r\n请将验证码填入输入框中！'
        send_mail(subject, message, 'admin@94loveyou.cn',
                  [to_email], fail_silently=False)

    @staticmethod
    def send_error(error_msg):
        subject = "亲爱的管理员，TGChat服务器端捕捉到异常！"
        message = '异常的具体信息：\r\n' + error_msg
        send_mail(subject, message, 'admin@94loveyou.cn',
                  ["754709124@qq.com"], fail_silently=False)

    @staticmethod
    def send_forget_emails(verify_code, to_email):
        subject = '你的账号正在找回密码，本次的验证码为：' + verify_code
        message = 'TG--本次的验证码为：' + verify_code + '，\r\n请将验证码填入输入框中！'
        send_mail(subject, message, 'admin@94loveyou.cn',
                  [to_email], fail_silently=False)

    @staticmethod
    def get_random_string(length):
        string = "0123456789"
        result = ""
        for i in range(length):
            index = random.randint(0, 9)
            temp = string[index]
            result += temp
        return result

    @staticmethod
    def encrypt_by_sha1(string):
        m = hashlib.sha1()
        m.update(string.encode("utf8"))
        return m.hexdigest()

