from django.conf import settings
from .models import SiteSettings


def site_settings(request):
    """
    Context processor to add site settings to all templates.
    Loads from database, with Django settings as fallback.
    """
    # Get settings from database
    try:
        db_settings = SiteSettings.get_settings()
    except:
        # If table doesn't exist yet (migrations not run), use defaults
        db_settings = None

    # Build context with database values or fallbacks
    context = {
        # Core site info
        'SITE_NAME': db_settings.site_name if db_settings else getattr(settings, 'SITE_NAME', 'AutoMaroc'),
        'SITE_DESCRIPTION': db_settings.site_description if db_settings else '',
        'SITE_LOGO': db_settings.site_logo.url if db_settings and db_settings.site_logo else None,
        'SITE_FAVICON': db_settings.site_favicon.url if db_settings and db_settings.site_favicon else None,
        'SITE_URL': getattr(settings, 'SITE_URL', 'http://localhost:8000'),

        # Contact info
        'SITE_EMAIL': db_settings.site_email if db_settings else '',
        'SITE_PHONE': db_settings.site_phone if db_settings else '',
        'SITE_ADDRESS': db_settings.site_address if db_settings else '',
        'WHATSAPP_NUMBER': db_settings.whatsapp_number if db_settings else getattr(settings, 'WHATSAPP_NUMBER', ''),

        # Footer
        'FOOTER_TEXT': db_settings.footer_text if db_settings else '',

        # Social media
        'FACEBOOK_URL': db_settings.facebook_url if db_settings else '',
        'INSTAGRAM_URL': db_settings.instagram_url if db_settings else '',
        'TWITTER_URL': db_settings.twitter_url if db_settings else '',
        'YOUTUBE_URL': db_settings.youtube_url if db_settings else '',
        'LINKEDIN_URL': db_settings.linkedin_url if db_settings else '',

        # Theme
        'SITE_THEME': db_settings.theme if db_settings else 'light',
        'PRIMARY_COLOR': db_settings.primary_color if db_settings else '#111827',
        'ACCENT_COLOR': db_settings.accent_color if db_settings else '#DC2626',

        # Debug
        'DEBUG': getattr(settings, 'DEBUG', False),
    }

    # Also add the full settings object for advanced use
    if db_settings:
        context['DB_SITE_SETTINGS'] = db_settings

    return context
