from django.contrib import admin
from django.urls import path
from translator import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path ('',views.translate_text,name='home'),
]
