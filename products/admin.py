from django.contrib import admin
from django.utils.html import format_html
from .models import Product, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display  = ['thumbnail', 'name', 'category', 'brand', 'price', 'rating', 'stock', 'is_featured']
    list_filter   = ['category', 'brand', 'is_featured']
    search_fields = ['name', 'description', 'brand']
    list_editable = ['price', 'stock', 'is_featured']
    readonly_fields = ['image_preview']

    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'description', 'category', 'brand')
        }),
        ('Image', {
            'fields': ('image', 'image_preview'),   # upload field + live preview
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'rating', 'stock')
        }),
        ('Flags', {
            'fields': ('is_featured',)
        }),
    )

    # Small thumbnail in the list view
    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width:48px;height:48px;'
                'object-fit:cover;border-radius:6px;" />',
                obj.image.url
            )
        return '—'
    thumbnail.short_description = 'Image'

    # Larger preview inside the edit form
    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width:200px;max-height:200px;'
                'object-fit:contain;border-radius:8px;border:1px solid #ddd;" />',
                obj.image.url
            )
        return 'No image uploaded yet.'
    image_preview.short_description = 'Current Image'
