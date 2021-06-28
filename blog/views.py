from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from .models import Post, BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.

def blogHome(request):
    allposts = Post.objects.all()
    context = {'allposts' : allposts}
    return render(request, 'blog/blogHome.html', context)


def blogPost(request, slug):
    post = Post.objects.filter(slugs=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    repDict={}
    for reply in replies:
        if reply.parent.sno not in repDict.keys():
            repDict[reply.parent.sno] = [reply]
        else:
            repDict[reply.parent.sno].append(reply)
    context = {'post': post, 'comments':comments, 'user': request.user, 'repDict':repDict}
    return render(request, 'blog/blogPost.html', context)

# API for comments
def postComment(request):
    if request.method=='POST':
        comment = request.POST.get("comment")
        user = request.user
        postSno = request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno = request.POST.get("parentSno")
        if parentSno=="":
            comment = BlogComment(comment=comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your message has been posted successfully")
        else:
            parent = BlogComment.objects.get(sno=parentSno)
            comment = BlogComment(comment=comment, user=user, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your Reply has been posted successfully")

    return redirect(f"/blog/{post.slugs}")