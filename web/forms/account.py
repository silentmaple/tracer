import random

from django import forms

from web import models
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.conf import settings
from web.forms.bootstrap import BootStrapForm
from django_redis import get_redis_connection
from utils import encrypt


class RegisterModelForm(BootStrapForm,forms.ModelForm):
    mobile = forms.CharField(
        label="手机号",
        # validators=[RegexValidator(r'(1[3][5][6][7][8][9])\d{9}$', '手机号格式错误'), ]
        validators=[RegexValidator(r'1[356789]\d{9}$', '手机号格式错误')]
    )
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='重复密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "重复密码长度不能小于8个字符",
            'max_length': "重复密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput())
    verify_code = forms.CharField(label='验证码', widget=forms.TextInput())

    class Meta:
        model = models.UserInfo
        fields = ['username', 'email', 'password', 'confirm_password', 'mobile', 'verify_code']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for name, field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)

    # 上述为返回响应html标签，下面利用form局部钩子校验参数
    # 'username', 'email', 'password', 'confirm_password', 'mobile', 'verify_code'
    def clean_username(self):
        # 校验数据库中是否存在
        username = self.cleaned_data['username']
        exists = models.UserInfo.objects.filter(username=username).exists()
        if exists:
            raise ValidationError("用户名已存在")
        return username

    def clean_email(self):
        # 校验邮箱
        email = self.cleaned_data['email']
        exists = models.UserInfo.objects.filter(email=email).exists()
        if exists:
            raise ValidationError("邮箱已存在")
        return email

    def clean_password(self):
        # 将密码转换为密文保存
        password = self.cleaned_data["password"]
        return encrypt.md5(password)

    def clean_confirm_password(self):
        # 校验2次密码是否正确
        password = self.cleaned_data.get('password')
        confirm_password = encrypt.md5(self.cleaned_data.get('confirm_password'))
        if confirm_password != password:
            raise ValidationError("两次密码不一致")
        return confirm_password

    def clean_mobile(self):
        # 校验手机号
        mobile = self.cleaned_data['mobile']
        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        if exists:
            raise ValidationError("手机号已存在")
        return mobile

    def clean_verify_code(self):
        # 校验验证码
        mobile = self.cleaned_data.get('mobile')
        verify_code = self.cleaned_data['verify_code']
        if not mobile:
            return verify_code
        conn = get_redis_connection()
        redis_code = conn.get(mobile)
        if not redis_code:
            raise ValidationError("验证码失效或未发，请重新获取")

        redis_code_str = redis_code.decode('utf-8')

        if redis_code_str != verify_code.strip():
            raise ValidationError("验证码错误")
        return verify_code


class SendSmsForm(forms.Form):
    mobile = forms.CharField(
        label="手机号",
        validators=[RegexValidator(r'1[356789]\d{9}$', '手机号格式错误'), ]
    )

    def __init__(self, request, *args, **kwargs):
        # 将request传入此类中，便于获得tpl，可以和手机号一起校验
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_mobile(self):
        """手机号校验的局部钩子"""
        mobile = self.cleaned_data["mobile"]
        # 获得tpl模板参数，校验模板是否正确
        tpl = self.request.GET.get("tpl")
        template_id = settings.TENCENT_SMS_TEMPLATE.get(tpl)
        if not template_id:
            raise ValidationError("短信模板错误")

        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        # if exists:
        #     if tpl == "register":
        #         raise ValidationError("手机号已存在")
        if tpl == 'login':
            if not exists:
                raise ValidationError("手机号不存在")
        else:
            if exists:
                raise ValidationError("手机号已存在")

        # 发送短信
        sms_code = random.randint(1000, 9999)
        print(sms_code)

        # 将短信验证码保存到redis，并设置过期时间为60s
        conn = get_redis_connection("default")
        conn.set(mobile, sms_code, ex=60)

        return mobile


class LoginSmsForm(BootStrapForm,forms.Form):
    mobile = forms.CharField(
        label="手机号",
        # validators=[RegexValidator(r'(1[3][5][6][7][8][9])\d{9}$', '手机号格式错误'), ]
        validators=[RegexValidator(r'1[356789]\d{9}$', '手机号格式错误')]
    )
    verify_code = forms.CharField(label='验证码', widget=forms.TextInput())

    # def __init__(self,*args,**kwargs):
    # 此属性封装在forms/bootstrap.py中
    #     super().__init__(*args,**kwargs)
    #     for field in self.fields.items():
    #         field.widget.attrs['class'] = 'form-control'
    #         field.widget.attrs['placeholder'] = '请输入{}'.format(field.label)

    def clean_mobile(self):
        """校验手机号"""
        mobile = self.cleaned_data['mobile']
        exists = models.UserInfo.objects.filter(mobile=mobile).exists()
        if not exists:
            raise ValidationError("手机号未注册，请注册账号")

        return mobile

    def clean_verify_code(self):
        """校验验证码"""
        mobile = self.cleaned_data['mobile']
        verify_code = self.cleaned_data['verify_code']
        # 手机号不存在，则验证码无需再校验
        if not mobile:
            return verify_code

        conn = get_redis_connection('default')
        verify_code_str = conn.get(mobile).decode('utf-8')
        if not verify_code_str:
            raise ValidationError("验证码失效或未发，请重新获取")

        if verify_code.strip() != verify_code_str:
            raise ValidationError("验证码输入错误")

        return verify_code


class LoginForm(BootStrapForm, forms.Form):
    username = forms.CharField(label='邮箱或手机号')
    password = forms.CharField(
        label='密码',
        min_length=8,
        max_length=64,
        error_messages={
            'min_length': "密码长度不能小于8个字符",
            'max_length': "密码长度不能大于64个字符"
        },
        widget=forms.PasswordInput(render_value=True)
    )
    image_code = forms.CharField(label='图片验证码')

    def __init__(self, request, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.request = request

    def clean_password(self):
        pwd = self.cleaned_data['password']
        return encrypt.md5(pwd)

    def clean_image_code(self):
        image_code = self.cleaned_data['image_code']
        # 去session获取自己的验证码
        session_code = self.request.session.get('image_code')
        if not session_code:
            raise ValidationError('验证码已过期，请重新获取')

        if image_code.strip().upper() != session_code.strip().upper():
            raise ValidationError('验证码输入错误')

        return image_code







