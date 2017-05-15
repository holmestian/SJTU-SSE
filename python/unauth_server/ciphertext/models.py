from __future__ import unicode_literals
from django.db import models

class Ciphertext(models.Model):
	# keystring_len = 100
	keystring = models.CharField(blank=False, default='0'*100, max_length=100)
	# Maybe FileField is better
	context = models.TextField(blank=True, default='')
	created = models.DateTimeField(auto_now_add=True)
	#owner = models.ForeignKey('auth.User', related_name='items', on_delete=models.CASCADE)

	def __str(self):
		return str(self.id) + ": " + self.keystring
