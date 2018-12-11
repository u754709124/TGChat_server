import re
import hashlib
import traceback

from ChatTogether.utils import Utils
from .models import UserInfo, UserLogin, Relationship
from django.http import JsonResponse
from ChatTogether.get_upload_token import get_upload_token


def register(requests):
    # 请求发送验证码
    if requests.method == "GET":
        e_mail = requests.GET.get("e-mail", "")
        target_filename = requests.GET["filename"]
        if re.match(r'^[0-9a-zA-Z_]{0,19}@[0-9a-zA-Z]{1,13}\.[com,cn,net]{1,3}$',e_mail):
            #  发送邮件
            random_string = Utils.get_random_string(6)
            Utils.send_register_emails(random_string, e_mail)
            #  获取上传文件token
            upload_token = get_upload_token(target_filename)
            return_json = {"status": "success", "msg": {"random_string": random_string, "upload_token": upload_token}}
            return JsonResponse(return_json)
        else:
            return_json = {"status": "failed", "msg": "邮箱格式不正确！"}
            return JsonResponse(return_json)
    elif requests.method == "POST":
        username = requests.POST["username"]
        hash_value = requests.POST["hashValue"]
        salt = requests.POST["salt"]
        e_mail = requests.POST["e-mail"]
        nickname = requests.POST["nickname"]
        head_image = requests.POST["image"]

        #  返回信息
        return_json = {}
        #  存入数据库
        try:
            # 查询服务器是否已经有该账号
            query_result = UserLogin.objects.filter(username=username).values("salt")
            query_result_list = list(query_result)
            if len(query_result_list):
                return_json = {"status": "failed", "msg": "重新选个账号哦，这个账号已经有人占领啦！"}
            else:
                # 将得到的密文和salt拼接进行sha1加密
                encrypt_value = Utils.encrypt_by_sha1(hash_value + salt)
                user_dict = {"username": username, "encrypt_value": encrypt_value, "salt": salt}
                UserLogin.objects.create(**user_dict)

                info_dict = {"username": username, "e_mail": e_mail, "nickname": nickname, "head_image": head_image}
                UserInfo.objects.create(**info_dict)
                return_json = {"status": "success", "msg": "注册成功，请重新登录！"}
        except Exception as e:
            error_msg = traceback.format_exc()
            Utils.send_error(error_msg)
            return_json = {"status": "failed", "msg": "服务器出现异常，管理员小哥哥正在排查..."}
        finally:
            return JsonResponse(return_json)


def login(requests):
    if requests.method == "POST":
        username = requests.POST["username"]
        hash_value = requests.POST["hashValue"]
        print(username)
        print(hash_value)
        # 查询数据库
        login_info = UserLogin.objects.filter(username=username).values("encrypt_value", "salt")
        login_info_list = list(login_info)

        # 判断是否能查询到该账号
        if len(login_info_list) == 0:
            return_json = {"status": "failed", "msg": "账号或密码错误，请仔细检查！"}
        else:
            # 取得加密后字符串和盐
            encrypt_value = login_info_list[0]["encrypt_value"]
            salt = login_info_list[0]["salt"]

            # 将得到的hash_value加盐后sha1加密跟服务器端密文进行比对
            value = Utils.encrypt_by_sha1(hash_value + salt)
            print("hash_value:" + hash_value)
            print("encrypt_value:" + encrypt_value)
            print("salt:" + salt)
            print("value:" + value)
            if value == encrypt_value:
                user_info = UserInfo.objects.filter(username=username).values("nickname", "head_image")
                user_info_list = list(user_info)
                nickname = user_info_list[0]["nickname"]
                head_image = user_info_list[0]["head_image"]
                return_json = {"status": "success", "msg": {"nickname": nickname, "head_image": head_image}}
            else:
                return_json = {"status": "failed", "msg": "账号或密码错误，请仔细检查！"}
        return JsonResponse(return_json)


def forget_password(requests):
    if requests.method == "GET":
        e_mail = requests.GET.get("e-mail", "")
        username = requests.GET["username"]
        user_info = UserInfo.objects.filter(username=username).values("e_mail")
        user_info_list = list(user_info)

        #  找不到该邮箱
        if len(user_info_list) == 0:
            return_json = {"status": "failed", "msg": "邮箱与账号不匹配！"}
        else:
            database_mail = user_info_list[0]["e_mail"]
            if database_mail == e_mail:
                random_string = Utils.get_random_string(6)
                Utils.send_forget_emails(random_string, e_mail)
                return_json = {"status": "success", "msg": {"random_string": random_string}}
            else:
                return_json = {"status": "failed", "msg": "邮箱与账号不匹配！"}
        return JsonResponse(return_json)
    elif requests.method == "POST":
        username = requests.POST["username"]
        hash_value = requests.POST["hashValue"]
        salt = requests.POST["salt"]

        #  返回信息
        return_json = {}
        #  存入数据库
        try:
            # 将得到的密文和salt拼接进行sha1加密
            encrypt_value = Utils.encrypt_by_sha1(hash_value + salt)
            user_dict = {"username": username, "encrypt_value": encrypt_value, "salt": salt}
            UserLogin.objects.create(**user_dict)

            return_json = {"status": "success", "msg": "修改密码成功，请重新登录！"}
        except Exception as e:
            error_msg = traceback.format_exc()
            Utils.send_error(error_msg)
            return_json = {"status": "failed", "msg": "服务器出现异常，管理员小哥哥正在排查..."}
        finally:
            return JsonResponse(return_json)


def query_user_info(requests):
    if requests.method == "GET":
        username = requests.GET["username"]
        info = UserInfo.objects.filter(username=username).values("nickname", "head_image")
        info_list = list(info)
        if len(info_list) == 0:
            return_json = {"status": "failed", "msg": "没有查询到这个账号哦！"}
        else:
            nickname = info_list[0]["nickname"]
            head_image = info_list[0]["head_image"]
            return_json = {"status": "success", "msg": {"nickname": nickname, "head_image": head_image}}
        return JsonResponse(return_json)


def friends(requests):
    if requests.method == "GET":
        kind = requests.GET["kind"]
        #  请求添加好友
        if kind == "1":
            my_account = requests.GET["my_account"]
            his_account = requests.GET["his_account"]
            len1 = len(list(Relationship.objects.filter(user1=my_account, user2=his_account).values("user2")))
            len2 = len(list(Relationship.objects.filter(user1=his_account, user2=my_account).values("user2")))
            if len1 != 0 or len2 != 0:
                return_json = {"status": "failed", "msg": "已经添加过了哦！"}
            else:
                try:
                    Relationship.objects.create(user1=my_account, user2=his_account)
                    return_json = {"status": "success", "msg": "添加成功！"}
                except Exception as e:
                    error_msg = traceback.format_exc()
                    Utils.send_error(error_msg)
                    return_json = {"status": "failed", "msg": "添加失败, 管理员小哥哥正在排查哦..."}
            return JsonResponse(return_json)
        elif kind == "2":
            my_account = requests.GET["my_account"]
            account_list = []

            account1_list = list(Relationship.objects.filter(user1=my_account).values("user2"))
            for account_object1 in account1_list:
                account1 = account_object1["user2"]
                account_list.append(account1)

            account2_list = list(Relationship.objects.filter(user2=my_account).values("user1"))
            for account_object2 in account2_list:
                account2 = account_object2["user1"]
                account_list.append(account2)

            return_json = {"status": "success", "msg": account_list}
            return JsonResponse(return_json)