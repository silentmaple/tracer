class BootStrapForm(object):
    bootstrap_class_exclude = []

    def __init__(self, *args, **kwargs):
        bootstrap_class_exclude = []
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            # 因为此时调用bootstrap_class_exclude的self是form中的ProjectModelForm生成的对象，因此bootstrap_class_exclude优先去ProjectModelForm找
            if name in self.bootstrap_class_exclude:
                continue
            old_class = field.widget.attrs.get('class', "")
            field.widget.attrs['class'] = '{} form-control'.format(old_class)
            field.widget.attrs['placeholder'] = '请输入%s' % (field.label,)
