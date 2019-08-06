from django.db import models
from db import base_model
from django.contrib.auth.models import  AbstractUser
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from django.conf import  settings
class User(AbstractUser,base_model.BaseModel):
    def generate_active_token(self):
        serializer=Serializer(settings.SECRET_KEY,3600)
        info={'confirm':self.id}
        token=serializer.dumps(info)
        return token.decode()
    class Meta:
        db_table='db_user'
        verbose_name='用户'
        verbose_name_plural=verbose_name

class Address(base_model.BaseModel):
    user=models.ForeignKey('User',verbose_name='所属用户',on_delete=models.CASCADE)
    receiver=models.CharField(max_length=20,verbose_name='收件人')
    addr=models.CharField(max_length=256,verbose_name='收货地址')
    zip_code=models.CharField(max_length=6,null=True,verbose_name='邮政编码')
    phone=models.CharField(max_length=11,verbose_name='联系电话')
    is_default=models.BooleanField(default=False,verbose_name='是否默认')
    class Meta:
        db_table="db_address"
        verbose_name='地址'
        verbose_name_plural=verbose_name
