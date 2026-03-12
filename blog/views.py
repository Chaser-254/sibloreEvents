from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .models import Post, Category, Tag, Comment


class OrganizerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and getattr(self.request.user, 'is_seller', False)


class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['featured_posts'] = Post.objects.filter(status='published', featured=True)[:3]
        context['categories'] = Category.objects.all()
        context['popular_tags'] = Tag.objects.all()[:10]
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Post.objects.filter(status='published').select_related('author', 'category').prefetch_related('tags', 'comments__author')
    
    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['related_posts'] = Post.objects.filter(
            status='published',
            category=self.object.category
        ).exclude(pk=self.object.pk)[:3]
        context['can_comment'] = self.request.user.is_authenticated and not getattr(self.request.user, 'is_seller', False)
        return context


class PostCreateView(LoginRequiredMixin, OrganizerRequiredMixin, CreateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'category', 'content', 'featured_image', 'excerpt', 'featured']
    success_url = reverse_lazy('blog:my_posts')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = None  # Let the model generate the slug
        messages.success(self.request, 'Blog post created successfully! It\'s now in draft status.')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create New Blog Post'
        return context


class PostUpdateView(LoginRequiredMixin, OrganizerRequiredMixin, UpdateView):
    model = Post
    template_name = 'blog/post_form.html'
    fields = ['title', 'category', 'content', 'featured_image', 'excerpt', 'featured', 'status']
    success_url = reverse_lazy('blog:my_posts')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Blog post updated successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edit Blog Post'
        return context


class PostDeleteView(LoginRequiredMixin, OrganizerRequiredMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:my_posts')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Blog post deleted successfully!')
        return super().delete(request, *args, **kwargs)


class MyPostsView(LoginRequiredMixin, OrganizerRequiredMixin, ListView):
    model = Post
    template_name = 'blog/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user).select_related('category').order_by('-created_at')


class CategoryPostView(ListView):
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', category=self.category).select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostView(ListView):
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.filter(status='published', tags=self.tag).select_related('author', 'category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class SearchView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                status='published'
            ).filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(excerpt__icontains=query)
            ).select_related('author', 'category').distinct()
        return Post.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Only buyers (non-sellers) can comment
    if getattr(request.user, 'is_seller', False):
        messages.error(request, 'Event organizers cannot comment on blog posts.')
        return redirect('blog:post_detail', slug=slug)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                post=post,
                author=request.user,
                content=content
            )
            messages.success(request, 'Your comment has been posted!')
        else:
            messages.error(request, 'Please enter a comment.')
    
    return redirect('blog:post_detail', slug=slug)
