from django.contrib import admin
from .models import UserLogin, UserInfo, Relationship


class UserLoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'encrypt_value', 'salt')


admin.site.register(UserLogin, UserLoginAdmin)


class UserInfoAdmin(admin.ModelAdmin):
    list_display = ('username', 'e_mail', 'nickname', 'head_image')


admin.site.register(UserInfo, UserInfoAdmin)


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2')


admin.site.register(Relationship, RelationshipAdmin)