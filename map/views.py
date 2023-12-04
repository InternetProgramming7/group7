from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import *
from datetime import date

def map_benefit_list(request):
    today = date.today()
    benefits = Benefit.objects.filter(deadline__gte=today).order_by('deadline') # 날짜가 지난 데이터들은 불러오지 않음 deadline>today
    maps=Map.objects.filter(deadline__gte=today).order_by('deadline')
    context={'benefits':benefits, 'maps':maps}
    return render(request, 'map/map_benefit.html',context)

class map_detail(DetailView):
    model=Map


class benefit_detail(DetailView):
    model=Benefit


def benefit_scrap(request, id):
    benefit=get_object_or_404(Benefit, id=id)

    if request.user not in  benefit.scrap.all():
        benefit.scrap.add(request.user)
    else:
        benefit.scrap.remove(request.user)
    print(benefit.scrap.all())
    benefit.save()
    return redirect('map:benefit-detail', benefit.id)

def map_scrap(request, id):
    map=get_object_or_404(Map, id=id)

    if request.user not in  map.scrap.all():
        map.scrap.add(request.user)
    else:
        map.scrap.remove(request.user)
    print(map.scrap.all())
    map.save()
    return redirect('map:map-detail', map.id)


def benefit_scrap_detail(request, id):
    benefit=get_object_or_404(Benefit, id=id)
    context={
        'benefit':benefit
    }
    return render(request, 'map/benefit_detail _mypage.html',context )

def map_scrap_detail(request, id):
    map=get_object_or_404(Map, id=id)
    context={
        'map':map
    }
    return render(request, 'map/map_detail_mypage.html',context )
