from django.contrib import admin
from .models import Ciphertext

class CiphertextAdmin(admin.ModelAdmin):
	list_display = ('id', 'keystring', 'context')

admin.site.register(Ciphertext, CiphertextAdmin)
