# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from ciphertext.models import Ciphertext

# Register your models here.

class CiphertextAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'keys')

admin.site.register(Ciphertext, CiphertextAdmin)
