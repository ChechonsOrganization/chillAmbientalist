from django.contrib import admin
# importar modelos
from .models import Gallery, Category, GalleryImages

# Register your models here.

# crear clase para administrar las imagenes de los productos
class GalleryImagesInLine(admin.StackedInline):
    exclude = ('original_image_name','original_image_ext')
    model = GalleryImages
    extra = 3

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'url_clean', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'url_clean': ('title',)}
    raw_id_fields = ('author',)
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    inlines = [GalleryImagesInLine]

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    prepopulated_fields = {'url_clean': ('title',)}

"""
class TypeAdmin(ImportExportModelAdmin):
    resource_class = TypeResource
    list_display = ('id','title')
"""

#class ElementAdmin(admin.ModelAdmin):
#    list_display = ('id', 'title','description','category','type')

#admin.site.register(Type, TypeAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Gallery, GalleryAdmin)
