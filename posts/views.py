from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.db.models import Q 
from django.urls import reverse_lazy


from posts.models import Post, PostCategory, Comment
from common.views import TitleMixin
from posts.forms import PostCreateForm, PostUpdateForm, CommentCreateForm


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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context



class PostPageView(TitleMixin, FormMixin, DetailView):
    model = Post
    template_name = 'posts/post_page.html'
    context_object_name = 'post'
    pk_url_kwarg = 'post_id'
    title = 'Blog Page'
    form_class = CommentCreateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        context['author'] = self.object.author
        context['body'] = self.object.body
        context['image'] = self.object.image.url if self.object.image else None
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.author = self.request.user  # Assuming the author is the logged-in user
        form.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('posts:post_page', kwargs={'post_id': self.object.id})

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
    title = 'Update Post'
    

class PostDeleteView(DeleteView):
    model = Post
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy("index")