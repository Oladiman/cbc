"""CBC URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from main import views
from accounts.views import(login_view, register_view, logout_view, edit_user)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index, name='index'),
    url(r'^login/', login_view, name='login'),
    url(r'^sell/$', views.sell_form, name='sell'),
    url(r'^my-products/$', views.my_products, name='my_products'),
    url(r'^delete-product/(?P<slug>[\w-]+)/$', views.delete_product, name='delete_products'),
    url(r'^add-product/(?P<slug>[\w-]+)/$', views.add_product, name='add_product'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^register/', register_view, name='register'),
    url(r'^categories/(?P<category>[\w-]+)/$', views.category, name='category'),
    url(r'^accounts/(?P<username>[\w-]+)/$', edit_user, name='account_update'),
    # url(r'^accounts/profile/$', profile_view, name='user_profile'),
    url(r'^cart/$', views.cart, name='cart'),
    url(r'^delete-cart/(?P<username>[\w-]+)/(?P<slug>[\w-]+)/$', views.delete_cart, name='delete_cart'),
    url(r'^product-details/(?P<slug>[\w-]+)/$', views.product_detail, name='product-detail'),
    url(r'^shop/$', views.shop, name='shop'),
    url(r'^contact-us/$', views.contact, name='contact'),
    url(r'^Terms-of-use/$',views.Terms_of_use,name='Terms-of-use'),
    url(r'^about-us/$', views.about_cbc, name='about-cbc'),
    url(r'^privacy-policy/$', views.privacy_policy, name='privacy_policy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
