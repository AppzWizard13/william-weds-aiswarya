from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from .models import Category, SubCategory, Product, Discount, DeliveryZone
from .forms import CategoryForm, SubCategoryForm, ProductForm, DiscountForm, DeliveryZoneForm
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.db.models import Q
import json

from .models import Product, ProductImage, Category, SubCategory
from .forms import ProductForm

class SoftDeleteMixin:
    """Toggles is_active to False instead of deleting from DB."""
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.is_active = False
        self.object.save()
        return redirect(self.get_success_url())

# --- CATEGORY VIEWS ---
class CategoryListView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'master/category_list.html'
    context_object_name = 'categories'
    paginate_by = 10

class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'master/category_form.html'
    success_url = reverse_lazy('master:category_list')

class CategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'master/category_form.html'
    success_url = reverse_lazy('master:category_list')

class CategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = Category
    success_url = reverse_lazy('master:category_list')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        messages.success(request, f'Category "{category.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


# --- SUBCATEGORY VIEWS ---
class SubCategoryListView(LoginRequiredMixin, ListView):
    model = SubCategory
    template_name = 'master/subcategory_list.html'
    context_object_name = 'subcategories'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.request.GET.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset.select_related('category')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['selected_category'] = self.request.GET.get('category', '')
        return context


class SubCategoryCreateView(LoginRequiredMixin, CreateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'master/subcategory_form.html'
    success_url = reverse_lazy('master:subcategory_list')
    
    def get_initial(self):
        initial = super().get_initial()
        # Pre-select category if passed in URL
        category_id = self.request.GET.get('category')
        if category_id:
            try:
                initial['category'] = Category.objects.get(id=category_id)
            except Category.DoesNotExist:
                pass
        return initial
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = False
        return context


class SubCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = SubCategory
    form_class = SubCategoryForm
    template_name = 'master/subcategory_form.html'
    success_url = reverse_lazy('master:subcategory_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_edit'] = True
        return context


class SubCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = SubCategory
    success_url = reverse_lazy('master:subcategory_list')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        subcategory = self.get_object()
        messages.success(request, f'SubCategory "{subcategory.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)



# --- PRODUCT VIEWS (With Vendor Isolation) ---
class ProductListView(LoginRequiredMixin, ListView):
    model = Product
    template_name = 'master/product_list.html'
    context_object_name = 'products'
    
    def get_queryset(self):
        qs = super().get_queryset()
        if not self.request.user.is_superuser and hasattr(self.request.user, 'vendor'):
            qs = qs.filter(vendor=self.request.user.vendor)
        return qs

from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from .models import Product
from .forms import ProductForm

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'master/product_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_action'] = 'create'
        context['page_title'] = 'Add New Product'
        return context
    
    def form_valid(self, form):
        try:
            # Automatically assign vendor for non-superusers
            if not self.request.user.is_superuser:
                form.instance.vendor = self.request.user.vendor
                
            response = super().form_valid(form)
            messages.success(
                self.request, 
                f'✅ Product "{form.instance.name}" created successfully! '
                f'You can now add gallery images.'
            )
            return response
            
        except Exception as e:
            messages.error(
                self.request,
                f'❌ Failed to create product: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        messages.error(
            self.request,
            '⚠️ Please correct the errors below and try again.'
        )
        return super().form_invalid(form)
    
    def get_success_url(self):
        # Return to edit page if we want to add gallery images immediately
        if 'save_and_add_images' in self.request.POST:
            return reverse('master:product_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('master:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'master/product_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['view_action'] = 'update'
        context['object'] = self.object  # This is important!
        context['page_title'] = f'Edit Product - {self.object.name}'
        return context
    
    def get_queryset(self):
        # Only allow editing own products or superuser
        qs = super().get_queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(vendor=self.request.user.vendor)
        return qs
    
    def form_valid(self, form):
        try:
            response = super().form_valid(form)
            
            # Different success messages based on action
            if 'save_and_continue' in self.request.POST:
                messages.success(
                    self.request,
                    f'✅ Product "{form.instance.name}" updated successfully! '
                    f'Continuing with gallery images...'
                )
                return redirect('master:product_update', pk=form.instance.pk)
            else:
                messages.success(
                    self.request,
                    f'✅ Product "{form.instance.name}" updated successfully!'
                )
            return response
            
        except Exception as e:
            messages.error(
                self.request,
                f'❌ Failed to update product: {str(e)}'
            )
            return self.form_invalid(form)
    
    def form_invalid(self, form):
        # More specific error messages
        errors = []
        for field, field_errors in form.errors.items():
            if field != '__all__':
                errors.append(f"{form[field].label}: {', '.join(field_errors)}")
            else:
                errors.append(', '.join(field_errors))
        
        if errors:
            messages.error(
                self.request,
                f'⚠️ Please fix these errors:<br><ul><li>{"</li><li>".join(errors)}</li></ul>',
                extra_tags='safe'
            )
        else:
            messages.error(
                self.request,
                '⚠️ Please correct the form errors below and try again.'
            )
        
        return super().form_invalid(form)
    
    def get_success_url(self):
        if 'save_and_continue' in self.request.POST:
            return reverse('master:product_update', kwargs={'pk': self.object.pk})
        elif 'save_and_add_images' in self.request.POST:
            return reverse('master:product_update', kwargs={'pk': self.object.pk})
        return reverse_lazy('master:product_list')


class ProductDeleteView(LoginRequiredMixin, SoftDeleteMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('master:product_list')
    template_name = 'master/confirm_delete.html'

    def delete(self, request, *args, **kwargs):
        product = self.get_object()
        messages.success(request, f'Product "{product.name}" deleted successfully!')
        return super().delete(request, *args, **kwargs)


# ==================== AJAX VIEWS FOR IMAGE HANDLING ====================

class UploadGalleryImageView(LoginRequiredMixin, View):
    """
    AJAX view for uploading gallery images
    """
    def post(self, request, *args, **kwargs):
        try:
            if not request.FILES.get('image'):
                return JsonResponse({'success': False, 'error': 'No image provided'})
            
            product_id = request.POST.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID required'})
            
            # Get product with vendor isolation
            product_qs = Product.objects.all()
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                product_qs = product_qs.filter(vendor=request.user.vendor)
            
            product = get_object_or_404(product_qs, id=product_id)
            
            image_file = request.FILES['image']
            
            # Validate file size (5MB limit)
            if image_file.size > 5 * 1024 * 1024:
                return JsonResponse({'success': False, 'error': 'File size exceeds 5MB'})
            
            # Validate file type
            if not image_file.content_type.startswith('image/'):
                return JsonResponse({'success': False, 'error': 'File must be an image'})
            
            # Create gallery image
            gallery_image = ProductImage.objects.create(
                product=product,
                image=image_file
            )
            
            return JsonResponse({
                'success': True,
                'image': {
                    'id': gallery_image.id,
                    'url': gallery_image.image.url,
                    'filename': image_file.name,
                    'size': image_file.size
                }
            })
            
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class DeleteGalleryImageView(LoginRequiredMixin, View):
    """
    AJAX view for deleting gallery images
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            
            if not image_id:
                return JsonResponse({'success': False, 'error': 'Image ID required'})
            
            # Get image with product vendor check
            image = get_object_or_404(ProductImage, id=image_id)
            
            # Check vendor permission
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                if image.product.vendor != request.user.vendor:
                    return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            # Store info for response
            image_url = image.image.url if image.image else None
            
            # Delete the image (file will be deleted by signal or manually)
            image.delete()
            
            return JsonResponse({
                'success': True,
                'message': 'Image deleted successfully',
                'image_url': image_url
            })
            
        except ProductImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class SetPrimaryImageView(LoginRequiredMixin, View):
    """
    AJAX view for setting primary image
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            image_id = data.get('image_id')
            product_id = data.get('product_id')
            
            if not image_id or not product_id:
                return JsonResponse({'success': False, 'error': 'Image ID and Product ID required'})
            
            # Get image with product vendor check
            image = get_object_or_404(ProductImage, id=image_id, product_id=product_id)
            
            # Check vendor permission
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                if image.product.vendor != request.user.vendor:
                    return JsonResponse({'success': False, 'error': 'Permission denied'})
            
            # Remove primary flag from all images of this product
            ProductImage.objects.filter(product_id=product_id).update(is_primary=False)
            
            # Set this image as primary
            image.is_primary = True
            image.save()
            
            # Also update the main product image if needed
            product = image.product
            if not product.image:  # If no main image, set this as main
                product.image = image.image
                product.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Primary image updated successfully',
                'image_url': image.image.url,
                'image_id': image.id
            })
            
        except ProductImage.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Image not found'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class ToggleProductStatusView(LoginRequiredMixin, View):
    """
    AJAX view for toggling product active status
    """
    def post(self, request, pk, *args, **kwargs):
        try:
            # Get product with vendor isolation
            product_qs = Product.objects.all()
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                product_qs = product_qs.filter(vendor=request.user.vendor)
            
            product = get_object_or_404(product_qs, pk=pk)
            
            # Toggle status
            product.is_active = not product.is_active
            product.save()
            
            status_text = "activated" if product.is_active else "deactivated"
            
            return JsonResponse({
                'success': True,
                'is_active': product.is_active,
                'message': f'Product {status_text} successfully'
            })
            
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class BulkUploadGalleryImagesView(LoginRequiredMixin, View):
    """
    AJAX view for bulk uploading multiple gallery images
    """
    def post(self, request, *args, **kwargs):
        try:
            files = request.FILES.getlist('images')
            product_id = request.POST.get('product_id')
            
            if not files:
                return JsonResponse({'success': False, 'error': 'No images provided'})
            
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID required'})
            
            # Get product with vendor isolation
            product_qs = Product.objects.all()
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                product_qs = product_qs.filter(vendor=request.user.vendor)
            
            product = get_object_or_404(product_qs, id=product_id)
            
            uploaded_images = []
            errors = []
            
            for image_file in files:
                try:
                    # Validate file size (5MB limit)
                    if image_file.size > 5 * 1024 * 1024:
                        errors.append(f'{image_file.name}: File size exceeds 5MB')
                        continue
                    
                    # Validate file type
                    if not image_file.content_type.startswith('image/'):
                        errors.append(f'{image_file.name}: File must be an image')
                        continue
                    
                    # Create gallery image
                    gallery_image = ProductImage.objects.create(
                        product=product,
                        image=image_file
                    )
                    
                    uploaded_images.append({
                        'id': gallery_image.id,
                        'url': gallery_image.image.url,
                        'filename': image_file.name
                    })
                    
                except Exception as e:
                    errors.append(f'{image_file.name}: {str(e)}')
            
            return JsonResponse({
                'success': True,
                'uploaded': uploaded_images,
                'errors': errors,
                'message': f'Successfully uploaded {len(uploaded_images)} images'
            })
            
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


class ReorderGalleryImagesView(LoginRequiredMixin, View):
    """
    AJAX view for reordering gallery images
    """
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body)
            image_order = data.get('image_order', [])
            product_id = data.get('product_id')
            
            if not image_order or not product_id:
                return JsonResponse({'success': False, 'error': 'Invalid data'})
            
            # Get product with vendor isolation
            product_qs = Product.objects.all()
            if not request.user.is_superuser and hasattr(request.user, 'vendor'):
                product_qs = product_qs.filter(vendor=request.user.vendor)
            
            product = get_object_or_404(product_qs, id=product_id)
            
            # Update order (you'll need to add an 'order' field to ProductImage model)
            for index, image_id in enumerate(image_order):
                ProductImage.objects.filter(
                    id=image_id, 
                    product=product
                ).update(order=index)
            
            return JsonResponse({
                'success': True,
                'message': 'Images reordered successfully'
            })
            
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})


# --- DISCOUNT VIEWS ---
class DiscountListView(LoginRequiredMixin, ListView):
    model = Discount
    template_name = 'master/discount_list.html'

class DiscountCreateView(LoginRequiredMixin, CreateView):
    model = Discount
    form_class = DiscountForm
    template_name = 'master/discount_form.html'
    success_url = reverse_lazy('master:discount_list')

# --- DELIVERY ZONE VIEWS ---
class DeliveryZoneListView(LoginRequiredMixin, ListView):
    model = DeliveryZone
    template_name = 'master/delivery_zone_list.html'

class DeliveryZoneUpdateView(LoginRequiredMixin, UpdateView):
    model = DeliveryZone
    form_class = DeliveryZoneForm
    template_name = 'master/delivery_zone_form.html'
    success_url = reverse_lazy('master:delivery_zone_list')
