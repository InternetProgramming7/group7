from django.urls import path
from . import views

app_name='trade'

urlpatterns=[
    path('r/',views.trade_require,name='trade'),
    path('f/',views.trade_finish, name='trade-finish'),
    path('create/', views.create, name='create'),
    path('<int:pk>/', views.trade_detail, name='trade_detail'),
    path('<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('<int:post_id>/chat/<int:chatroom_id>', views.into_chatroom, name='chating'),
    path('<int:post_id>/go-chat/',views.chat, name='go-chat'),
    path('<int:pk>/chat/', views.chat, name='chat'),
    path('<int:pk>/like/', views.like_post, name='like_post'),
    path('liked/', views.liked_posts, name='liked_posts'),
    path('<int:post_id>/review/', views.create_review, name='review'),
]
