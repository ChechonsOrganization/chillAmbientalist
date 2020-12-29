# para llamar la variable de galeria desde los templates
# importamos django db
from django.db import models
# importamos modelo
from .models import Gallery, Category
# cargar el modelo tag
from taggit.models import Tag

def add_gallery_to_context(request):

    """
    # obtener el listado de los tags
    gallery = Gallery.objects.all()

    # iba en el if de search 
    gallery = Gallery.objects.prefetch_related('galleryimages_set')

    gallery = gallery.all()

    # crear instancia de paginator
    paginator = Paginator(gallery, 9)
    # obtener el listado de los tags
    
    # obtener el listado de los tags
    
    page_number = request.GET.get('page')
    gallery_page = paginator.get_page(page_number)
    """
    categories = Category.objects.all()
    tags = Tag.objects.all()

    gallery = Gallery.objects.all()
    gallery = Gallery.objects.order_by('created')

    gallery_months = Gallery.objects.dates('created','month','DESC')

    gallery = Gallery.objects.prefetch_related('galleryimages_set')
    #gallery = gallery.all()

    return {'gallery_images': gallery, 'gallery_months':gallery_months, 'categories':categories, 'tags':tags}