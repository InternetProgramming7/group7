from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Chatting, ChatRoom, Review
from .forms import PostForm, ReviewForm
from users.models import User

def trade_require(request):
    posts = Post.objects.filter(allowed_reviewer__isnull=True).order_by('-created_at')
    return render(request, 'trade/trade_first.html', {'posts': posts})

def trade_finish(request):
    posts = Post.objects.filter(allowed_reviewer__isnull=False).order_by('-created_at')
    return render(request, 'trade/trade_finish.html', {'posts': posts})

def create(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('trade:trade')
    else:
        form = PostForm()
    return render(request, 'trade/trade_write.html', {'form': form})

def trade_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    find_review=Review.objects.filter(post=post,reviewer=request.user )

    # 이미 후기가 존재한다면 후기를 남기지 못하도록 한정
    review_exists = find_review.exists()
    return render(request, 'trade/trade_detail.html', {'post': post,'review_exists':review_exists})

def delete_post(request, pk):
    record=get_object_or_404(Post, pk=pk)
    record.delete()
    return redirect('trade:trade')

def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    # 현재 사용자가 글의 작성자인지 확인
    if request.user != post.author:
        return render(request, '403.html', status=403)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            allowed_reviewer_text = form.cleaned_data.get('allowed_reviewer_text')
            # admin(슈퍼유저) 계정이 nickname이 없어서 admin은 제외하도록 필터링함 
            post.allowed_reviewer=User.objects.filter(nickname=allowed_reviewer_text).exclude(nickname='admin').first()
            form.save()
            return redirect('trade:trade_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'trade/trade_write.html', {'form': form})

def create_review(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
   

    if request.method == 'POST':
        form = ReviewForm(request.POST)
                
        if form.is_valid():
            review = form.save(commit=False)
            review.post = post
            review.reviewer = request.user
            # 전체 리뷰 수 증가
            post.author.review_count+=1

            post.author.save()
            # 평점 계산
            post.author.grade=(post.author.grade*(post.author.review_count-1)+review.rating)/post.author.review_count
            review.save()
            post.author.save()
            return redirect('trade:trade_detail', pk=post_id)
    else:
        form = ReviewForm()

    return render(request, 'trade/review.html', {'form': form,'post':post})

def chat(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 처음 열었을 경우는 저장, 아니면 그냥 값 들고옴 
    chat_room, created=ChatRoom.objects.get_or_create(
        buyer=request.user,
        seller=post.author,
        post=post
    )
    return redirect('trade:chating',pk, chat_room.id)


def chat(request, post_id):
    post=get_object_or_404(Post, pk=post_id)
    # 처음 열었을 경우는 저장, 아니면 그냥 값 들고옴 
    chat_room, created = ChatRoom.objects.get_or_create(
        buyer=request.user,
        seller=post.author,
        post=post
    )
    return redirect('trade:chating', post_id, chat_room.id)

# 채팅방으로 들어감
def into_chatroom(request, post_id, chatroom_id):
    chat_room=get_object_or_404(ChatRoom, id=chatroom_id)

    if request.method == "POST":
        text = request.POST['text']
        Chatting.objects.create(
            text=text,
            chat_room=chat_room,
            writer=request.user
        )
        return redirect('trade:chating', post_id=post_id, chatroom_id=chatroom_id)

    chats=Chatting.objects.filter(chat_room=chat_room)
    return render(request, 'trade/chat.html', {'chats': chats})

# 판매자가 채팅 조회
def seller_chat(request):
    chat_room=ChatRoom.objects.filter(seller=request.user)
    return render(request, 'trade/seller_chat.html',{'chat_room':chat_room})


    return render(request, 'trade/trade_chat.html', {'post': post})

# 찜하기 
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('trade:trade_detail', pk=pk)

def liked_posts(request):
    liked_posts = request.user.liked_posts.all()
    return render(request, 'trade/liked_posts.html', {'liked_posts': liked_posts})
