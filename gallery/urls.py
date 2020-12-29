# Importar path desde django.urls
from django.urls import path, re_path
# importar .views
from .views import ArticleYearArchiveView, ArticleMonthArchiveView, ArticleDayArchiveView

# Importar vistas de app gallery
from . import views

app_name='gallery'

urlpatterns = [
    path('', views.index, name='index'),
    path('gallery/', views.gallery, name='gallery'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('blog/', views.blog_list, name='blog'),
    path('blog/tag/<slug:tag_slug>/', views.blog_list, name='gallery_list_by_tag'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:gallery>', views.blog_detail, name='blog_detail'),
    #path('blog/<int:year>/<int:month>/<int:day>', views.ArticleDayArchiveView.as_view(day_format='%d'), name='show_day'),
    #path('blog/<int:year>/<int:month>/', views.ArticleMonthArchiveView.as_view(month_format='%m'), name='show_month'),
    #path('blog/<int:year>/', views.ArticleYearArchiveView.as_view(), name='show_year'),    
    path('category/<str:url_clean>/', views.CategoryView, name='category'),
    path('contact/', views.contact, name='contact'),
]
