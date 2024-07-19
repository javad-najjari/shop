from .models import Category




def categories(request):
    
    # TODO: It must be stored in redis (9 queries)

    all_categories = Category.objects.all()
    category_filter = [category for category in all_categories if category.products.count() > 0]

    return {
        'categories': category_filter,
    }

