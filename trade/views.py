from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post, Chatting, ChatRoom
from .forms import PostForm
from users.models import User

def trade_first(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'trade/trade_first.html', {'posts': posts})

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
    return render(request, 'trade/trade_detail.html', {'post': post})

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
            form.save()
            return redirect('trade:trade_detail', pk=pk)
    else:
        form = PostForm(instance=post)

    return render(request, 'trade/trade_write.html', {'form': form})
  
def chat(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 처음 열었을 경우는 저장, 아니면 그냥 값 들고옴 
    chat_room, created=ChatRoom.objects.get_or_create(
        buyer=request.user,
        seller=post.author,
        post=post
    )
    return redirect('trade:chating',pk, chat_room.id)


def chat(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # 처음 열었을 경우는 저장, 아니면 그냥 값 들고옴 
    chat_room, created = ChatRoom.objects.get_or_create(
        buyer=request.user,
        seller=post.author,
        post=post
    )
    return redirect('trade:chating', pk, chat_room.id)

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

def seller_chat(request):
    chat_room=ChatRoom.objects.filter(seller=request.user)
    return render(request, 'trade/seller_chat.html',{'chat_room':chat_room})


    return render(request, 'trade/trade_chat.html', {'post': post})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.user in post.likes.all():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect('trade:trade_detail', pk=pk)

def liked_posts(request):
    # 현재 로그인한 사용자가 찜한 글들을 가져옴
    liked_posts = request.user.liked_posts.all()
    return render(request, 'trade/liked_posts.html', {'liked_posts': liked_posts})
