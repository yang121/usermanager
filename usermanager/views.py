from django.shortcuts import render, HttpResponse, redirect
from django.http import JsonResponse
from django.views import View
from rbac.cbv.views import RbacView
from rbac import models
from django.core.exceptions import ValidationError
from utils.auth_tool import my_auth
from usermanager.form import formformat
from rbac.service import initial_permission
from utils.json_time_extend import JsonCustomEncoder
import json


class Login(RbacView, View):
    def look(self, request, *args, **kwargs):
        obj = formformat.LoginForm()
        return render(request, 'login.html',{"obj": obj})

    def post(self, request, *args, **kwargs):
        obj = formformat.LoginForm(request.POST)

        if obj.is_valid():
            print('clean_data', obj.cleaned_data)
            auth_data = obj.cleaned_data
            user = my_auth(**auth_data)

            if user:
                request.session['login_status'] = True
                request.session['username'] = user.username
                request.session['uid'] = user.id
                initial_permission(request, user.id)
                print(request.session['rbac_permission_session_key'])
                if request.session['rbac_permission_session_key']['/backend.html']:
                    request.session['backend'] = True
                print(request.session.items())
                return redirect('/index.html')
            else:
                obj.add_error('username', ValidationError('用户名或密码错误'))
                print(obj.errors)
                return render(request, 'login.html', {'obj': obj})

        return render(request, 'login.html', {'obj': obj})


class Register(RbacView, View):
    def look(self, request, *args, **kwargs):
        obj = formformat.RegisterForm()
        return render(request, 'register.html', {"obj": obj})

    def post(self, request, *args, **kwargs):
        obj = formformat.RegisterForm(request.POST)
        try:
            code = request.session['code']
            input_code = request.POST.get('code').upper()
            print('input_code', input_code, ': code', code)
            if code != input_code:
                raise ValidationError('验证码错误')

        except Exception as e:
            print(e)
            obj.add_error('__all__', ValidationError(e))
            return render(request, 'register.html', {'obj': obj})

        if obj.is_valid():
            reg_data = obj.cleaned_data
            res = models.User.objects.create(**reg_data)
            print('res:', res)
            if res:
                user = models.User.objects.filter(**reg_data).first()
                request.session['login_status'] = True
                request.session['username'] = user.username
                request.session['uid'] = user.id
                initial_permission(request, user.id)
                print(request.session['rbac_permission_session_key'])
                if request.session['rbac_permission_session_key']['/backend.html']:
                    request.session['backend'] = True
                print(request.session.items())
                return redirect('/index.html')
            obj.add_error('__all__', ValidationError('服务器繁忙，请稍后再试'))
        request.session['login_status'] = False
        print('注册失败',request.session)
        return render(request, 'register.html', {'obj': obj})
"""
[
    ('login_status', True), 
    ('username', 'lcc520'), 
    ('rbac_menu_permission_session_key', {
        'rbac_menu_permission_key': [{
            'permission_id': 1, 
            'permission__menu_id': 4,
            'permission__url': '/usermanager.html', 
            'permission__caption': '用户信息设置'}], 
        'rbac_menu_key': [
            {'caption': '布局管理', 'id': 1, 'parent_id': None}, 
            {'caption': '首页', 'id': 3, 'parent_id': 1}, 
            {'caption': '用户管理', 'id': 4, 'parent_id': None}
        ]}), 
    ('uid', 2), 
    ('rbac_permission_session_key', {
        '/usermanager.html': ['get', 'delete', 'put', 'look', 'post'], 
        '/backend.html': ['look']
    })
]
"""


class Index(RbacView, View):
    def look(self, request, *args, **kwargs):
        return render(request, 'index.html')


class Logout(RbacView, View):
    def look(self, request, *args, **kwargs):
        request.session['login_status'] = False
        del request.session['username']
        del request.session['uid']
        print(request.session.items())
        return redirect('/index.html')


class Code(RbacView, View):
    def look(self, request, *args, **kwargs):
        from utils.code_generator import rd_check_code
        img, code = rd_check_code()
        from io import BytesIO
        stream = BytesIO()
        img.save(stream, 'png')
        request.session['code'] = code
        print(code)
        return HttpResponse(stream.getvalue())

class Backend(RbacView, View):
    def look(self, request, *args, **kwargs):
        return render(request, 'backend.html')


class UserInfo(RbacView, View):
    def look(self, request, *args, **kwargs):
        # print(request.permission_code)
        # if request
        return render(request, 'userinfo.html')




def get_data_list(request,model_cls,table_config):
    values_list = []
    for row in table_config:
        if not row['q']:
            continue
        values_list.append(row['q'])

    from django.db.models import Q

    condition = request.GET.get('condition')
    condition_dict = json.loads(condition)

    con = Q()
    for name,values in condition_dict.items():
        ele = Q() # select xx from where cabinet_num=sdf or cabinet_num='123'
        ele.connector = 'OR'
        for item in values:
            ele.children.append((name,item))
        con.add(ele, 'AND')

    server_list = model_cls.objects.filter(con).values(*values_list)
    return server_list


class UserInfoJson(RbacView, View):
    def look(self, request, *args, **kwargs):
        from usermanager.page_config import user as userConfig
        server_list = get_data_list(request,models.User,userConfig.user_config)
        ret = {
            'server_list': list(server_list),
            'table_config': userConfig.user_config,
            'global_dict':{
                # 'device_type_choices': models.User.device_type_choices,
                # 'device_status_choices': models.User.device_status_choices,
                # 'idc_choices': list(models.User.objects.values_list('id','name'))
            },
            'search_config': userConfig.search_config

        }

        return HttpResponse(json.dumps(ret, cls=JsonCustomEncoder))

    def delete(self, request, *args, **kwargs):
        uid = request.GET.get('nid')
        models.User.objects.filter(id=uid).delete()
        return redirect('/backend/userinfo.html')

    def post(self, request, *args, **kwargs):
        if request.method == 'GET':
            obj = formformat.RegisterForm()
            return render(request, 'add-userinfo.html', {"obj": obj})
        else:
            obj = formformat.RegisterForm(request.POST)
            return render(request, 'add-userinfo.html', {"obj": obj})
