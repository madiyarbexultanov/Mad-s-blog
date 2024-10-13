from django import forms
from .models import Comment, Post, PostCategory

class PostCreateForm(forms.ModelForm):
    categories = forms.ModelMultipleChoiceField(
    queryset=PostCategory.objects.all(),
    widget=forms.SelectMultiple(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'categories',)
        labels = {
            'body': 'Content', 
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your content here...', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
class PostUpdateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'image', 'categories',)
        labels = {
            'body': 'Content', 
        }
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Write your content here...', 'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-control'})
        }
        
class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)

        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Write your comment here...', 'class': 'form-control'}),
        }