from django.conf.urls import url
from tutorials import views

urlpatterns = [
    url(r'^api/posts$', views.post_list),
    url(r'^api/posts/(?P<pk>[0-9]+)$', views.post_detail),
    url(r'^api/posts/published$', views.post_list_published),

    url(r'^api/user$', views.create_user),
    url(r'^api/user/(?P<pk>[0-9]+)$', views.user_detail),
    
    url(r'^api/login$', views.user_Login),
]