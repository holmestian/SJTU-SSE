from rest_framework import serializers
from ciphertext.models import Ciphertext
from django.contrib.auth.models import User

class CiphertextSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')

	class Meta:
		model = Ciphertext
		fields = ('url', 'id', 'owner', 'keystring', 'context', 'created')

class UserSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'password', 'email')
