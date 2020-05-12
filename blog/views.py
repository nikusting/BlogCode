from django.http import HttpResponse
from django.shortcuts import render,get_object_or_404,redirect
from .models import Post,Category,Tag
import markdown
from comments.forms import CommentForm



def index(request):
    post_list = Post.objects.all().order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    post.body=markdown.markdown(post.body,
                                extensions=[
                                    'markdown.extensions.extra',
                                    'markdown.extensions.codehilite',
                                    'markdown.extensions.toc'
                                ])

    form=CommentForm()
    comment_list=post.comment_set.all()
    context={'post':post,
             'form':form,
             'comment_list':comment_list
             }

    return render(request, 'blog/detail.html', context=context)

def archives(request,year,month):
    post_list=Post.objects.filter(created_time__year=year,
                                  created_time__month=month
                                  ).order_by(('-created_time'))
    return  render(request,'blog/index.html',context={'post_list':post_list})

def category(request, pk):
    # 记得在开始部分导入 Category 类
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate).order_by('-created_time')
    return render(request, 'blog/index.html', context={'post_list': post_list})






