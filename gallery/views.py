# Django modules
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, reverse, get_object_or_404
# importar paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# importar vistas genericas
from django.views import generic
# importar vistas genericas por fechas
from django.views.generic.dates import YearArchiveView, MonthArchiveView, DayArchiveView
# importar vistas genericas
from django.views.generic.list import ListView
# Current-app modules
# importamos el modelo Element, Category de la app listelement
# from .forms import GalleryForm
from .models import Gallery, Category, Contact
# Third-party libraries
# cargar el modelo tag
from taggit.models import Tag
# Importar Count
from django.db.models import Count
# cargar forms
from .forms import CommentForm, ContactForm


# Creación de las vistas


def index(request):
    """
   Vista Inicio, raiz del sitio.
   """
    # return render(request,'index_page.html',{'comments_page':comments_page})

    gallery = Gallery.objects.all()
    gallery = Gallery.objects.prefetch_related('galleryimages_set')
    gallery = gallery.all()

    return render(request, 'index.html', {'gallery_images': gallery})


def gallery(request):
    """
      Vista Galería
    """
    # obtener el listado de los tags
    gallery = Gallery.objects.all()

    # iba en el if de search
    gallery = Gallery.objects.prefetch_related('category', 'galleryimages_set')

    # gallery = gallery.all()

    # crear instancia de paginator
    paginator = Paginator(gallery, 9)
    # obtener el listado de los tags
    # categories = Category.objects.all()
    # obtener el listado de los tags
    # tags = Tag.objects.all()
    page_number = request.GET.get('page')
    gallery_page = paginator.get_page(page_number)

    return render(request, 'gallery.html', {'gallery': gallery_page, })


def about(request):
    """
        Vista Acerca de
    """
    return render(request, 'about.html')


def services(request):
    """
        Vista Mis Servicios
    """
    return render(request, 'services.html')


def blog_list(request, tag_slug=None):
    """
       Vista Lista de Blog
       Se le pasa tag_slug de manera opcional por la URL
    """
    # Obtener el listado de toda la galeria de fotos
    object_list = Gallery.objects.all()
    # Relacionar con category y galleryimages
    object_list = Gallery.objects.select_related('author').prefetch_related('category', 'galleryimages_set')
    # Añadir tag
    tag = None

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    # crear instancia de paginator
    paginator = Paginator(object_list, 5)
    # obtener el listado de las categorías
    categories = Category.objects.all()
    # obtener el listado de los tags
    # tags = Tag.objects.all()
    page = request.GET.get('page')

    try:
        galleries = paginator.page(page)
    except PageNotAnInteger:
        # Si la pagina no es un int devolver la primera pagina
        galleries = paginator.page(1)
    except EmptyPage:
        # Si la pagina esta fuera de rango se entrega la ultima pagina de los resultados
        galleries = paginator.page(paginator.num_pages)

    return render(request, 'blog_list.html',
                  {'page': page, 'galleries': galleries, 'categories': categories, 'tag': tag})


# url_clean en lugar de gallery
def blog_detail(request, year, month, day, gallery):
    """
   Vista Detalle de un Blog
   """
    # gallery = get_object_or_404(Gallery, url_clean=url_clean) cambiar en urls
    gallery = get_object_or_404(Gallery.objects.select_related('author'),
                                url_clean=gallery,
                                status='published',
                                publish__year=year,
                                publish__month=month,
                                publish__day=day)

    # Lista de comentarios activos para este post
    comments = gallery.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        # Un comentario fue publicado
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Crear objeto Comment pero sin guardarlo en la bd todavia
            new_comment = comment_form.save(commit=False)
            # Asignar el post gallery actual al comentario
            new_comment.gallery = gallery
            # Guardar el comentario en la bd
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    # Lista de post similares
    gallery_tags_ids = gallery.tags.values_list('id', flat=True)
    similar_posts = Gallery.published.prefetch_related('galleryimages_set').filter(tags__in=gallery_tags_ids).exclude(
        id=gallery.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    return render(request, 'blog_detail.html', {'gallery': gallery,
                                                'comments': comments,
                                                'new_comment': new_comment,
                                                'comment_form': comment_form,
                                                'similar_posts': similar_posts})


"""
class BlogView(generic.ListView):
   model = Gallery
   template_name = 'gallery/blog_detail.html'
   slug_field = 'url_clean'
   slug_url_kwarg = 'url_clean'
"""


class ArticleYearArchiveView(YearArchiveView):
    paginate_by = 5
    model = Gallery
    template_name = 'blogger_detail.html'
    #context_object_name = 'gallery'
    queryset = Gallery.objects.all().prefetch_related('category', 'galleryimages_set')
    date_field = 'created'
    make_object_list = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.all().prefetch_related('category', 'galleryimages_set').filter(
            created__year=kwargs['year'].year)
        return context


class ArticleMonthArchiveView(MonthArchiveView):
    paginate_by = 5
    template_name = 'blogger_detail.html'
    date_field = 'created'
    queryset = Gallery.objects.all().prefetch_related('category', 'galleryimages_set')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.all().prefetch_related('category', 'galleryimages_set').filter(
            created__year=kwargs['month'].year).filter(created__month=kwargs['month'].month)
        return context


class ArticleDayArchiveView(DayArchiveView):
    queryset = Gallery.objects.all()
    date_field = 'created'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['gallery'] = Gallery.objects.all().prefetch_related('category', 'galleryimages_set').filter(
            created__year=kwargs['day'].year).filter(created__month=kwargs['day'].month).filter(
            created__day=kwargs['day'].day)
        return context


def CategoryView(request, url_clean):
    # category_posts = Gallery.objects.all().prefetch_related('category').filter(category=url_clean)

    # Crear una variable categoria y pasarla la url limpia
    categories = get_object_or_404(Category, url_clean=url_clean)
    # Crear una variable de publicaciones filtradas por su categoria
    category_posts = Gallery.objects.prefetch_related('category', 'galleryimages_set').filter(category=categories)

    paginator = Paginator(category_posts, 5)
    page_number = request.GET.get('page')
    category_page = paginator.get_page(page_number)

    return render(request, 'categories.html', {'url_clean': url_clean, 'category_posts': category_page})


def contact(request):
    if request.method == 'POST':
        # Un comentario fue publicado
        contact_form = ContactForm(data=request.POST)
        if contact_form.is_valid():
            contact = Contact()
            contact.name = contact_form.cleaned_data['name']
            contact.email = contact_form.cleaned_data['email']
            contact.subject = contact_form.cleaned_data['subject']
            contact.message = contact_form.cleaned_data['message']
            contact.save()

            messages.add_message(request, messages.INFO, 'Contacto recibido')

            return redirect('gallery:contact')
    else:
        contact_form = ContactForm()

    return render(request, 'contact.html', {'contact_form': contact_form})
