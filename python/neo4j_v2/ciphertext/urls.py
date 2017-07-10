from django.conf.urls import url, include
from ciphertext import views
from rest_framework.urlpatterns import format_suffix_patterns

cipher_list = views.CipherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

cipher_detail = views.CipherViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    #url(r'^ciphers/$', views.CipherList.as_view(), name='cipher-list'),
    url(r'^ciphers/$', cipher_list, name='cipher-list'),
    url(r'^keys/$', views.KeyList.as_view(), name='key-list'),
    url(r'^ciphers/(?P<pk>[0-9]+)/$', cipher_detail, name='cipher-detail'),
    url(r'^keys/(?P<pk>[0-9]+)/$', views.KeyDetail.as_view(), name='key-detail'),
])
