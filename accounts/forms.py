from django import forms
from .models import Profile

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'title', 'image']
        widgets = {
            # Usamos DateInput para asegurar que el navegador muestre un selector de fecha
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
        }