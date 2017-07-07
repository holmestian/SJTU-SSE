# -*- coding: utf-8 -*-

from __future__ import absolute_import

from django.conf.urls import url
from .views import *

__author__ = 'wangjksjtu'

urlpatterns = [
    url(r'^$', index, name='home'),
    url(r'^ciphertext/$', CiphertextListView.as_view(), name='cipher_list'),
    url(r'^key/$', KeyListView.as_view(), name='key_list'),
    url(r'^ciphertext/(?P<pk>[\d]+)/$', CiphertextDetailView.as_view(), name='cipher_detail'),
    url(r'^key/(?P<pk>[\d]+)/$', KeyDetailView.as_view(), name='key_detail'),
]
