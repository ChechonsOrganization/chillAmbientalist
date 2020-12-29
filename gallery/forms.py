# Crear formulario para crear un post en la galeria
from django import forms
from .models import Comment, Contact
from django.forms import Textarea, TextInput


class CommentForm(forms.ModelForm):
    """
    Clase para construir el formulario para los comentarios
    necesitaremos el forms.ModelForm para construir el form
    dinamicamente para el modelo Comment.
    """

    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name' : TextInput(attrs={'class':'form-control'}),
            'email': TextInput(attrs={'class':'form-control'}),
            'body': Textarea(attrs={'class':'form-control'})
        }


class SearchForm(forms.Form):
    query = forms.CharField()


class ContactForm(forms.ModelForm):
    """ 
    Crear formulario de contacto
    """

    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
        widgets = {
            'name' : TextInput(attrs={'class':'form-control', 'placeholder':'Tu Nombre'}),
            'email': TextInput(attrs={'class':'form-control', 'placeholder':'Tu Email'}),
            'subject': TextInput(attrs={'class':'form-control', 'placeholder':'Asunto'}),
            'message': Textarea(attrs={'class':'form-control', 'placeholder':'Mensaje', 'cols':'30', 'rows':'7'})
        }



