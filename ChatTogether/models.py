from django.db import models


class UserLogin(models.Model):
    username = models.CharField(db_column='Username', verbose_name='Username', max_length=16)
    encrypt_value = models.CharField(db_column='Encrypt_value', max_length=200, verbose_name='Encrypt_value')
    salt = models.CharField(db_column='Salt', max_length=20, verbose_name='Salt')


class UserInfo(models.Model):
    username = models.CharField(db_column='Username', verbose_name='Username', max_length=16)
    e_mail = models.CharField(db_column='E-mail', max_length=50, verbose_name='E-mail')
    nickname = models.CharField(db_column='Nickname', max_length=20, verbose_name='Nickname')
    head_image = models.CharField(db_column='Head_image', max_length=100, verbose_name='Head_image')


class Relationship(models.Model):
    user1 = models.CharField(db_column='User1', verbose_name='User1', max_length=16)
    user2 = models.CharField(db_column='User2', verbose_name='User2', max_length=16)