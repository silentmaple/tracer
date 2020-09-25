from io import BytesIO
import uuid
import datetime

from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from web.forms import account
from web import models
from django.db.models import Q

from utils.image_code import check_code


def register(request):
    """注册"""
    if request.method == "GET":
        # 如果请求为get，返回register.html
        form = account.RegisterModelForm()
        return render(request, 'register.html', {'form': form})

    # 请求为post，利用form进行校验
    form = account.RegisterModelForm(data=request.POST)
    if form.is_valid():
        # 校验完成后，利用form中save方法保存数据
        instance = form.save()

        # 用户注册,创建交易记录
        # 方式一
        policy_object = models.PricePolicy.objects.filter(category=1, title="个人免费版").first()
        models.Transaction.objects.create(
            status=2,
            order=str(uuid.uuid4()),
            user=instance,
            price_policy=policy_object,
            count=0,
            price=0,
            start_datetime=datetime.datetime.now()
        )

        # return JsonResponse({'status': True, 'data': '/login/'})
        return JsonResponse({'status': True, 'data': '/login/'})
    return JsonResponse({'status': False, 'error': form.errors})


def send_sms(request):
    # 校验在form中完成
    # mobile = request.GET.get("mobile")
    # tpl = request.GET.get("tpl")
    print(request.GET)
    # 将request传入到form中
    form = account.SendSmsForm(request, data=request.GET)
    if form.is_valid():
        return JsonResponse({'status': True})

    return JsonResponse({'status': False, 'error': form.errors})


def login_sms(request):
    if request.method == 'GET':
        form = account.LoginSmsForm()
        return render(request, 'login_sms.html', {'form': form})
    form = account.LoginSmsForm(request.POST)
    if form.is_valid():
        mobile = form.cleaned_data['mobile']
        user_obj = models.UserInfo.objects.filter(mobile=mobile).first()

        request.session['user_id'] = user_obj.id
        request.session.set_expiry(60 * 60 * 24 * 24)

        return JsonResponse({'status': True, 'data': '/index/'})
    return JsonResponse({'status': False, 'error': form.errors})


def login(request):
    if request.method == 'GET':
        form = account.LoginForm(request)
        return render(request, 'login.html', {'form': form})
    form = account.LoginForm(request, data=request.POST)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user_obj = models.UserInfo.objects.filter(Q(email=username) | Q(mobile=username)).filter(
            password=password).first()
        if user_obj:
            request.session['user_id'] = user_obj.id
            request.session.set_expiry(60 * 60 * 24 * 14)

            return redirect('index')
        form.add_error('username', '用户名或密码错误')

    return render(request, 'login.html', {'form': form})


def imagec_code(request):
    image, code = check_code()
    # 将image返回，code保存到session中
    # 保存到session中，一个是有sessionid这个唯一key，每次请求都会携带sessionid，这样更方便
    # 保存到redis中，一个要自己创建唯一key，另一个还要连接redis，相对更耗性能
    request.session['image_code'] = code
    request.session.set_expiry(60)  # 主动修改session的过期时间为60s

    # 把图片的内容写到内存 stream,生成image直接放到内存中
    stream = BytesIO()
    image.save(stream, 'png')
    return HttpResponse(stream.getvalue())


def logout(request):
    request.session.flush()
    return redirect('index')


def index(request):
    return render(request, 'index.html')
