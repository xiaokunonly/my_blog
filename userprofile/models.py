from django.db import models
from django.contrib.auth.models import User
#引入内置信号
from django.db.models.signals import post_save
#引入信号接收器的装饰器
from django.dispatch import receiver
# Create your models here.

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')
    phone=models.CharField(max_length=20,blank=True)
    # 头像
    avatar=models.ImageField(upload_to='avatar/%Y%m%d/',blank=True)
    #个人简介
    bio=models.TextField(max_length=500,blank=True)
    def __str__(self):
        return 'user{}'.format(self.user.username)

# #通过信号传递机制，每当User创建/更新时，Profile也会自动的创建/更新
# #信号接收函数，每当新建User实例时自动调用
# @receiver(post_save,sender=User)
# def create_user_profile(sender,instance,created,**kwargs):
#     if created:
#         Profile.objects.create(user=instance)
#
# #信号接收函数，每单更新User实例时自动调用
# @receiver(post_save,sender=User)
# def save_user_profile(sender,instance,**kwargs):
#     instance.profile.save()