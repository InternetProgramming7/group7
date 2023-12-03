from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .forms import  SignUpForm
from trade.models import *
from community.models import  Delivery
from community.models import Post as CommunityPost
# 회원가입
def signup_view(request):
    if request.method == "GET":
        form = SignUpForm()
        context = {'form': form}
        return render(request, 'accounts/signup.html', context)
    form = SignUpForm(request.POST, request.FILES)
    # 유효한 내용인지 확인
    if form.is_valid():
        user = form.save()
        return redirect('main')
    else:
        return render(request, 'accounts/signup.html', {'form': form})

# 로그인
def login_view(request):
    if request.method=="GET":
        return render(request, 'accounts/login.html', {'form':AuthenticationForm})
    form=AuthenticationForm(request, data=request.POST)
    if form.is_valid():
        login(request, form.user_cache)
        return redirect('main')
    return render(request, 'accounts/login.html',{'form':form})

# 로그아웃
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect('main')

# 마이페이지
def mypage(request):
    return render(request, 'accounts/mypage.html')

def review_make(request):
    posts=Post.objects.filter(allowed_reviewer=request.user).order_by('-id')
    return render(request, 'accounts/review_list.html',{'posts':posts})

# 유저 정보 수정
def update_userinfo(request):
    if request.method=="POST":
        nickname=request.POST.get('nickname')
        email=request.POST.get('email')
        new_profile=request.FILES.get('profile')
        if new_profile:
            request.user.profile.delete()
            request.user.profile=new_profile
        request.user.nickname=nickname
        request.user.email=email
        request.user.save()
        return redirect('accounts:mypage')
    return render(request, 'accounts/update_userinfo.html')

# 혜택1 스크랩
def benefit_scrap(request):
    benefits=request.user.scrap_benefits.all()
    context = {
        'benefits': benefits
    }
    return render(request, 'accounts/benefit_scrap.html', context)

# 혜택 2 스크랩
def map_scrap(request):
    maps=request.user.map_benefits.all()
    context={
        'maps':maps
    }
    return render(request, 'accounts/map_scrap.html', context)

# 내가 올린 중고거래
def my_trade(request):
    trades=Post.objects.filter(author=request.user)
    context={
        'trades':trades
    }
    return render(request, 'accounts/my_trade.html',context)

def my_trade_detail(request, post_id):
    post=get_object_or_404(Post, id=post_id)
    context={
        'post':post
    }
    return render(request, 'accounts/trade_detail.html',context)

# 해당하는 중고거래에서 생긴 채팅방 조회
def seller_chat(request, post_id):
    chat_room=ChatRoom.objects.filter(post=post_id, seller=request.user)
    return render(request, 'accounts/seller_chat.html',{'chat_room':chat_room})

# 진행중인 채팅방 
def proceeding_chat(request):
    chat_room=ChatRoom.objects.filter( buyer=request.user)
    return render(request,'accounts/buyer_chat.html',{'chat_room':chat_room} )

# 채팅 나가기
def leave_chat_room(request, room_id):
    chat_room=ChatRoom.objects.filter(id=room_id)
    chat_room.delete()
    return redirect('accounts:proceeding-chat')

# 커뮤니티 음식
def my_post_food(request):
    posts=CommunityPost.objects.filter( author=request.user).order_by('-id')
    return render(request, 'accounts/my_food.html',{'posts':posts})

# 커뮤니티 ott
def my_post_ott(request):
    posts=Delivery.objects.filter( author=request.user).order_by('-id')
    return render(request, 'accounts/my_ott.html',{'posts':posts})