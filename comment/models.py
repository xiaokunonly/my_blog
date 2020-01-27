from django.db import models
from django.contrib.auth.models import User
from ckeditor.fields import RichTextField
# Create your models here.
from article.models import ArticlePost
#django-mptt
from mptt.models import MPTTModel,TreeForeignKey
class Comment(MPTTModel):
    article=models.ForeignKey(
        ArticlePost,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    user=models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    body=RichTextField()
    #树形结构
    parent=TreeForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children'
    )
    #记录被回复者，即二级评论回复给谁
    reply_to=models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='replyers',
    )
    created=models.DateTimeField(auto_now_add=True)
    class MPTTMeta:
        order_insertion_by=['created']
    def __str__(self):
        return self.body[:20]