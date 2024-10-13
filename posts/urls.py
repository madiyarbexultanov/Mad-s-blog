from django.urls import path
from posts.views import IndexListView, PostCreateView, PostPageView, PostDeleteView, PostUpdateView


app_name = 'posts'

urlpatterns = [
    path('category/<int:category_id>/', IndexListView.as_view(), name='category'),
    path('post/<int:post_id>/', PostPageView.as_view(), name='post_page'),
    path('create/', PostCreateView.as_view(), name='create_post'),
    path('update/<int:post_id>/', PostUpdateView.as_view(), name='update_post'),
    path('delete/<int:post_id>/', PostDeleteView.as_view(), name='delete_post'),
    # path('post/<int:post_id>/comment/', CommentCreateView.as_view(), name='add_comment'),
]