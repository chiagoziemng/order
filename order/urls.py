from django.urls import path
from . import views

urlpatterns = [
    path('', views.inventory, name='inventory'),
    path('create-product/', views.create_product, name='create_product'),
    path('update-product/<int:product_id>/', views.update_product, name='update_product'),
    path('delete-product/<int:product_id>/', views.delete_product, name='delete_product'),

    path('sales/', views.sales_list, name='sales_list'),
    #path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/confirm/<int:sale_id>/', views.confirm_sale, name='confirm_sale'),

    path('invoices/', views.invoice_list, name='invoice_list'),
    path('invoices/<int:invoice_id>/', views.invoice_details, name='invoice_details'),



      path('sales/create/', views.create_sale, name='create_sale'),
    path('sales/add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('sales/cart/', views.cart, name='cart'),
    path('sales/remove_cart_item/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('sales/generate_invoice/', views.generate_invoice, name='generate_invoice'),
    path('sales/invoice_details/<int:invoice_id>/', views.invoice_details, name='invoice_details'),


    
]
