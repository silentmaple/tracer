from django.db import models


# Create your models here.

class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, db_index=True)  # db_index=True 索引
    password = models.CharField(verbose_name='密码', max_length=32)
    email = models.EmailField(verbose_name='邮箱地址', max_length=32)
    mobile = models.CharField(verbose_name='手机号', max_length=32)

    # price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy', null=True, blank=True)

    def __str__(self):
        return self.username


class PricePolicy(models.Model):
    """ 价格策略 """
    category_choices = (
        (1, '免费版'),
        (2, '收费版'),
        (3, '其他'),
    )
    # 分类
    category = models.SmallIntegerField(verbose_name='收费类型', default=2, choices=category_choices)
    # 标题
    title = models.CharField(verbose_name='标题', max_length=32)
    # 价格
    price = models.PositiveIntegerField(verbose_name='价格')  # 正整数
    # 项目数
    project_num = models.PositiveIntegerField(verbose_name='项目数')
    # 项目成员数
    project_member = models.PositiveIntegerField(verbose_name='项目成员数')
    # 单项目空间
    project_space = models.PositiveIntegerField(verbose_name='单项目空间', help_text='G')
    # 单文件大小
    per_file_size = models.PositiveIntegerField(verbose_name='单文件大小', help_text="M")
    # 创建时间
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Transaction(models.Model):
    """ 交易记录 """
    status_choice = (
        (1, '未支付'),
        (2, '已支付')
    )
    # 是否支付的状态
    status = models.SmallIntegerField(verbose_name='状态', choices=status_choice)
    # 订单号
    order = models.CharField(verbose_name='订单号', max_length=64, unique=True)  # 唯一索引
    # 所属用户
    user = models.ForeignKey(verbose_name='用户', to='UserInfo')
    # 所用价格策略
    price_policy = models.ForeignKey(verbose_name='价格策略', to='PricePolicy')
    # 数量
    count = models.IntegerField(verbose_name='数量（年）', help_text='0表示无限期')
    # 实际支付
    price = models.IntegerField(verbose_name='实际支付价格')
    # 开始时间
    start_datetime = models.DateTimeField(verbose_name='开始时间', null=True, blank=True)
    # 结束时间
    end_datetime = models.DateTimeField(verbose_name='结束时间', null=True, blank=True)
    # 创建时间
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)


class Project(models.Model):
    """ 项目表 """
    COLOR_CHOICES = (
        (1, "#56b8eb"),  # 56b8eb
        (2, "#f28033"),  # f28033
        (3, "#ebc656"),  # ebc656
        (4, "#a2d148"),  # a2d148
        (5, "#20BFA4"),  # #20BFA4
        (6, "#7461c2"),  # 7461c2,
        (7, "#20bfa3"),  # 20bfa3,
    )

    name = models.CharField(verbose_name='项目名', max_length=32)
    color = models.SmallIntegerField(verbose_name='颜色', choices=COLOR_CHOICES, default=1)
    desc = models.CharField(verbose_name='项目描述', max_length=255, null=True, blank=True)

    use_space = models.BigIntegerField(verbose_name='项目已使用空间', default=0, help_text='字节')

    star = models.BooleanField(verbose_name='星标', default=False)

    join_count = models.SmallIntegerField(verbose_name='参与人数', default=1)
    creator = models.ForeignKey(verbose_name='创建者', to='UserInfo')
    create_datetime = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

    # bucket = models.CharField(verbose_name='cos桶', max_length=128)
    # region = models.CharField(verbose_name='cos区域', max_length=32)

    # 查询：可以省事；
    # 增加、删除、修改：无法完成
    # project_user = models.ManyToManyField(to='UserInfo',through="ProjectUser",through_fields=('project','user'))


class ProjectUser(models.Model):
    """ 项目参与者 """
    project = models.ForeignKey(verbose_name='项目', to='Project')
    user = models.ForeignKey(verbose_name='参与者', to='UserInfo')
    star = models.BooleanField(verbose_name='星标', default=False)

    create_datetime = models.DateTimeField(verbose_name='加入时间', auto_now_add=True)

















