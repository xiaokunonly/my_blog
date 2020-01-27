from django import forms
from django.contrib.auth.models import User
from .models import Profile
#登录表单，继承了forms.Form类，此类不涉及对数据库的修改
class UserLoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

#注册表单，继承了forms.ModelForm类，此类涉及对数据库的修改
class UserRegisterForm(forms.ModelForm):
    password=forms.CharField()
    password2=forms.CharField()
    class Meta:
        model=User
        fields=('username','email')
    # 该方法不能定义为clean_password,因为会将password2判定为无效数据而清洗掉。该方法会自动调用
    def clean_password2(self):
        data=self.cleaned_data
        if data.get('password') ==data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")

class ProfileForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('phone','avatar','bio')