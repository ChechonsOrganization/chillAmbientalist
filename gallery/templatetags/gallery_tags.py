"""
Custom template tags
"""

from django import template
from django.db.models import Count
from ..models import Gallery

# Importes de Custom Filter
# from django.utils.safestring import mark_safe
# import markdown


register = template.Library()


@register.simple_tag
def total_galleries():
    """
    Crear un simple tag que retorne el
    numero de galleries publicados
    """
    return Gallery.published.count()


@register.inclusion_tag('latest_galleries.html')
# Corregir para listar las fotos
def show_latest_posts(count=6):
    """ 
    Crear inclusion tag para mostrar los ultimos
    6 galleries publicados en un sidebar o footer reutilizable por vistas
    """
    latest_galleries = Gallery.published.select_related('author').prefetch_related('galleryimages_set').order_by('-publish') [:count]
    latest_galleries_images = latest_galleries.prefetch_related('galleryimages_set')
    return {'latest_galleries': latest_galleries,}


@register.simple_tag
def get_most_commented_galleries(count=4):
    """ 
    Crear un simple tag que retorne las galleries mas populares
    en este caso seran los que tienen mas comentarios
    """
    commented_galleries = Gallery.published.prefetch_related('author','galleryimages_set').annotate(total_comments=Count('comments')).order_by('-total_comments') [:count]
    return commented_galleries


