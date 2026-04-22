from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.utils.text import slugify
from .models import Car, CarImage


@receiver(pre_save, sender=Car)
def set_car_slug(sender, instance, **kwargs):
    """Generate slug for car if not set"""
    if not instance.slug and instance.brand and instance.model_name:
        base_slug = slugify(f"{instance.brand.name}-{instance.model_name}-{instance.year}")
        instance.slug = base_slug


@receiver(post_save, sender=Car)
def update_car_slug_with_id(sender, instance, created, **kwargs):
    """Update slug to include car ID for uniqueness after creation"""
    if created and instance.slug and str(instance.id) not in instance.slug:
        instance.slug = f"{instance.slug}-{instance.id}"
        instance.save(update_fields=['slug'])


@receiver(pre_save, sender=CarImage)
def ensure_single_featured_image(sender, instance, **kwargs):
    """Ensure only one featured image per car"""
    if instance.is_featured:
        # Get existing featured images for this car
        existing_featured = CarImage.objects.filter(
            car=instance.car, 
            is_featured=True
        ).exclude(id=instance.id)
        
        # Set them to not featured
        existing_featured.update(is_featured=False)
