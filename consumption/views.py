from django.shortcuts import render, redirect, get_object_or_404
from datetime import datetime
from .models import Record
from users.models import *
from django.http import Http404
from django.views.generic import  DetailView
# Create your views here.

y = [n for n in range(2023, 1999, -1)] # 2023-부터 2000 year
m=[n for n in range(1,13)] # 1~12 month
d=[n for n in range(1,32)] # 1~31 day

# 입력받은 날짜(%m/%d/%Y)를 month, day, year로 분할 후 리턴
def parseTime(date): 
    m=date[0:2]
    d=date[3:5]
    if len(d)==1:
        d="0"+d
    y=date[6:10]
    return y,m,d

# 가장 많이 출현한 카테고리를 리턴, 여러개일 수 있으니 리스트로 리턴
def common_category(a,b,c,d,e,f):
    max_count=max(a, b, c, d, e)
    common_category_list=[]
    if max_count == a:
        common_category_list.append("음식")
    elif max_count == b:
        common_category_list.append("생필품")
    elif max_count == c:
        common_category_list.append("여가")
    elif max_count == d:
        common_category_list.append("교통")
    elif max_count == e:
        common_category_list.append("학습")
    elif max_count == e:
        common_category_list.append("기타")

    return common_category_list

# 금융 기록
def main_consumption(request, nickname):
    # like에서 처리한 후 다시 main_consumption으로 리다이렉트 할 때 최근에 조회했던 사용자를 조회하도록 해야 하므로 세션으로 처리함
    request.session['nickname'] = nickname
    # 조회하는 유저 확인
    user = User.objects.get(nickname=nickname)

    if request.method=="GET":
        try:
            # 세션에 입력되어 있는 값이 있는지 확인
            year=request.session['year']
            month=request.session['month']
            date=request.session['date']
        except:
            # 없다면 현재 시간으로 초기화
            today=datetime.today().strftime("%m/%d/%Y")
            year, month, date=parseTime(today)
    else:
        year=request.POST.get('year')
        month=request.POST.get('month')
        date=request.POST.get('date')
        request.session['year']=year
        request.session['month']=month
        request.session['date']=date

    records=Record.objects.filter(writer=user, year=year, month=month, date=date).order_by('category')
    category=["음식","생필품","여가","교통","학습","기타"]
    context={
        "find_y":year,
        "find_m":month,
        "find_d":date,
        "year":y,
        "month":m,
        "date":d,
        "records":records,
        "category":category,
        "nickname":nickname
    }
    return render(request, 'consumption/consumption.html', context)
        
# (알찬소 영수증) 금융 기록 조회
class consumption_detail(DetailView):
    model=Record

# 금융 기록 수정
def calender_update(request, id):
    record=get_object_or_404(Record, id=id)
    if request.method=="POST":
        full_date=request.POST.get('full_date')
        price=request.POST.get('price')
        name=request.POST.get('name')
        category=request.POST.get('category')
        purpose=request.POST.get('purpose')
        share=request.POST.get('share')
        detail=request.POST.get('detail')
        share = request.POST.get('share') == "True"
        year, month, date=parseTime(full_date)
        record.year=year
        record.month=month
        record.date=date
        record.price=price
        record.name=name
        record.category=category
        record.purpose=purpose
        record.share=share
        record.detail=detail
        record.writer=request.user
        record.save()
        return redirect('consumption:consumption', request.user.nickname)
    else:
        return render(request, 'consumption/calener_update.html',{"record":record})

# 금융 기록 작성
def calender(request):
    if request.method=="GET":
        # 기본적으로 오늘이 등록되도록 
        today=datetime.today().strftime("%m/%d/%Y")
        context={
            'today':today
        }

        return render(request, 'consumption/calender.html',context)
    # 폼에 등록되어 있는 정보 가져옴 
    else:
        full_date=request.POST.get('full_date')
        price=request.POST.get('price')
        name=request.POST.get('name')
        category=request.POST.get('category')
        purpose=request.POST.get('purpose')
        share=request.POST.get('share')
        detail=request.POST.get('detail')
        share = request.POST.get('share') == "True"
        year, month, date=parseTime(full_date)
        # Record 객체 생성 
        Record.objects.create(
            year=year,
            month=month,
            date=date,
            price=price,
            name=name,
            category=category,
            purpose=purpose,
            share=share,
            detail=detail,
            writer=request.user
        )
        return redirect('consumption:consumption', request.user.nickname)

# 금융 기록 삭제 
def delete(request, id):
    record=get_object_or_404(Record, id=id)
    record.delete()
    return redirect('consumption:consumption', request.user.nickname)

