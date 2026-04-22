from django import forms
from .models import Car, Category, Brand, Feature, CarImage


class CarForm(forms.ModelForm):
    """Form for creating/editing cars"""
    
    class Meta:
        model = Car
        fields = ['title', 'slug', 'category', 'brand', 'model_name', 'year', 
                  'mileage', 'fuel_type', 'transmission', 'horsepower', 'engine_size',
                  'drivetrain', 'color', 'doors', 'seats', 'condition',
                  'vin_number', 'registration_city', 'description', 'price',
                  'negotiable_price', 'featured', 'status', 'published', 'features']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Titre de l\'annonce'}),
            'slug': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'url-slug-auto-generated'}),
            'model_name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ex: Classe C'}),
            'year': forms.NumberInput(attrs={'class': 'input-field', 'min': 1900, 'max': 2030}),
            'mileage': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Kilométrage en km'}),
            'horsepower': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Ex: 150'}),
            'engine_size': forms.NumberInput(attrs={'class': 'input-field', 'step': '0.1', 'placeholder': 'Ex: 2.0'}),
            'color': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ex: Noir métallisé'}),
            'doors': forms.NumberInput(attrs={'class': 'input-field', 'min': 2, 'max': 5}),
            'seats': forms.NumberInput(attrs={'class': 'input-field', 'min': 2, 'max': 9}),
            'vin_number': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'N° de série (VIN)'}),
            'registration_city': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Ex: Casablanca'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 5, 'placeholder': 'Description détaillée du véhicule...'}),
            'price': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Prix en MAD'}),
            'category': forms.Select(attrs={'class': 'input-field'}),
            'brand': forms.Select(attrs={'class': 'input-field'}),
            'fuel_type': forms.Select(attrs={'class': 'input-field'}),
            'transmission': forms.Select(attrs={'class': 'input-field'}),
            'drivetrain': forms.Select(attrs={'class': 'input-field'}),
            'condition': forms.Select(attrs={'class': 'input-field'}),
            'status': forms.Select(attrs={'class': 'input-field'}),
            'features': forms.CheckboxSelectMultiple(),
        }


class CarFilterForm(forms.Form):
    """Form for filtering cars on listing page"""
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label='Toutes les marques',
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.filter(is_active=True),
        required=False,
        empty_label='Toutes les catégories',
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    price_min = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Prix min'})
    )
    price_max = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Prix max'})
    )
    year_min = forms.IntegerField(
        required=False,
        min_value=1900,
        max_value=2030,
        widget=forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Année min'})
    )
    fuel_type = forms.ChoiceField(
        choices=[('', 'Tous')] + Car.FUEL_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    transmission = forms.ChoiceField(
        choices=[('', 'Toutes')] + Car.TRANS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'input-field'})
    )
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Rechercher...'})
    )


class CategoryForm(forms.ModelForm):
    """Form for creating/editing categories"""
    
    class Meta:
        model = Category
        fields = ['name', 'slug', 'icon', 'description', 'is_active', 'order']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'slug': forms.TextInput(attrs={'class': 'input-field'}),
            'description': forms.Textarea(attrs={'class': 'input-field', 'rows': 3}),
            'order': forms.NumberInput(attrs={'class': 'input-field'}),
        }


class BrandForm(forms.ModelForm):
    """Form for creating/editing brands"""
    
    class Meta:
        model = Brand
        fields = ['name', 'slug', 'logo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'slug': forms.TextInput(attrs={'class': 'input-field'}),
        }


class FeatureForm(forms.ModelForm):
    """Form for creating/editing features"""
    
    class Meta:
        model = Feature
        fields = ['name', 'icon']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field'}),
            'icon': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'fas fa-car'}),
        }


class CarImageForm(forms.ModelForm):
    """Form for uploading car images"""
    
    class Meta:
        model = CarImage
        fields = ['image', 'alt_text', 'is_featured', 'order']
        widgets = {
            'image': forms.ClearableFileInput(attrs={'class': 'input-field'}),
            'alt_text': forms.TextInput(attrs={'class': 'input-field'}),
            'order': forms.NumberInput(attrs={'class': 'input-field'}),
        }


class CarImageInlineFormSet(forms.BaseInlineFormSet):
    """Inline formset for car images"""
    pass


# Create inline formset factory
CarImageFormSet = forms.inlineformset_factory(
    Car,
    CarImage,
    form=CarImageForm,
    formset=CarImageInlineFormSet,
    extra=6,  # Show 6 empty forms for batch upload
    max_num=15,  # Maximum 15 images per car
    can_delete=True
)
