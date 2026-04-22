from django.db import models
from django.core.validators import URLValidator


class TimeStampedModel(models.Model):
    """
    Abstract base class that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SiteSettings(models.Model):
    """
    Site-wide settings model.
    Uses singleton pattern - only one instance should exist.
    """
    # Site Identity
    site_name = models.CharField(max_length=100, default='AutoMaroc')
    site_description = models.TextField(blank=True, help_text='Meta description for SEO')
    site_logo = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Site logo (recommended: 200x60px)')
    site_favicon = models.ImageField(upload_to='site/', blank=True, null=True, help_text='Favicon (recommended: 32x32px or 64x64px)')

    # Contact Information
    site_email = models.EmailField(max_length=255, blank=True, help_text='Contact email address')
    site_phone = models.CharField(max_length=50, blank=True, help_text='Contact phone number')
    site_address = models.TextField(blank=True, help_text='Physical address')

    # Footer
    footer_text = models.TextField(blank=True, help_text='Copyright text or footer message')

    # Social Media Links
    facebook_url = models.URLField(blank=True, validators=[URLValidator()], help_text='Facebook page URL')
    instagram_url = models.URLField(blank=True, validators=[URLValidator()], help_text='Instagram profile URL')
    twitter_url = models.URLField(blank=True, validators=[URLValidator()], help_text='Twitter/X profile URL')
    youtube_url = models.URLField(blank=True, validators=[URLValidator()], help_text='YouTube channel URL')
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()], help_text='LinkedIn page URL')
    whatsapp_number = models.CharField(max_length=20, blank=True, help_text='WhatsApp number (e.g., +212600000000)')

    # Theme
    THEME_CHOICES = [
        ('light', 'Light'),
        ('dark', 'Dark'),
        ('auto', 'Auto (System Preference)'),
    ]
    theme = models.CharField(max_length=10, choices=THEME_CHOICES, default='light', help_text='Default site theme')
    primary_color = models.CharField(max_length=7, default='#111827', help_text='Primary brand color (hex)')
    accent_color = models.CharField(max_length=7, default='#DC2626', help_text='Accent color (hex)')

    # Meta
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Settings'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        """Ensure only one instance exists"""
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create the singleton settings instance"""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings
