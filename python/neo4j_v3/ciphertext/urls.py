from django.conf.urls import url
from ciphertext import views
from rest_framework.urlpatterns import format_suffix_patterns

cipher_list = views.CiphertextViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

cipher_detail = views.CiphertextViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^graph/$', views.api_graph),
    url(r'^ciphertext/$', cipher_list, name='ciphertext-list'),
    url(r'^ciphertext/(?P<pk>[0-9]+)/$', cipher_detail, name='ciphertext-detail'),
])
