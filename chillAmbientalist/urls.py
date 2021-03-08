"""chillAmbientalist URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# Django modules
from django.contrib import admin
# importar i18n_patterns (libro chapter 3)
from django.conf.urls.i18n import i18n_patterns
# añadir include
from django.urls import path, include
# importar settings y static para que funcione el añadir static
from django.conf import settings
from django.conf.urls.static import static
# importar redirect (libro chapter 3)
from django.shortcuts import redirect

app_name = 'chillAmbientalist'

urlpatterns = [
    path('admin/', admin.site.urls),
    # Path de templates/partials/index.html
    path('', include('gallery.urls')),
]

"""
url_patterns += static(settings.STATIC_URL,
document_root=settings.STATIC_ROOT)
urlpatterns += static("/uploads/", document_root=settings.MEDIA_ROOT)
"""

# ignorar aviso del VS
# IMPORTANTE

""" in urls.py
urlpatterns = [
    .....
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)"""

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static("/uploads/", document_root=settings.MEDIA_ROOT)
    urlpatterns += path('__debug__/', include(debug_toolbar.urls)),
