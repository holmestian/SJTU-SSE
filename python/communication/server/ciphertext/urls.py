from django.conf.urls import url, include
from ciphertext import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = format_suffix_patterns([
    url(r'^$', views.api_root),
    url(r'^ciphertexts/$', views.CiphertextList.as_view(), name='ciphertext-list'),
    url(r'^ciphertexts/(?P<pk>[0-9]+)/$', views.CiphertextDetail.as_view(), name='ciphertext-detail'),
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),
])

# Login and logout views for the browsable API
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]
