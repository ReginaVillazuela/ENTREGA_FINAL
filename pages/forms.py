from django import forms
from .models import Page, Comment

class PageForm(forms.ModelForm):
    class Meta:
        model = Page
        fields = ('title', 'subtitle', 'content', 'image', 'category')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Título del Paper'}),
            'content': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Contenido principal del paper', 'rows': 10}),
            # El campo category se renderizará como un <select> automáticamente
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={'class': 'shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline', 'placeholder': 'Añade tu comentario...', 'rows': 3}),
        }

