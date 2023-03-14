from django.urls import path, re_path

from . import views

app_name = "OpenVPNApp"

urlpatterns = [
    path('wx', views.wx, name='wx'),
    re_path('wx?P<signature>&?P<echostr>&?P<timestamp>&?P<nonce>', views.wx, name='wx'),
    path('gettoken', views.get_token, name='gettoken'),
    # path('test', views.test, name='test'),
]

# urlpatterns = [
#     re_path(r'articles(?P<year>[0-9]{4})/$', views.wx),
#     # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive),
#     # re_path(r'^articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail),
# ]