# 팔로잉한 친구 조회 
def friend(request):
    following=request.user.following.all()
    following_array=[n.following for n in following]

    context={
        "following":following_array,
    }
    return render(request, 'consumption/friend.html', context)

# 친구 조회 (닉네임 or 아이디)
def search_friend(request):
    if request.method=="POST":
        search=request.POST.get("search")
        # 친구 팔로우 해도 검색 상태가 유지되도록 세션에 넣음 
        request.session['search'] = search
        # 닉네임으로 검색 1
        users=User.objects.filter(nickname__contains=search)
        # 닉네임으로 검색해도 나오지 않으면 아이디로 검색
        if not users:
            users=User.objects.filter(username__contains=search)
    else:
        try:
            users=User.objects.filter(nickname__contains=request.session['search'])
        except:
            users=None
    # 현재 유저가 팔로잉한 유저 객체를 모두 리턴 
    following=request.user.following.all() 
    # 유저 객체 중 객체들의 username만 리턴 
    following_nickname_array=[n.following.nickname for n in following]
    context={
        "following":following_nickname_array,
        "users":users
    }
    return render(request, 'consumption/search_friend.html', context)

# 팔로우
def follow(request, nickname):
    following=User.objects.get(nickname=nickname)
    Follow.objects.create(follower=request.user, following=following)
    return redirect("consumption:search-friend")

# 언팔로우
def unfollow(request,nickname):
    unfollowing=User.objects.get(nickname=nickname)
    relation=Follow.objects.filter(follower=request.user, following=unfollowing)
    relation.delete()
    return redirect("consumption:search-friend")

# 금융기록 좋아요
def like(request, id):
    record=get_object_or_404(Record, id=id)
    # 레코드 객체의 좋아요에 사용자가 없는경우 -> 좋아요를 누르도록 처리해야 함
    if request.user not in record.like_user.all():
        record.like_user.add(request.user)
        record.likes+=1
    # 레코드 객체의 좋아요에 사용자가 있는경우 -> 좋아요를 해제하도록 처리해야 함
    else:
        record.like_user.remove(request.user)
        record.likes-=1
    record.save()
    return redirect('consumption:consumption', request.session['nickname'])

# 금융 통계
def statistic(request):
    # 날짜 검색한 경우
    if request.method=="POST":
        year=request.POST.get("year")
        month=request.POST.get("month")
    # 날짜 검색 없이 처음 get 요청인 경우 현재 달을 보여줌 
    else:
        today=datetime.today().strftime("%m/%d/%Y")
        year, month, date=parseTime(today)
        
    # 각각의 카테고리에 해당하는 Record 객체 필터링 
    total=Record.objects.filter(writer=request.user, year=year, month=month).count()
    food=Record.objects.filter(writer=request.user, category="음식", year=year, month=month)
    life=Record.objects.filter(writer=request.user, category="생필품", year=year, month=month)
    leisure=Record.objects.filter(writer=request.user, category="여가", year=year, month=month)
    transportation=Record.objects.filter(writer=request.user, category="교통", year=year, month=month)
    study=Record.objects.filter(writer=request.user, category="학습", year=year, month=month)
    etc=Record.objects.filter(writer=request.user, category="기타", year=year, month=month)
    
    total_records= Record.objects.filter(writer=request.user, year=year, month=month)
    common_category_array=common_category(food.count(),life.count(),leisure.count(),transportation.count(),study.count(),etc.count())
    
    # 통계 계산
    try:
        food_p = (food.count() / total) * 100
        life_p = (life.count() / total) * 100
        leisure_p = (leisure.count() / total) * 100
        transportation_p = (transportation.count() / total) * 100
        study_p = (study.count() / total) * 100
        etc_p = (etc.count() / total) * 100
    
    # 아무 기록도 없을 경우 
    except:
        food_p=life_p=leisure_p=transportation_p=study_p=etc_p=0
        common_category_array=[]

    # html에서 리스트로 접근하기 위해 리스트에 담음 
    value=[food_p, life_p, leisure_p, transportation_p, study_p, etc_p]
    value=','.join(map(str,value))
    context={
        "common_category":common_category_array,
        "value":value,
        "year":y,
        "month":m,
        "find_y":year,
        "find_m":month,
        "total_consumed":sum(record.price for record in total_records),
        "food_c":sum(record.price for record in food),
        "life_c":sum(record.price for record in life),
        "leisure_c":sum(record.price for record in leisure),
        "transportation_c":sum(record.price for record in transportation),
        "study_c":sum(record.price for record in study),
        "etc_c":sum(record.price for record in etc),
        
    }
    return render(request, 'consumption/statistics.html', context)
