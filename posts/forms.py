from django import forms
from .models import Comment, Post

class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'body', 'image', 'categories')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control', 'autocomplete': 'off'})

            self.fields['body'].widget.attrs.update({'class': 'form-control django_ckeditor_5'})
            self.fields['body'].required = False