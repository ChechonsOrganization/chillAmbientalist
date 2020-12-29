from django.db import models
from django.urls import reverse
from django.utils import timezone
# importar taggit para el uso de tags valga la redundancia
from taggit.managers import TaggableManager
# importar django stdimage
from stdimage import StdImageField, JPEGField
# importar signals para eliminar las imagenes
from django.dispatch import receiver
# importar los settings
from django.conf import settings
# importar User
from django.contrib.auth.models import User
# importar slugify para convertir el texto de las url limpias en slug de manera automatica
from django.utils.text import slugify
# importar os para eliminar imagenes
import os


class Category(models.Model):
    """
    Creacion de categoría para las publicaciones
    """
    title = models.CharField(max_length=255)
    url_clean = models.CharField(max_length=255)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    # definir modelo __str__
    def __str__(self):
        return self.title


class PublishedManager(models.Manager):
    """ 
    Custom manager para el modelo para las publicaciones de galeria
    que tengan el status de publicado ("published")
    """

    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Gallery(models.Model):
    """ 
    Clase gallery donde se almacenaran las imagenes con sus descripciones
    """
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="blog_galleries")
    title = models.CharField(("Title"), max_length=150)
    # se actualiza el url_clean: url_clean = models.CharField(max_length=255),
    # no es necesario la migracion para actualizar
    url_clean = models.SlugField(("Url_Clean"), max_length=255, unique_for_date='publish')
    description = models.CharField(("Description"), max_length=255)
    body = models.TextField(("Body"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category_galleries")
    # Fecha de publicado, creado y actualizado
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    # agregamos el tag para que el modelo sea etiquetable
    tags = TaggableManager()
    # status para ver si esta en borrador o publicado    
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    # Campos Custom Manager
    # Manager por default
    objects = models.Manager()
    # Nuestro custom manager
    published = PublishedManager()

    # funcion save para setear el url_clean de manera automatica escribir blank=True
    """def save(self, *args, **kwargs):
        self.url_clean = slugify(self.title)
        super(Gallery, self).save(*args, **kwargs)"""

    class Meta:
        # Remove parent's ordering effect
        ordering = ('-publish',)

    def __str__(self):
        return self.title

    # Usar el URL de post detail para definir la construccion de una URL canonica
    # para los objectos post, para eso usaremos el metodo reverse(), que nos permite construir URLs
    # por su nombre y pasarle parametros opcionales
    def get_absolute_url(self):
        return reverse('gallery:blog_detail', args=[self.publish.year, self.publish.month, self.publish.day, self.url_clean])


class Comment(models.Model):
    """ 
    Creacion del model de comentario para los posts
    """
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE, related_name='comments')
    name =  models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('-created',)
    
    def __str__(self):
        return f'Comentado por {self.name} en {self.post}'


class GalleryImages(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    # image = models.ImageField(upload_to='images/')
    # image = models.JPEGField(upload_to='images/', variations={'custom': {'width': 800, 'height': 700, "crop": True}})
    image = StdImageField(upload_to='images/',variations={'custom': {'width': 800, 'height': 700, "crop": True}})
    # para obtener el nombre de la imagen original
    original_image_name = models.CharField(max_length=100, default='')
    # para obtener la extension
    original_image_ext = models.CharField(max_length=5, default='')

    def __str__(self):
        return self.title

    # guardar campos de manera personalizada
    def save(self, *args, **kwargs):
        """
            Obtener la referencia del nombre original de la imagen como de su extensión
        """
        (root, ext) = os.path.splitext(self.image.path)
        """
            Quitar path absoluto del archivo, para solo dejar la carpeta donde este
            se guardará (images), el nombre de la imagen y su extension.

            Importamos y llamamos a settings para quitar path absoluto 
            que yace en la variable root y solo dejar la carpeta donde se subirá(images).
            Esto es para almacenar el nombre y carpeta de nuestras imagenes en la base de datos
            elementimages -> original_image_name que es lo mismo que -> image, solo que esté sera llamado y el image no

            Condiciones:
                1. Si el original_image_name está vacío porque no hay imagen subida,
                   la variable root elimina el path absoluto y agrega la carpeta donde esta se sube (images)
                2. Si el original_image_name no está vacío, quiere decir que se está actualizando
                   ya sea la imagen o solo su titulo, en este caso hay dos posibilidades, asi que
                   necesitaremos primero comprobar si la variable root contiene la carpeta de subida (images), luego:
                   2.1. Si hayamos que la variable "palabra" se encuentra en la variable "root" quiere decir que
                        estamos actualizando solo el titulo de la imagen, por lo cual tendremos que quitar
                        todo el path absoluto y agregar "images/" nuevamente, de otro modo se nos duplicará en la BBDD,
                        asi que reemplazamos la palabra "images\" y luego eliminamos el path absoluto para que no se duplique
                   2.2 Sino encuentran la palabra en el root significa que estamos actualizando por otra imagen, entonces solo
                        procedemos a eliminar el path absoluto y agregar el nombre de la carpeta de subida "images/" y asignarla
                        nuevamente a original_image_name
        """
        if (self.original_image_name == ""):
            root = root.replace(settings.MEDIA_ROOT+"\\", "images/")
            self.original_image_name = root
        elif (self.original_image_name != ""):
            # probar si root contene la palabra images\ para actualizar solo el titulo
            palabra = "images\\"
            if palabra in root.lower():
                root = root.replace('images\\', '')
                root = root.replace(settings.MEDIA_ROOT+"\\", "images/")
                self.original_image_name = root
            else:
                root = root.replace(settings.MEDIA_ROOT+"\\", "images/")
                self.original_image_name = root

        # guardar extensión de la imagen
        self.original_image_ext = ext

        # llamamos a la super clase para salvar datos
        super(GalleryImages, self).save(*args, **kwargs)


# Funcion para eliminar Imagenes Y sus CUSTOM al eliminar una imagen del registro en BBDD
# @receiver para estar atento cuando se borre para ser accionado
@receiver(models.signals.post_delete, sender=GalleryImages)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    # preguntar si la instancia (imagen original) existe
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)

    # obtener el nombre original de la imagen como de su extensión (custom)
    (root, ext) = os.path.splitext(instance.image.path)

    # sumamos el nombre de la imagen original mas su extensión
    extra_file = root+".custom.jpg"

    # preguntar si la imagen custom existe para eliminarla
    if os.path.isfile(extra_file):
        os.remove(extra_file)


# Funcion para eliminar Imagenes al ser actualizarlas del registro en BBDD
# @receiver para estar atento cuando se borre para ser accionado
@receiver(models.signals.pre_save, sender=GalleryImages)
def auto_delete_file_on_update(sender, instance, **kwargs):

    # preguntar si tenemos pk
    if not instance.pk:
        return False

    # para buscar al elemento por su pk y por image
    try:
        old_file = GalleryImages.objects.get(pk=instance.pk).image
    except GalleryImages.DoesNotExist:
        return False

    # comparamos si tenemos una imagen antigua para eliminarla del registro
    new_file = instance.image
    if not old_file == new_file:
        # preguntar si la instancia antigua existe
        if instance.image:
            if os.path.isfile(old_file.path):
                os.remove(old_file.path)

        # obtener el nombre original de la imagen como de su extensión (imagen custom)
        (root, ext) = os.path.splitext(old_file.path)

        # sumamos el nombre de la imagen original mas su extensión
        extra_old_file = root+".custom.jpg"

        # preguntar si la imagen custom existe para eliminarla
        if os.path.isfile(extra_old_file):
            os.remove(extra_old_file)


class Contact(models.Model):
    """
    Creacion del model de contacto
    """
    name = models.CharField(max_length=80)
    email = models.EmailField()
    subject = models.CharField(max_length=80)
    message = models.TextField(max_length=500)

    def __str__(self):
        return self.email