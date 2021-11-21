from django.http.response import HttpResponse
from django.shortcuts import render,redirect
from blog.models import Post,BlogComment
from django.contrib import messages
from blog.templatetags import extras

# Create your views here.
def blogHome(request):
    allPosts = Post.objects.all() 
    context={'allPosts':allPosts}
    return render(request,'blog/blogHome.html',context)
    #return HttpResponse("This is Home of the blogs")

def blogPost(request,slug):
    post = Post.objects.filter(slug=slug).first()
    post.views=post.views+1
    post.save()

    comments=BlogComment.objects.filter(post=post,parent=None)
    replies=BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)

    context={'post':post,'comments':comments,'user':request.user,'replyDict':replyDict}
    return render(request,'blog/blogPost.html',context)

def postComment(request):   
    if request.method=="POST":
        comment = request.POST.get("comment")
        user=request.user
        postSno=request.POST.get("postSno")
        post = Post.objects.get(sno=postSno)
        parentSno=request.POST.get("parentSno")
        if parentSno=="":
            comment=BlogComment(comment=comment,user=user,post=post)
            messages.success(request,"Comment Posted Successfully")
            comment.save()
        else:
            parent=BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment=comment,user=user,post=post,parent=parent)
            messages.success(request,"Reply Posted Successfully")
            comment.save()
        
        
    return redirect(f"/blog/{post.slug}")