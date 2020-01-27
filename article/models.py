from django.db import models
from django.urls import reverse
# Create your models here.
#导入内建的Usermoxing
from django.contrib.auth.models import User
#timezone用于处理时间相关事务
from django.utils import timezone
#标签
from taggit.managers import TaggableManager
#pillow
from PIL import Image
#栏目类
class ArticleColumn(models.Model):
    title=models.CharField(max_length=100,blank=True)
    created=models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.title
#博客文章数据模型
class ArticlePost(models.Model):
    author=models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    body=models.TextField()
    created=models.DateTimeField(default=timezone.now)
    updated=models.DateTimeField(auto_now=True)
    total_views=models.PositiveIntegerField(default=0)
    column=models.ForeignKey(ArticleColumn,null=True,blank=True,on_delete=models.CASCADE,related_name='article')
    tags=TaggableManager(blank=True)
    avatar=models.ImageField(upload_to='article/%Y%m%d/',blank=True)
    likes=models.PositiveIntegerField(default=0)
    class Meta:
        # ordering指定模型返回的数据的排列顺序
        # '-created'表明数据应倒序排列
        ordering=('-created',)
    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('article:article_detail',args=[self.id])
    def save(self,*args,**kwargs):
        article=super(ArticlePost,self).save(*args,**kwargs)
        if self.avatar and not kwargs.get('update_fields'):
            image = Image.open(self.avatar)
            (x,y)=image.size
            new_x=400
            new_y=int(new_x*(y/x))
            resized_image=image.resize((new_x,new_y),Image.ANTIALIAS)
            resized_image.save(self.avatar.path)
        return article





