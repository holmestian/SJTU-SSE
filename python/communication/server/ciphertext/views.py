from rest_framework import generics
from rest_framework import permissions
from django.contrib.auth.models import User
from ciphertext.serializers import CiphertextSerializer, UserSerializer
from ciphertext.models import Ciphertext
from ciphertext.permissions import IsOwner, IsUser
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

class CiphertextList(generics.ListCreateAPIView):
    serializer_class = CiphertextSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    def get_queryset(self):
        """
        This view should return a list of all the ciphertexts
        for the currently authenticated user.
        """
        owner = self.request.user
        keystring = self.request.GET.get('keystring', '')
        if keystring: 
            return Ciphertext.objects.filter(owner=owner).filter(keystring=keystring)
        else: return Ciphertext.objects.filter(owner=owner)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class CiphertextDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwner)
    queryset = Ciphertext.objects.all()
    serializer_class = CiphertextSerializer

class UserList(generics.ListCreateAPIView):
    #permission_classes = (permissions.IsAuthenticated, IsUser)
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user
        return User.objects.filter(username=user.username)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAuthenticated, IsUser)
    serializer_class = UserSerializer
    queryset = User.objects.all()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
		'users': reverse('user-list', request=request, format=format),
		'ciphertexts': reverse('ciphertext-list', request=request, format=format),
    })

