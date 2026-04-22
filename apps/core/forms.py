from django import forms
from .models import SiteSettings


class SiteSettingsForm(forms.ModelForm):
    """Form for site settings management"""

    class Meta:
        model = SiteSettings
        fields = [
            'site_name', 'site_description', 'site_logo', 'site_favicon',
            'site_email', 'site_phone', 'site_address', 'footer_text',
            'facebook_url', 'instagram_url', 'twitter_url', 'youtube_url',
            'linkedin_url', 'whatsapp_number', 'theme', 'primary_color',
            'accent_color'
        ]
        widgets = {
            'site_name': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': 'Nom du site'
            }),
            'site_description': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 3,
                'placeholder': 'Description du site (pour SEO)'
            }),
            'site_email': forms.EmailInput(attrs={
                'class': 'input-field',
                'placeholder': 'contact@example.com'
            }),
            'site_phone': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '+212 6 00 00 00 00'
            }),
            'site_address': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 2,
                'placeholder': 'Adresse physique du site'
            }),
            'footer_text': forms.Textarea(attrs={
                'class': 'input-field',
                'rows': 2,
                'placeholder': 'Texte du footer (copyright, etc.)'
            }),
            'facebook_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://facebook.com/votrepage'
            }),
            'instagram_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://instagram.com/votrecompte'
            }),
            'twitter_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://twitter.com/votrecompte'
            }),
            'youtube_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://youtube.com/votrechaine'
            }),
            'linkedin_url': forms.URLInput(attrs={
                'class': 'input-field',
                'placeholder': 'https://linkedin.com/company/votrepage'
            }),
            'whatsapp_number': forms.TextInput(attrs={
                'class': 'input-field',
                'placeholder': '+212600000000'
            }),
            'theme': forms.Select(attrs={
                'class': 'input-field'
            }),
            'primary_color': forms.TextInput(attrs={
                'class': 'input-field',
                'type': 'color',
                'style': 'height: 42px; padding: 2px;'
            }),
            'accent_color': forms.TextInput(attrs={
                'class': 'input-field',
                'type': 'color',
                'style': 'height: 42px; padding: 2px;'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields optional (blank=True in model)
        for field in self.fields.values():
            field.required = False
