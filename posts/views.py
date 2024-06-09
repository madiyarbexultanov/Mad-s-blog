from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.db.models import Q 
from django.urls import reverse_lazy


from posts.models import Post, PostCategory, Comment
from common.views import TitleMixin
from posts.forms import PostCreateForm, PostUpdateForm


class IndexListView(TitleMixin, ListView):
    model = Post
    template_name = 'posts/index.html'
    title = 'Blog'
    categories = PostCategory.objects.all()

    def get_queryset(self):
        #Filters posts by categories
        queryset = super(IndexListView, self).get_queryset() #queryset is equal to Post.objects.all()
        category_id = self.kwargs.get('category_id')
        search_query = self.request.GET.get('q')  # Get the search query from the request

        if category_id:
            queryset = queryset.filter(categories=category_id)

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) | Q(author__username__icontains=search_query)
            )
        return queryset



class PostPageView(TitleMixin, DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    title = 'Blog Page'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.object
        context['author'] = post.author
        context['body'] = post.body
        context['image'] = post.image.url
        return context

class PostCreateView(TitleMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'posts/post_create.html'  # Create a new template for the form
    success_url = '/'  # Redirect to home page after successful form submission
    title = 'Create New Post'

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author of the post to the current user
        return super().form_valid(form)
    
class PostUpdateView(UpdateView):
    template_name = 'posts/post_update.html'
    form_class = PostUpdateForm
    model = Post
    pk_url_kwarg = 'post_id'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('index')
    

class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy("index")