from django import forms
from .models import ArticlePost

#写文章的表单类
class ArticlePostForm(forms.ModelForm):
    class Meta:
        #指明数据模型来源
        model=ArticlePost
        fields=('title','body','tags','avatar')
