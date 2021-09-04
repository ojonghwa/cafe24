from django import forms
from .models import Like, Profile
from .widgets import starWidget


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'address', 'postal_code', 'mobile']
        labels = {
            'fullname'   : '이름',
            'address'    : '주소',
            'postal_code': '우편번호',
            'mobile'     : '전화번호',
        }


class LikeForm(forms.ModelForm):
    class Meta:
        model = Like
        fields = ['user', 'product', 'grade']
        labels = {
            'grade'   : '평점',
        }
        widgets = {
            'grade':starWidget
        }

