from django import template


register = template.Library()



@register.inclusion_tag('product/partials/product_list.html')
def product_list(products):
    return {'products': products}

