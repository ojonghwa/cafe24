from django import forms
from blog.models import Post, Comment


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'body', 'product', 'status']
        widgets = {
            'title' : forms.TextInput(attrs={'class':'form-control'}), 
            #'author': forms.Select(attrs={'class':'form-control'}), 
            'body'  : forms.Textarea(attrs={'class':'form-control', 'rows':'10'}), 
            'product': forms.Select(attrs={'class':'form-control'}),
            'status': forms.Select(attrs={'class':'form-control'}),
        }
        labels = {
            'title' : '제목', 
            'body'  : '내용', 
            'product': '제품',
            'status': '공개 여부',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }
