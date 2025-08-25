from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, TemplateView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.urls import reverse_lazy
from .models import Article, Category, Comment, Advertisement
from .forms import CommentForm
import json


class HomeView(TemplateView):
    template_name = 'news/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Breaking news ticker
        context['breaking_news'] = Article.objects.filter(
            is_breaking=True, 
            status='published'
        )[:10]
        
        # Featured article (main story)
        context['featured_article'] = Article.objects.filter(
            featured=True, 
            status='published'
        ).first()
        
        # Latest articles by category
        categories = Category.objects.filter(is_active=True, parent=None)[:6]
        context['category_articles'] = {}
        
        for category in categories:
            articles = Article.objects.filter(
                category=category, 
                status='published'
            )[:5]
            if articles.exists():
                context['category_articles'][category] = articles
        
        # Most read articles
        context['most_read'] = Article.objects.filter(
            status='published'
        ).order_by('-views')[:5]
        
        # Most commented articles
        context['most_commented'] = Article.objects.filter(
            status='published'
        ).annotate(
            comment_count=Count('comments', filter=Q(comments__active=True))
        ).order_by('-comment_count')[:5]
        
        # Latest articles (general)
        context['latest_articles'] = Article.objects.filter(
            status='published'
        )[:8]
        
        return context


class ArticleDetailView(DetailView):
    model = Article
    template_name = 'news/article_detail.html'
    context_object_name = 'article'
    
    def get_object(self):
        return get_object_or_404(
            Article,
            publish_date__year=self.kwargs['year'],
            publish_date__month=self.kwargs['month'],
            publish_date__day=self.kwargs['day'],
            slug=self.kwargs['slug'],
            status='published'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Increment views
        article.increment_views()
        
        # Comments
        context['comments'] = article.comments.filter(active=True).order_by('-created_date')
        context['comment_form'] = CommentForm()
        
        # Related articles
        context['related_articles'] = article.get_related_articles()
        
        return context


class CategoryView(ListView):
    model = Article
    template_name = 'news/category_detail.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return self.category.get_all_articles().order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagView(ListView):
    model = Article
    template_name = 'news/tag_detail.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        tag_slug = self.kwargs['slug']
        return Article.objects.filter(
            tags__slug=tag_slug,
            status='published'
        ).order_by('-publish_date')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_slug'] = self.kwargs['slug']
        return context


class SearchView(ListView):
    model = Article
    template_name = 'news/search_results.html'
    context_object_name = 'articles'
    paginate_by = 10
    
    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Article.objects.filter(
                Q(title__icontains=query) |
                Q(summary__icontains=query) |
                Q(body__icontains=query),
                status='published'
            ).order_by('-publish_date')
        return Article.objects.none()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('news:login')
    
    def form_valid(self, form):
        messages.success(self.request, 'অ্যাকাউন্ট সফলভাবে তৈরি হয়েছে!')
        return super().form_valid(form)


class AddCommentView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    
    def form_valid(self, form):
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        form.instance.article = article
        form.instance.user = self.request.user
        form.instance.active = False  # Needs moderation
        
        response = super().form_valid(form)
        messages.success(self.request, 'আপনার মন্তব্য পর্যালোচনার জন্য পাঠানো হয়েছে।')
        
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'message': 'মন্তব্য সফলভাবে যোগ করা হয়েছে!'})
        
        return redirect(article.get_absolute_url())
    
    def form_invalid(self, form):
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'errors': form.errors})
        
        article = get_object_or_404(Article, id=self.kwargs['article_id'])
        messages.error(self.request, 'মন্তব্য যোগ করতে ত্রুটি হয়েছে।')
        return redirect(article.get_absolute_url())