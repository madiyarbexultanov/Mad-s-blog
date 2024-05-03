from django.urls import path
from posts.views import IndexListView, PostCreateView, PostPageView


app_name = 'posts'

urlpatterns = [
    path('category/<int:category_id>/', IndexListView.as_view(), name='category'),
    path('post/<int:post_id>/', PostPageView.as_view(), name='post_page'),
    path('create/', PostCreateView.as_view(), name='create_post'),
]