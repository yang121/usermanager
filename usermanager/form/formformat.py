from django.forms import Form, fields, widgets
from rbac import models
from django.core.exceptions import ValidationError


class LoginForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请输入用户名', 'class': "form-control", 'id': "inputUserName"}),
        label='',
        label_suffix=''
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'placeholder': '请输入密码', 'class': "form-control", 'id': "inputPassWord"}),
        label='',
        label_suffix='',
        error_messages={

        }
    )


class RegisterForm(Form):
    username = fields.CharField(
        widget=widgets.TextInput(attrs={'placeholder': '请填写用户名', 'class': "form-control", 'id': "inputUserName"}),
        label='',
        label_suffix='',
        max_length=32,
        min_length=5,
        required=True,
        error_messages={
            'required': "请填写用户名",
            'min_length': "用户名长度必须大于5",
            'max_length': "用户名长度必须小于32",
        }
    )

    password = fields.CharField(
        widget=widgets.PasswordInput(attrs={'placeholder': '请填写密码', 'class': "form-control", 'id': "inputPassWord"}),
        label='',
        label_suffix='',
        max_length=64,
        min_length=6,
        required=True,
        error_messages={
            'required': "请填写密码",
            'min_length': "密码长度必须大于5",
            'max_length': "密码长度必须小于32",
        }
    )

    email = fields.EmailField(
        widget=widgets.EmailInput(attrs={'placeholder': '请填写电子邮箱', 'class': "form-control", 'id': "inputEmail"}),
        label='',
        label_suffix='',
        error_messages={
            'required': "请填写确认密码",
            'invalid': '邮箱格式错误',
        }
    )

    def clean_username(self):
        username = self.cleaned_data['username']
        if models.User.objects.filter(username=username).first():
            raise ValidationError('此用户名已被注册')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if models.User.objects.filter(email=email).first():
            raise ValidationError("此邮箱已被注册")
        return email