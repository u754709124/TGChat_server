from qiniu import Auth


# 上传到七牛后保存的文件名
def get_upload_token(filename):
    # 需要填写你的 Access Key 和 Secret Key
    access_key = ''
    secret_key = ''
    # 构建鉴权对象
    q = Auth(access_key, secret_key)
    # 要上传的空间
    bucket_name = 'tgchat'

    # 生成上传 Token，可以指定过期时间等
    # 3600为token过期时间，秒为单位。3600等于一小时
    token = q.upload_token(bucket_name, filename, 60)
    return token
