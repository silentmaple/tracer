from django.shortcuts import render
from django.http import HttpResponse
# from utils.yuntongxun.sms import CCP

# ModelForm组件相关模块
from django import forms
from app01 import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

# redis
from django_redis import get_redis_connection


# Create your views here.

def send_sms(request):

    mobile = request.GET.get('mobile')
    tpl = request.GET.get('tpl')
    conn = get_redis_connection("default")
    conn.set("flag",1,ex=60)
    print("qianqian")
    print(mobile)
    print(tpl)
    return HttpResponse("发送短信验证码成功")


class RegisterModelForm(forms.ModelForm):
    mobile = forms.CharField(label="手机号", validators=[RegexValidator(r'1[3][5][6][7][8][9]\d{9}$', '手机号格式错误'),])
    password = forms.CharField(label='密码',widget=forms.PasswordInput())
    confirm_password = forms.CharField(label='重复密码',widget=forms.PasswordInput())
    verify_code = forms.CharField(label='验证码',widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile', 'verify_code']

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
            field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)


def register(request):
    form = RegisterModelForm()
    context = {'form': form}
    print(form)
    return render(request, 'register.html', context)
