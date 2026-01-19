from django.urls import path
from  . import views

app_name = 'pages'

urlpatterns = [
  path('',views.index,name = 'index'),
  path('about/',views.about,name='about'),
  path('contact/',views.contact_view,name="contact"),
  path('contact/success/',views.contact_success,name="contact_success"),
  path('privacy-policy/',views.privacypolicy,name="privacy_policy"),
  path('terms-and-conditions/',views.tandc,name="tandc"),
]