from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="নাম")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="স্লাগ")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              related_name='children', verbose_name="প্যারেন্ট ক্যাটেগরি")
    description = models.TextField(blank=True, verbose_name="বিবরণ")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    
    class Meta:
        verbose_name = "ক্যাটেগরি"
        verbose_name_plural = "ক্যাটেগরিসমূহ"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:category_detail', kwargs={'slug': self.slug})
    
    def get_children(self):
        return self.children.filter(is_active=True)
    
    def get_all_articles(self):
        """Get all articles from this category and its children"""
        from django.db.models import Q
        categories = [self]
        categories.extend(self.get_children())
        return Article.objects.filter(
            Q(category__in=categories),
            status='published'
        )


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="নাম")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="স্লাগ")
    
    class Meta:
        verbose_name = "ট্যাগ"
        verbose_name_plural = "ট্যাগসমূহ"
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Article(models.Model):
    STATUS_CHOICES = [
        ('draft', 'খসড়া'),
        ('published', 'প্রকাশিত'),
        ('archived', 'সংরক্ষিত'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="শিরোনাম")
    slug = models.SlugField(max_length=200, unique_for_date='publish_date', verbose_name="স্লাগ")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name="লেখক")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='articles', verbose_name="ক্যাটেগরি")
    tags = TaggableManager(verbose_name="ট্যাগসমূহ", blank=True)
    image = models.ImageField(upload_to='articles/%Y/%m/%d/', verbose_name="ছবি")
    image_caption = models.CharField(max_length=200, blank=True, verbose_name="ছবির ক্যাপশন")
    body = RichTextUploadingField(verbose_name="বিষয়বস্তু")
    summary = models.TextField(max_length=500, verbose_name="সারসংক্ষেপ")
    publish_date = models.DateTimeField(default=timezone.now, verbose_name="প্রকাশের তারিখ")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    updated_date = models.DateTimeField(auto_now=True, verbose_name="আপডেটের তারিখ")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft', verbose_name="অবস্থা")
    is_breaking = models.BooleanField(default=False, verbose_name="জরুরি সংবাদ")
    views = models.PositiveIntegerField(default=0, verbose_name="দেখা হয়েছে")
    featured = models.BooleanField(default=False, verbose_name="ফিচারড")
    
    class Meta:
        verbose_name = "নিবন্ধ"
        verbose_name_plural = "নিবন্ধসমূহ"
        ordering = ['-publish_date']
        get_latest_by = 'publish_date'
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('news:article_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })
    
    def increment_views(self):
        """Increment article views"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def get_related_articles(self, count=5):
        """Get related articles by tags and category"""
        from django.db.models import Count
        
        # Get articles with similar tags
        tag_ids = self.tags.values_list('id', flat=True)
        related = Article.objects.filter(
            tags__in=tag_ids,
            status='published'
        ).exclude(id=self.id).annotate(
            tag_count=Count('tags')
        ).order_by('-tag_count', '-publish_date')[:count]
        
        # If not enough related articles, fill with same category
        if related.count() < count:
            category_articles = Article.objects.filter(
                category=self.category,
                status='published'
            ).exclude(id=self.id).order_by('-publish_date')
            
            related_ids = [article.id for article in related]
            additional = category_articles.exclude(id__in=related_ids)[:count - related.count()]
            
            related = list(related) + list(additional)
        
        return related[:count]


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments', verbose_name="নিবন্ধ")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="ব্যবহারকারী")
    body = models.TextField(verbose_name="মন্তব্য")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    active = models.BooleanField(default=False, verbose_name="সক্রিয়")
    
    class Meta:
        verbose_name = "মন্তব্য"
        verbose_name_plural = "মন্তব্যসমূহ"
        ordering = ['-created_date']
    
    def __str__(self):
        return f'{self.user.username} - {self.article.title[:50]}'


class Advertisement(models.Model):
    AD_LOCATIONS = [
        ('top_banner', 'শীর্ষ ব্যানার'),
        ('sidebar', 'সাইডবার'),
        ('bottom_banner', 'নিচের ব্যানার'),
        ('in_article', 'নিবন্ধের মধ্যে'),
        ('popup', 'পপআপ'),
    ]
    
    title = models.CharField(max_length=100, verbose_name="শিরোনাম")
    ad_image = models.ImageField(upload_to='ads/', verbose_name="বিজ্ঞাপনের ছবি")
    ad_url = models.URLField(verbose_name="বিজ্ঞাপনের লিংক")
    ad_location = models.CharField(max_length=20, choices=AD_LOCATIONS, verbose_name="বিজ্ঞাপনের অবস্থান")
    is_active = models.BooleanField(default=True, verbose_name="সক্রিয়")
    start_date = models.DateTimeField(verbose_name="শুরুর তারিখ")
    end_date = models.DateTimeField(verbose_name="শেষ তারিখ")
    created_date = models.DateTimeField(auto_now_add=True, verbose_name="তৈরির তারিখ")
    
    class Meta:
        verbose_name = "বিজ্ঞাপন"
        verbose_name_plural = "বিজ্ঞাপনসমূহ"
        ordering = ['-created_date']
    
    def __str__(self):
        return self.title
    
    def is_valid(self):
        """Check if ad is currently valid"""
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date