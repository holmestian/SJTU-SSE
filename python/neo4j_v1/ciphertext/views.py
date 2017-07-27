# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from .models import *
from SJTU_SSE_v2 import db

class KeyListView(ListView):

    model = Key

class KeyDetailView(DetailView):

    model = Key

class CiphertextDetailView(DetailView):

    model = Ciphertext

class CiphertextListView(ListView):

    model = Ciphertext

def index(request):
    return render(request, 'ciphertext/index.html')
