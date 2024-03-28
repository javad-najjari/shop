from .models import Category




def categories(request):
    all_categories = Category.objects.all()
    category_filter = [category for category in all_categories if category.products.count() > 0]

    return {
        'categories': category_filter
    }

