from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Comment, Delivery
from .forms import PostForm, CommentForm, PostDelivery
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def community_main(request):
    return render(request,'community/community_main.html')
def delivery(request):
    delivery_posts = Delivery.objects.all().order_by('-created_at')
    paginator = Paginator(delivery_posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 번째 페이지를 반환합니다.
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지를 반환합니다.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'community/delivery.html', {'posts': posts})

def food(request):
    all_posts = Post.objects.all().order_by('-created_at')
    paginator = Paginator(all_posts, 5)
    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우, 첫 번째 페이지를 반환합니다.
        posts = paginator.page(1)
    except EmptyPage:
        # 페이지가 비어 있는 경우, 마지막 페이지를 반환합니다.
        posts = paginator.page(paginator.num_pages)
    return render(request, 'community/food.html', {'posts': posts})
'''
class FoodListView(ListView):
    model=Post
    template_name='community/food,html'
    context_objects_name='posts'
    paginate_by=5
    ordering=['-created_at']
'''

def category_posts(request, category):
    posts = Post.objects.filter(category=category).order_by('-created_at')

    return render(request, 'community/category_posts.html',{'posts':posts,'category':category})

def category_delivery(request, category_delivery):
    posts = Post.objects.filter(category=category_delivery).order_by('-created_at')

    return render(request, 'community/category_delivery.html',{'posts':posts,'category_delivery':category_delivery})


#def food_post(request):
#    posts=Post.objects.all()
#    return render(request,'community/food.html',{'posts':posts})
#def delivery_post(request):
#    posts=Post.objects.all()
#    return render(request, 'community/delivery.html',{'posts':posts})

def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, user=request.user)
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            return redirect('community:food')
    else:
        form = PostForm(user=request.user)
    return render(request, 'community/create_post.html', {'form': form})

def delivery_post(request):
    if request.method == 'POST':
        delivery_form = PostDelivery(request.POST)
        if delivery_form.is_valid():
            delivery_form.instance.author = request.user
            delivery_form.save()
            return redirect('community:delivery')
    else:
        delivery_form = PostDelivery(user=request.user)
    return render(request, 'community/delivery_post.html', {'delivery_form': delivery_form})

def delete_post(request,pk):
    post=get_object_or_404(Post,pk=pk)

    if request.user==post.author:
        post.delete()

    return redirect('community:food')

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user != post.author:
        return redirect('community:food-detail', pk=post.pk)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('community:food-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'community/edit_post.html', {'form': form, 'post':post})

def edit_delivery(request, pk):
    post = get_object_or_404(Delivery, pk=pk)

    if request.user != post.author:
        return redirect('community:delivery-detail', pk=post.pk)

    if request.method == 'POST':
        delivery_form = PostDelivery(request.POST, instance=post)
        if delivery_form.is_valid():
            delivery_form.save()
            return redirect('community:delivery-detail', pk=post.pk)
    else:
        delivery_form = PostDelivery(instance=post)

    return render(request, 'community/edit_delivery.html', {'delivery_form': delivery_form, 'post':post})


def food_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'community/food_detail.html', {'post': post})

def delivery_detail(request,pk):
    post=get_object_or_404(Post, pk=pk)
    return render(request, 'community/delivery_detail.html',{'post':post})

def ott(request):
    return render(request, 'community/ott.html')

def search(request):
    query=request.GET.get('q')

    if query:
        posts=Post.objects.filter(title__icontains=query)
    else:
        if query:
            posts = Post.objects.filter(content__icontains=query)
        else:
            posts = []
    return render(request,'community/search_results.html',{'posts':posts, 'query':query})

def search_delivery(request):
    query=request.GET.get('q')

    if query:
        posts=Delivery.objects.filter(title__icontains=query)
    else:
        if query:
            posts = Delivery.objects.filter(content__icontains=query)
        else:
            posts = []
    return render(request,'community/search_delivery.html',{'posts':posts, 'query':query})


def comment(request, pk):
    post=get_object_or_404(Post, pk=pk)
    comments=Comment.objects.filter(post=post)

    if request.method=='POST':
        comment_form=CommentForm(request.POST)
        if comment_form.is_valid():
            new_comment=comment_form.save(commit=False)
            new_comment.post=post
            new_comment.author=request.user
            new_comment.save()
            return redirect('community:food-detail', pk=pk)
        else:
            comment_form=CommentForm()
        return render(request, 'community/food_detail.html',{'post': post, 'comments':comments, 'comment_form':comment_form})


#class PostList(ListView):
#    model = Post
#    ordering = '-created_at'

#class PostDetail(DetailView):
#    model = Post