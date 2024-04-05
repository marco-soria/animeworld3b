from django.contrib import admin
from django.utils.text import slugify

# Register your models here.
from .models import (
    Category,
    Product
)

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'category', 'created_at')
    list_filter = ('category',)  # Filtrado por categoría

# Registra el modelo Product con su respectivo admin personalizado
admin.site.register(Product, ProductAdmin)

# Define una función para generar el slug automáticamente
def generate_slug(modeladmin, request, queryset):
    for obj in queryset:
        obj.slug = slugify(obj.name)
        obj.save()

generate_slug.short_description = "Generate slug for selected categories"

# Define la clase CategoryAdmin para personalizar el admin de Category
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    actions = [generate_slug]  # Agrega la acción para generar slugs automáticamente

# Registra el modelo Category con su respectivo admin personalizado
admin.site.register(Category, CategoryAdmin)