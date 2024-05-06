from django.contrib import admin
from application.models import Product, Category, Vendor, CartOrderItems, CartOrder, ProductImages, ProductReview, WishList, Address
from import_export.admin import ImportExportModelAdmin


class ProductImagesAdmin(admin.TabularInline):
    model = ProductImages

class ProductAdmin(ImportExportModelAdmin):
    inlines = [ProductImagesAdmin]
    list_display = ['title', 'price', 'category']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'category_image']
    

class VendorAdmin(admin.ModelAdmin):
    list_display = ['title', 'vendor_image']


class CartOrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'price', 'paid_status', 'order_date']

class CartOrderItemsAdmin(admin.ModelAdmin):
    list_display = ['order', 'invoice_no', 'item', 'image', 'qty', 'price', 'total']

class ProductReviewAdmin(ImportExportModelAdmin):
    list_display = ['user', 'product', 'review', 'rating']


class WishListAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'date']

class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'status']



admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Vendor, VendorAdmin)
admin.site.register(CartOrder, CartOrderAdmin)
admin.site.register(CartOrderItems, CartOrderItemsAdmin)
admin.site.register(ProductReview, ProductReviewAdmin)
admin.site.register(WishList, WishListAdmin)
admin.site.register(Address, AddressAdmin)
