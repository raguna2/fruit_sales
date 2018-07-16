#sales/url.py
from django.conf.urls import url
from .master_list_views import MasterListView
from .deal_list_views import DealListView
from django.contrib.auth.views import logout_then_login,login
from .master_views import add_fruit, FruitDeleteView, FruitUpdateView
from .deal_views import add_deal, DealDeleteView, DealUpdateView
from .views import after_login, render_menu, upload_csv
from .analytics_views import render_analytics


urlpatterns = [
        #ログイン後のメニューページ
        url(r'^$', render_menu , name='mainpage'),
        url(r'^after_login$', after_login , name='after_login'),
        #masters
        url(r'^masters$', MasterListView.as_view() , name='masters'),
        url(r'^masters/add/$', add_fruit , name='add_fruit'),
        url(r'^masters/update/(?P<pk>\d+)/$', FruitUpdateView.as_view() , name='edit_fruit'),
        url(r'^masters/delete/(?P<pk>\d+)$', FruitDeleteView.as_view() , name='fruit_delete_confirm'),
        #deals
        url(r'^deals$', DealListView.as_view() , name='deals'),
        url(r'^deals/add/$', add_deal , name='add_deal'),
        url(r'^deals/upload/$', upload_csv , name='upload'),
        url(r'^deals/update/(?P<pk>\d+)/$', DealUpdateView.as_view() , name='edit_deal'),
        url(r'^deals/delete/(?P<pk>\d+)$', DealDeleteView.as_view() , name='deal_delete_confirm'),
        #analytics
        url(r'^analytics$', render_analytics , name='analytics'),
        ]

