#引入redirect重定向模块
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.views import View

from .models import ArticlePost
from .forms import ArticlePostForm
from comment.models import Comment
from .models import ArticleColumn
#引入User模型
from django.contrib.auth.models import User
#登录装饰器
from django.contrib.auth.decorators import login_required
#分页模块
from django.core.paginator import Paginator
#引入Q对象
from django.db.models import Q
#引入评论表单
from comment.forms import CommentForm
import markdown
from markdown.extensions import Extension
# Create your views here.
#视图函数
def article_list(request):
    search=request.GET.get('search')
    order=request.GET.get('order')
    column=request.GET.get('column')
    tag=request.GET.get('tag')
    #初始化查询集
    article_list=ArticlePost.objects.all()
    columns=ArticleColumn.objects.all()
    if search:
        #用Q对象进行联合搜索
        article_list=article_list.filter(
            Q(title__icontains=search)|
            Q(body__icontains=search)
         )
    else:
        search=''
    if column is not None and column.isdigit():
        article_list=article_list.filter(column=column)
    if tag and tag!='None':
        article_list=article_list.filter(tags__name__in=[tag])
    if order=='total_views':
        article_list=article_list.order_by('-total_views')
#分页
    paginator=Paginator(article_list,3)
    page=request.GET.get('page')
    articles=paginator.get_page(page)
    context={'articles':articles,'order':order,'search':search,'column':column,'tag':tag,'columns':columns}
    return render(request,'article/list.html',context)
#文章详情
def article_detail(request,id):
    article = ArticlePost.objects.get(id=id)
    comments=Comment.objects.filter(article_id=id)
    comment_form=CommentForm()
    # 包含 缩写、表格等常用扩展   #语法高亮显示
    md=markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    article.body=md.convert(article.body)
    # article.body=markdown.markdown(article.body,extensions=['markdown.extensions.extra',
    #                                                         'markdown.extensions.highlight',
    #                                                         'markdown.extensions.toc',])
    article.total_views+=1
    article.save(update_fields=['total_views'])
    pre_article=ArticlePost.objects.filter(id__lt=article.id).order_by('-id')
    next_article=ArticlePost.objects.filter(id__gt=article.id).order_by('id')
    if pre_article.count()>0:
        pre_article=pre_article[0]
    else:
        pre_article=None
    if next_article.count()>0:
        next_article=next_article[0]
    else:
        next_article=None
    context={'article': article,'toc': md.toc,'comments':comments,
             'comment_form':comment_form,'pre_article':pre_article,'next_article':next_article}
    return render(request,'article/detail.html',context)

#写文章视图
@login_required(login_url='/userprofile/login/')
def article_create(request):
    #判断用户是否提交数据
    if request.method=='POST':
        #将提交的数据赋值到表单实例中
        article_post_form=ArticlePostForm(request.POST,request.FILES)
        #判断提交的数据是否满足模型的要求
        if article_post_form.is_valid():
            #保存数据，但暂时不提交到数据库中
            new_article=article_post_form.save(commit=False)
            new_article.author=User.objects.get(id=request.user.id)
            if request.POST['column'] != 'none':
                new_article.column = ArticleColumn.objects.get(id=request.POST['column'])
            new_article.save()
            article_post_form.save_m2m()
            return redirect("article:article_list")
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form=ArticlePostForm()
        columns=ArticleColumn.objects.all()
        context={'article_post_form': article_post_form,'columns':columns}
        return render(request,'article/create.html',context)

#删文章
@login_required(login_url='/userprofile/login/')
def article_safe_delete(request,id):
    if request.method=='POST':
        article=ArticlePost.objects.get(id=id)
        if request.user!=article.author:
            return HttpResponse('抱歉，你无权修改这篇文章！')
        article.delete()
        return redirect("article:article_list")
    else:
        return HttpResponse("仅允许post请求")

#更新文章
@login_required(login_url='/userprofile/login/')
def article_update(request,id):
    """
    更新文章的视图函数
    通过POST方法提交表单，更新title,body字段
    GET方法进入初始表单页面
    id：文章的id
    :param request:
    :param id:
    :return:
    """
    article=ArticlePost.objects.get(id=id)
    if request.method=="POST":
        if request.user!=article.author:
            return HttpResponse('你无权修改这篇文章！')
        article_post_form=ArticlePostForm(data=request.POST)
        if article_post_form.is_valid():
            article.title=request.POST['title']
            article.body=request.POST['body']
            if request.POST['column']!="none":
                article.column=ArticleColumn.objects.get(id=request.POST['column'])
            if request.FILES.get('avatar'):
                article.avatar=request.FILES.get('avatar')
            article.tags.set(*request.POST.get('tags').split(','),clear=True)
            article.save()
            return redirect("article:article_detail",id=id)
        else:
            return HttpResponse("表单内容有误，请重新填写")
    else:
        article_post_form=ArticlePostForm()
        columns=ArticleColumn.objects.all()
        tags=','.join([x for x in article.tags.names()] )
        context={"article":article,"article_post_form":article_post_form,"columns":columns,'tags':tags}
        return render(request,'article/update.html',context)

#点赞
class IncreaseLikesView(View):
    def post(self,request,*args,**kwargs):
        article=ArticlePost.objects.get(id=kwargs.get('id'))
        article.likes+=1
        article.save()
        return HttpResponse('success')