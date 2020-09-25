from django.conf.urls import url, include
from web.views import account, project, dashboard, wiki, file, setting, statistics, issues

urlpatterns = [
    # 用户认证，登录，注册相关url
    url(r'^register/$', account.register, name="register"),
    url(r"^send/sms/$", account.send_sms, name="send_sms"),
    url(r'^login/sms/$', account.login_sms, name="login_sms"),
    url(r'^login/$', account.login, name="login"),
    url(r'^image/code/$', account.imagec_code, name="image_code"),
    url(r'^logout/$', account.logout, name='logout'),
    url(r'^index/$', account.index, name="index"),

    # 项目列表相关url
    url(r'^project/list/$', project.project_list, name='project_list'),
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

    # 项目管理相关url
    url(r'^manage/(?P<project_id>\d+)/', include([
        url(r'^wiki/$', wiki.wiki, name='wiki'),
        url(r'^file/$', file.file, name='file'),
        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^statistics/$', statistics.statistics, name='statistics'),
    ], None, None)),

]
