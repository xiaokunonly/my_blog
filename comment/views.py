from django.shortcuts import render,get_object_or_404,redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from .forms import CommentForm
from .models import Comment
from notifications.signals import notify
from django.contrib.auth.models import User
# Create your views here.
from article.models import ArticlePost
from django.http import JsonResponse
@login_required(login_url='/userprofile/login/')
def post_comment(request,article_id,parent_comment_id=None):
    article=get_object_or_404(ArticlePost,id=article_id)
    #处理post请求
    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.article=article
            new_comment.user=request.user
            # 二级回复
            if parent_comment_id:
                parent_comment=Comment.objects.get(id=parent_comment_id)
                #若回复层级超过二级，则转换为二级
                new_comment.parent_id=parent_comment.get_root().id
                #被回复人
                new_comment.reply_to=parent_comment.user
                new_comment.save()

                #二级评论
                if parent_comment.user==request.user:
                    if parent_comment.user.is_superuser:
                        if parent_comment.user!=article.author:
                            notify.send(
                                request.user,
                                recipient=article.author,
                                verb='回复了'+str(parent_comment.user),
                                target=article,
                                action_object=new_comment,
                            )
                    if not parent_comment.user.is_superuser:
                        if article.author.is_superuser:
                            notify.send(
                                request.user,
                                recipient=User.objects.filter(is_superuser=1),
                                verb='回复了' + str(parent_comment.user),
                                target=article,
                                action_object=new_comment,
                            )
                        else:
                            if article.author==parent_comment.user:
                                notify.send(
                                    request.user,
                                    recipient=User.objects.filter(is_superuser=1),
                                    verb='回复了' + str(parent_comment.user),
                                    target=article,
                                    action_object=new_comment,
                                )
                            else:
                                notify.send(
                                    request.user,
                                    recipient=[User.objects.filter(is_superuser=1),article.author],
                                    verb='回复了' + str(parent_comment.user),
                                    target=article,
                                    action_object=new_comment,
                                )
                else:
                    if parent_comment.user.is_superuser:
                        if parent_comment.user==article.author:
                            notify.send(
                                request.user,
                                recipient=User.objects.filter(is_superuser=1),
                                verb='回复了你' ,
                                target=article,
                                action_object=new_comment,
                            )
                        else:
                            if request.user==article.author:
                                notify.send(
                                    request.user,
                                    recipient=parent_comment.user,
                                    verb='回复了你',
                                    target=article,
                                    action_object=new_comment,
                                )
                            else:
                                notify.send(
                                    request.user,
                                    recipient=parent_comment.user,
                                    verb='回复了你',
                                    target=article,
                                    action_object=new_comment,
                                )
                                notify.send(
                                    request.user,
                                    recipient=article.author,
                                    verb='回复了'+str(parent_comment.user),
                                    target=article,
                                    action_object=new_comment,
                                )
                    else:
                        if parent_comment.user==article.author:
                            if request.user.is_superuser:
                                notify.send(
                                    request.user,
                                    recipient=parent_comment.user,
                                    verb='回复了你',
                                    target=article,
                                    action_object=new_comment,
                                )
                            else:
                                notify.send(
                                    request.user,
                                    recipient=parent_comment.user,
                                    verb='回复了你',
                                    target=article,
                                    action_object=new_comment,
                                )
                                notify.send(
                                    request.user,
                                    recipient=User.objects.filter(is_superuser=1),
                                    verb='回复了'+str(parent_comment.user),
                                    target=article,
                                    action_object=new_comment,
                                )
                        else:
                            if request.user.is_superuser:
                                if request.user==article.author:
                                    notify.send(
                                        request.user,
                                        recipient=parent_comment.user,
                                        verb='回复了你',
                                        target=article,
                                        action_object=new_comment,
                                    )
                                else:
                                    notify.send(
                                        request.user,
                                        recipient=parent_comment.user,
                                        verb='回复了你',
                                        target=article,
                                        action_object=new_comment,
                                    )
                                    notify.send(
                                        request.user,
                                        recipient=article.author,
                                        verb='回复了'+str(parent_comment.user),
                                        target=article,
                                        action_object=new_comment,
                                    )
                            else:
                                if article.author==request.user or article.author.is_superuser:
                                    notify.send(
                                        request.user,
                                        recipient=parent_comment.user,
                                        verb='回复了你',
                                        target=article,
                                        action_object=new_comment,
                                    )
                                    notify.send(
                                        request.user,
                                        recipient=User.objects.filter(is_superuser=1),
                                        verb='回复了' + str(parent_comment.user),
                                        target=article,
                                        action_object=new_comment,
                                    )
                                else:
                                    notify.send(
                                        request.user,
                                        recipient=parent_comment.user,
                                        verb='回复了你',
                                        target=article,
                                        action_object=new_comment,
                                    )
                                    notify.send(
                                        request.user,
                                        recipient=User.objects.filter(is_superuser=1),
                                        verb='回复了' + str(parent_comment.user),
                                        target=article,
                                        action_object=new_comment,
                                    )
                                    notify.send(
                                        request.user,
                                        recipient=article.author,
                                        verb='回复了' + str(parent_comment.user),
                                        target=article,
                                        action_object=new_comment,
                                    )
                #return HttpResponse('200 OK')
                return JsonResponse({"code":"200 OK","new_comment_id":new_comment.id})
            new_comment.save()
            #一级评论，如果文章作者和请求用户不同，则针对文章作者是不是超级用户做不同通知
            if request.user != article.author:
                #如果文章作者不是超级用户，分别给文章作者和超级用户发送不同通知
                if not article.author.is_superuser:
                    notify.send(
                        request.user,
                        recipient=article.author,
                        verb='评论了你',
                        target=article,
                        action_object=new_comment,
                    )
                    #如果评论者不是超级用户，才给超级用户发通知。
                    if not request.user.is_superuser:
                        notify.send(
                            request.user,
                            recipient=User.objects.filter(is_superuser=1),
                            verb='评论了'+str(article.author),
                            target=article,
                            action_object=new_comment,
                        )
                else:
                    notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='评论了你',
                        target=article,
                        action_object=new_comment,
                    )
            #如果评论者和文章作者一致，若不是管理员，则也通知管理员。
            else:
                if not request.user.is_superuser:
                    notify.send(
                        request.user,
                        recipient=User.objects.filter(is_superuser=1),
                        verb='评论了' + str(article.author),
                        target=article,
                        action_object=new_comment,
                    )
            redirect_url=article.get_absolute_url()+'#comment_elem_'+str(new_comment.id)
            return redirect(redirect_url)
        else:
            return HttpResponse('表单内容有误，请重新填写')
    elif request.method=='GET':
        comment_form=CommentForm()
        context={
            'comment_form':comment_form,
            'article_id':article_id,
            'parent_comment_id':parent_comment_id
        }
        return render(request,'comment/reply.html',context)
    else:
        return HttpResponse('仅接受GET/POST请求')