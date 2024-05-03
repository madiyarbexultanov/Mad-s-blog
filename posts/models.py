from django.db import models
from users.models import User
from django_ckeditor_5.fields import CKEditor5Field

class PostCategory(models.Model):
    name = models.CharField(max_length=128, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=256)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body=CKEditor5Field('Text', config_name='extends')
    image = models.ImageField(upload_to='post_images')
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField(to=PostCategory, related_name="posts")


    def __str__(self):
        return f'Title: {self.title} | Author: {self.author}'

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')  # Link the comment to the Post model
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # Link the comment to the User model
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
