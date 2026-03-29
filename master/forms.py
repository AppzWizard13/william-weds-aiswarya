from django import forms
from .models import Category, SubCategory, Product, Discount, DeliveryZone

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'description', 'image', 'is_active']

class SubCategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ['category', 'name', 'slug', 'description', 'image', 'is_active']

# ✅ ENHANCED ProductForm with Custom Error Messages & Validation
from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ['vendor', 'views', 'rating', 'total_reviews', 'created_at', 'updated_at']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': 'Enter detailed product description...',
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'discount_price': forms.NumberInput(attrs={'step': '0.01'}),
            'min_order_quantity': forms.NumberInput(attrs={'step': '0.01'}),
        }
    
    # Custom error messages for ALL fields
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Custom error messages for better UX
        self.fields['name'].error_messages = {
            'required': 'Product name is required',
            'max_length': 'Name must be less than 200 characters',
        }
        self.fields['category'].error_messages = {
            'required': 'Please select a category',
            'invalid_choice': 'Invalid category selected',
        }
        self.fields['subcategory'].error_messages = {
            'invalid_choice': 'Invalid subcategory selected',
        }
        self.fields['price'].error_messages = {
            'required': 'Price is required',
            'invalid': 'Enter a valid price (e.g. 99.99)',
            'max_digits': 'Price too large',
            'max_decimal_places': 'Too many decimal places',
            'min_value': 'Price cannot be negative',
        }
        self.fields['discount_price'].error_messages = {
            'invalid': 'Enter a valid discount price (e.g. 79.99)',
            'max_digits': 'Discount price too large',
            'max_decimal_places': 'Too many decimal places',
            'min_value': 'Discount price cannot be negative',
        }
        self.fields['stock'].error_messages = {
            'required': 'Stock quantity is required',
            'invalid': 'Enter a valid stock number',
            'max_value': 'Stock quantity too large',
        }
        self.fields['unit'].error_messages = {
            'required': 'Please select a unit',
            'invalid_choice': 'Invalid unit selected',
        }
        self.fields['min_order_quantity'].error_messages = {
            'required': 'Minimum order quantity is required',
            'invalid': 'Enter a valid minimum order quantity',
            'min_value': 'Minimum order must be at least 0.01',
        }
        self.fields['preparation_time'].error_messages = {
            'required': 'Preparation time is required',
            'invalid': 'Enter a valid preparation time',
            'max_value': 'Preparation time too large',
        }
        self.fields['description'].error_messages = {
            'required': 'Product description is required',
        }
        self.fields['image'].error_messages = {
            'required': 'Primary product image is required',
            'invalid_image': 'Upload a valid image. Only JPG/PNG allowed.',
            'max_length': 'File path too long',
        }
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name:
            raise ValidationError('Product name cannot be empty')
        if len(name.strip()) < 2:
            raise ValidationError('Product name must be at least 2 characters long')
        return name.strip()
    
    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price and price <= 0:
            raise ValidationError('Price must be greater than 0')
        return price
    
    def clean_discount_price(self):
        discount_price = self.cleaned_data.get('discount_price')
        price = self.cleaned_data.get('price')
        
        if discount_price and price:
            if discount_price >= price:
                raise ValidationError('Discount price must be less than regular price')
        return discount_price
    
    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (5MB)
            if image.size > 5 * 1024 * 1024:
                raise ValidationError('Image file size must be less than 5MB')
            
            # Check file extension
            valid_extensions = ['jpg', 'jpeg', 'png']
            ext = image.name.lower().rsplit('.', 1)[-1]
            if ext not in valid_extensions:
                raise ValidationError('Only JPG, JPEG, PNG images are allowed')
        return image
    
    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get('price')
        discount_price = cleaned_data.get('discount_price')
        
        # Business logic validation
        if price and discount_price and discount_price >= price:
            self.add_error('discount_price', 'Discount must be less than regular price')
        
        if not cleaned_data.get('category'):
            self.add_error('category', 'Category selection is required')
        
        return cleaned_data

class DiscountForm(forms.ModelForm):
    class Meta:
        model = Discount
        exclude = ['used_count', 'created_at', 'updated_at']
        widgets = {
            'valid_from': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'valid_to': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class DeliveryZoneForm(forms.ModelForm):
    class Meta:
        model = DeliveryZone
        fields = '__all__'
        widgets = {
            'cities': forms.Textarea(attrs={'rows': 2, 'placeholder': 'City1, City2...'}),
            'pincodes': forms.Textarea(attrs={'rows': 2, 'placeholder': '682001, 682002...'}),
        }
