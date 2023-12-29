from django.contrib import admin
from .models import Review, Category, Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'quantity', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Review)