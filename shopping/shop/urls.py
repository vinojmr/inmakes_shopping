from django.urls import path
from . import views
app_name = 'shop'
urlpatterns = [
    # path('', views.home, name='home'),
    path('', views.allprod, name='allprod'),
    path('<slug:c_slug>/', views.allprod, name='prod_cat'),
    path('<slug:c_slug>/<slug:p_slug>/', views.prod_deets, name='products')
]
