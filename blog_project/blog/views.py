from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import  User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    TemplateView)

from .models.blog_post import Post


# Create your views here.

# def home(request):
#     context = {
#         'posts': Post.objects.all()
#     }
#     return render(request, 'blog/home.html', context)


class PostListView(ListView):
    model = Post
    # <app>/<model>_<viewtype>.html
    # if we use this convention, we don't have to set template name
    template_name = 'blog/home.html'
    # if we access our variable using object we don't have to
    #change this
    context_object_name = 'posts'
    ordering = ['-date_posted',]
    paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    context_object_name = 'form'
    fields = ['title', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return  super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    context_object_name = 'form'
    fields = ['title', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return  super().form_valid(form)

    def test_func(self):
        post = self.get_object()

        return True if(self.request.user == post.author) else False;


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    context_object_name = 'post'
    fields = ['title', 'content', ]
    success_url = '/'

    def test_func(self):
        post = self.get_object()

        return True if(self.request.user == post.author) else False;





class AboutView(TemplateView):

    template_name = 'blog/about.html'



# def about(request):
#     return render(request, 'blog/about.html')
