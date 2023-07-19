from django.shortcuts import render, redirect, get_object_or_404
import json
from django.http import JsonResponse


from .forms import ProductForm, SaleForm, SaleItemFormSet, AddToCartForm

from .models import Product, Sale, Invoice, SaleItem, ShoppingCartItem

def inventory(request):
    products = Product.objects.all()
    return render(request, 'product/inventory.html', {'products': products})

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ProductForm()

    return render(request, 'product/create_product.html', {'form': form})

def update_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('inventory')
    else:
        form = ProductForm(instance=product)

    return render(request, 'product/update_product.html', {'form': form, 'product': product})

def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect('inventory')

    return render(request, 'product/delete_product.html', {'product': product})



def sales_list(request):
    sales = Sale.objects.all()
    return render(request, 'sales/sales_list.html', {'sales': sales})

def create_sale(request):
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        saleitem_formset = SaleItemFormSet(request.POST)

        if sale_form.is_valid() and saleitem_formset.is_valid():
            sale = sale_form.save()
            sale_items = saleitem_formset.save(commit=False)

            for sale_item in sale_items:
                sale_item.sale = sale
                sale_item.save()

            # Generate invoice
            total_amount = sum(sale_item.quantity_sold * sale_item.product.price for sale_item in sale_items)
            invoice = Invoice(sale=sale, total_amount=total_amount, invoice_number="INV001")
            invoice.save()

            return redirect('invoice_details', invoice_id=invoice.id)
    else:
        sale_form = SaleForm()
        saleitem_formset = SaleItemFormSet()

    return render(request, 'sales/create_sale.html', {'sale_form': sale_form, 'saleitem_formset': saleitem_formset})


def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = AddToCartForm(request.POST)
        if form.is_valid():
            cart_item = form.save(commit=False)
            cart_item.product = product
            cart_item.save()
            return redirect('cart')

    else:
        form = AddToCartForm()

    return render(request, 'sales/add_to_cart.html', {'form': form, 'product': product})


def cart(request):
    cart_items = ShoppingCartItem.objects.all()
    return render(request, 'sales/cart.html', {'cart_items': cart_items})


def remove_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(ShoppingCartItem, id=cart_item_id)

    if request.method == 'POST':
        cart_item.delete()
        return redirect('cart')

    return render(request, 'sales/remove_cart_item.html', {'cart_item': cart_item})


def generate_invoice(request):
    cart_items = ShoppingCartItem.objects.all()
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == 'POST':
        sale = Sale.objects.create(customer_name=request.POST.get('customer_name'))
        for cart_item in cart_items:
            SaleItem.objects.create(sale=sale, product=cart_item.product, quantity_sold=cart_item.quantity)
            cart_item.delete()

        invoice = Invoice.objects.create(sale=sale, total_amount=total_amount, invoice_number="INV001")

        return redirect('invoice_details', invoice_id=invoice.id)

    return render(request, 'sales/generate_invoice.html', {'cart_items': cart_items, 'total_amount': total_amount})




def invoice_details(request, invoice_id):
    invoice = Invoice.objects.get(id=invoice_id)
    sale_items = SaleItem.objects.filter(sale=invoice.sale)

    return render(request, 'invoices/invoice_details.html', {'invoice': invoice, 'sale_items': sale_items})


def confirm_sale(request, sale_id):
    sale = Sale.objects.get(id=sale_id)
    invoice = Invoice.objects.get(sale=sale)

    return render(request, 'sales/confirm_sale.html', {'sale': sale, 'invoice': invoice})


def invoice_list(request):
    invoices = Invoice.objects.all()
    return render(request, 'invoices/invoice_list.html', {'invoices': invoices})