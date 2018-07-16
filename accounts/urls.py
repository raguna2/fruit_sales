#accouts/url.py
from django.conf.urls import url
from .forms import LoginForm
from .views import main
from django.contrib.auth.views import logout_then_login,login

urlpatterns = [
        #トップページ
        url(r'^$', main, name='main'),
        #ログイン
        url(r'^login/$',login,name='login'),
        #ログアウト
        url(r'^logout/$',logout_then_login, name ='logout' ),
        ]

