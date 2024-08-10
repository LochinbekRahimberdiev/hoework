from django.urls import path
from shop.bd import auth
from shop import views
from shop.views import add_comment, order_product, add_product, delete_product, update_product

urlpatterns = [
    path('', views.home, name='home'),
    path('detail/<int:pk>', views.detail, name='detail'),
    path('detail/<int:product_id>/comment', add_comment, name='add_comment'),
    path('detail/<int:product_id>/order_product', order_product, name='order_product'),
    path('category/<int:cat_id>', views.home, name='category_by_id'),
    path('add-product/', add_product, name='add_product'),
    path('delete-product/<int:pk>', delete_product, name='delete_product'),
    path('update-product/<int:pk>', update_product, name='update_product'),
    path('login/', auth.login, name='login'),
    path('register/', auth.register, name='register'),
    path('logout/', auth.logout_page, name='logout'),
]