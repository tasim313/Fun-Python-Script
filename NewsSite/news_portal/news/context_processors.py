from .models import Category, Advertisement
from django.utils import timezone


def global_context(request):
    """Global context processor for common data"""
    
    # Main navigation categories
    main_categories = Category.objects.filter(
        is_active=True,
        parent=None
    ).prefetch_related('children')
    
    # Active advertisements
    now = timezone.now()
    ads = {
        'top_banner': Advertisement.objects.filter(
            ad_location='top_banner',
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first(),
        'sidebar': Advertisement.objects.filter(
            ad_location='sidebar',
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        )[:3],
        'bottom_banner': Advertisement.objects.filter(
            ad_location='bottom_banner',
            is_active=True,
            start_date__lte=now,
            end_date__gte=now
        ).first(),
    }
    
    return {
        'main_categories': main_categories,
        'ads': ads,
    }