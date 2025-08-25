from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Article, Comment, Advertisement


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'is_active', 'created_date']
    list_filter = ['is_active', 'parent', 'created_date']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('parent')


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'is_breaking', 'featured', 'views', 'publish_date']
    list_filter = ['status', 'is_breaking', 'featured', 'category', 'publish_date', 'author']
    search_fields = ['title', 'summary', 'body']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_breaking', 'featured']
    date_hierarchy = 'publish_date'
    ordering = ['-publish_date']
    
    fieldsets = (
        ('মূল তথ্য', {
            'fields': ('title', 'slug', 'author', 'category')
        }),
        ('বিষয়বস্তু', {
            'fields': ('summary', 'body', 'image', 'image_caption', 'tags')
        }),
        ('প্রকাশনা', {
            'fields': ('status', 'publish_date', 'is_breaking', 'featured')
        }),
        ('পরিসংখ্যান', {
            'fields': ('views',),
            'classes': ('collapse',)
        })
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new article
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'article_title', 'created_date', 'active']
    list_filter = ['active', 'created_date']
    search_fields = ['user__username', 'article__title', 'body']
    list_editable = ['active']
    ordering = ['-created_date']
    
    def article_title(self, obj):
        return obj.article.title[:50]
    article_title.short_description = 'নিবন্ধ'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user', 'article')


@admin.register(Advertisement)
class AdvertisementAdmin(admin.ModelAdmin):
    list_display = ['title', 'ad_location', 'is_active', 'is_valid_display', 'start_date', 'end_date']
    list_filter = ['ad_location', 'is_active', 'start_date', 'end_date']
    search_fields = ['title']
    list_editable = ['is_active']
    date_hierarchy = 'start_date'
    
    def is_valid_display(self, obj):
        if obj.is_valid():
            return format_html('<span style="color: green;">✓ বৈধ</span>')
        else:
            return format_html('<span style="color: red;">✗ অবৈধ</span>')
    is_valid_display.short_description = 'বৈধতা'