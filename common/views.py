class TitleMixin:
    title = None
    categories = None
    image = None
    
    def get_context_data(self, **kwargs):
        context = super(TitleMixin, self).get_context_data(**kwargs)
        context['title'] = self.title
        context["categories"] = self.categories
        context['image'] = self.image
        return context
