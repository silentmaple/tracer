from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from web.forms import project
from web import models

from utils.tencent.cos import create_bucket


def project_list(request):
    """项目列表"""
    # GET请求查看项目列表
    if request.method == 'GET':
        """
            1. 从数据库中获取两部分数据
                我创建的所有项目：已星标、未星标
                我参与的所有项目：已星标、未星标
            2. 提取已星标
                列表 = 循环 [我创建的所有项目] + [我参与的所有项目] 把已星标的数据提取

            得到三个列表：星标、创建、参与
            """
        project_dict = {'star': [], 'my': [], 'join': []}
        # 我创建的所有项目

        my_project_list = models.Project.objects.filter(creator=request.tracer.user)

        for row in my_project_list:

            if row.star:
                # append字典是因为要利用key区分我创建和我参与的项目
                project_dict['star'].append({"value": row, 'type': 'my'})
            else:
                project_dict['my'].append(row)

        # 我参与的所有项目
        join_project_list = models.ProjectUser.objects.filter(user=request.tracer.user)
        for item in join_project_list:
            if item.star:
                project_dict['star'].append({"value": item.project, 'type': 'join'})
            else:
                project_dict['join'].append(item.project)

        form = project.ProjectModelForm(request)
        return render(request, 'project_list.html', {'form': form, 'project_dict': project_dict})

    # POST，对话框的ajax添加项目。
    form = project.ProjectModelForm(request, data=request.POST)
    if form.is_valid():
        name = form.cleaned_data['name']
        # 1. 为项目创建一个桶
        bucket = "{}-{}-1251317460".format(request.tracer.user.mobile_phone, str(int(time.time())))
        region = 'ap-chengdu'
        create_bucket(bucket, region)

        # 2.创建项目
        # 验证通过：项目名、颜色、描述 + creator谁创建的项目？
        form.instance.bucket = bucket
        form.instance.region = region
        form.instance.creator = request.tracer.user
        instance = form.save()

        return JsonResponse({'status': True})
    return JsonResponse({'status': False, 'error': form.errors})


def project_star(request, project_type, project_id):
    """ 星标项目 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=True)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=True)
        return redirect('project_list')

    return HttpResponse('请求错误')


def project_unstar(request, project_type, project_id):
    """ 取消星标 """
    if project_type == 'my':
        models.Project.objects.filter(id=project_id, creator=request.tracer.user).update(star=False)
        return redirect('project_list')

    if project_type == 'join':
        models.ProjectUser.objects.filter(project_id=project_id, user=request.tracer.user).update(star=False)
        return redirect('project_list')

    return HttpResponse('请求错误')
