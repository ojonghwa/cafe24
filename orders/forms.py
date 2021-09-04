from django import forms
from .models import Order


class OrderCreateForm(forms.ModelForm):     #309
    class Meta:
        model = Order
        fields = ['user', 'fullname', 'email', 'address', 'postal_code', 'mobile']
        labels = {
            'user' : '사용자 ID (회원일 경우 입력-비회원은 빈칸)',
            'fullname'   : '이름',
            'address'    : '주소',
            'postal_code': '우편번호',
            'mobile'     : '전화번호',
        }

