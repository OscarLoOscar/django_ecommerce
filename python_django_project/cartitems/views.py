from django.shortcuts import render

# Create your views here.
def get_subtotal(self):
  return self.product.price * self.product.quantity