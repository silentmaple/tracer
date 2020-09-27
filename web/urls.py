from django.conf.urls import url, include
from web.views import account, project, dashboard, wiki, file, setting, statistics, issues

urlpatterns = [
    # 用户认证，登录，注册相关url
    url(r'^register/$', account.register, name="register"),  # 注册相关url
    url(r"^send/sms/$", account.send_sms, name="send_sms"),  # 发送短信url
    url(r'^login/sms/$', account.login_sms, name="login_sms"),  # 短信登录url
    url(r'^login/$', account.login, name="login"),  # 账号密码登录url
    url(r'^image/code/$', account.imagec_code, name="image_code"),  # 图片验证码url
    url(r'^logout/$', account.logout, name='logout'),  # 退出url
    url(r'^index/$', account.index, name="index"),  # 首页展示url

    # 项目列表相关url
    url(r'^project/list/$', project.project_list, name='project_list'),  # 项目首页展示url
    # 添加星标项目url
    url(r'^project/star/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_star, name='project_star'),
    # 取消星标项目url
    url(r'^project/unstar/(?P<project_type>\w+)/(?P<project_id>\d+)/$', project.project_unstar, name='project_unstar'),

    # 项目管理相关url
    url(r'^manage/(?P<project_id>\d+)/', include([
        # wiki相关url
        url(r'^wiki/$', wiki.wiki, name='wiki'),  # wiki首页
        url(r'^wiki/add/$', wiki.wiki_add, name='wiki_add'),  # 添加文章
        url(r'^wiki/catalog/$', wiki.wiki_catalog, name='wiki_catalog'),  # 多级目录
        url(r'^wiki/delete/(?P<wiki_id>\d+)/$', wiki.wiki_delete, name='wiki_delete'),  # 删除文章
        url(r'^wiki/edit/(?P<wiki_id>\d+)/$', wiki.wiki_edit, name='wiki_edit'),  # 编辑文章
        url(r'^wiki/upload/$', wiki.wiki_upload, name='wiki_upload'),  # 图片上传

        # 文件相关url
        url(r'^file/$', file.file, name='file'),  # 添加、修改，展示文件夹
        url(r'^file/delete/$', file.file_delete, name='file_delete'),  # 删除文件或文件夹
        url(r'^cos/credential/$', file.cos_credential, name='cos_credential'),  # 上传文件获取临时凭证
        url(r'^file/post/$', file.file_post, name='file_post'),  # 上传文件的相关操作的url
        url(r'^file/download/(?P<file_id>\d+)/$', file.file_download, name='file_download'),  # 文件下载相关url

        url(r'^setting/$', setting.setting, name='setting'),
        url(r'^issues/$', issues.issues, name='issues'),
        url(r'^dashboard/$', dashboard.dashboard, name='dashboard'),
        url(r'^statistics/$', statistics.statistics, name='statistics'),
    ], None, None)),

]
