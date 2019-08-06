from django.shortcuts import render,redirect,reverse,HttpResponse
import re
from apps.user.models import User
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import settings
from itsdangerous import SignatureExpired
def register(request):
    '''显示注册页面'''
    if request.method=='GET':
        return render(request, 'register.html')
    else:
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username, password, email]):
            return render(request, 'register.html', {'errorMsg': '数据不完整'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errorMsg': '邮箱格式不正确！'})
        if allow != 'on':
            return render(request, 'register.html', {'errorMsg': '请同意协议'})
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errorMsg': '该用户已经存在'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()
        return redirect(reverse('goods:index'))


def register_hander(request):
    pass

class RegisterView(View):
    def get(self,request):
        return render(request,'register.html')
    def post(self,request):
        username = request.POST.get('user_name')
        password = request.POST.get('pwd')
        email = request.POST.get('email')
        allow = request.POST.get('allow')
        if not all([username, password, email]):
            return render(request, 'register.html', {'errorMsg': '数据不完整'})
        if not re.match(r'^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
            return render(request, 'register.html', {'errorMsg': '邮箱格式不正确！'})
        if allow != 'on':
            return render(request, 'register.html', {'errorMsg': '请同意协议'})
        try:
            user = User.objects.get(username=username)

        except User.DoesNotExist:
            user = None

        if user:
            return render(request, 'register.html', {'errorMsg': '该用户已经存在'})

        user = User.objects.create_user(username, email, password)
        user.is_active = 1
        user.save()
        return redirect(reverse('goods:index'))


class ActiveView(View):
    def get(self,request,token):
        serializer=Serializer(settings.SECRET_KEY,3600)
        try:
            info=serializer.loads(token)
            user_id=info['confirm']
            user=User.objects.get(id=user_id)
            user.is_active=1
            user.save()

            return  redirect(reverse('user:login'))
        except SignatureExpired as e:
            return HttpResponse('激活链接已过期')

class LoginView(View):
    def get(self,request):
        return render(request,'login.html')


