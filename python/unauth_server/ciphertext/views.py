from rest_framework import generics
#from django.contrib.auth.models import User
from ciphertext.serializers import CiphertextSerializer
from ciphertext.models import Ciphertext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ciphertext.tree import Tree

class CiphertextList(generics.ListCreateAPIView):
    #queryset = Ciphertext.objects.all()
    serializer_class = CiphertextSerializer
    global idlist
    idlist = []

    def get_queryset(self):
        keystring = self.request.GET.get('keystring','')
        key = self.request.GET.get('key','')
        if keystring:
            return Ciphertext.objects.filter(keystring=keystring)
        elif key:
            if len(idlist) == 0:
                #return Ciphertext.objects.filter(id=None)
                return {}
            tree = Tree()
            alist = tree.query(int(key))
            if alist == ['']:
                #return Ciphertext.objects.filter(id=None)
                return {}
            return Ciphertext.objects.filter(id__in=alist)
        else: return Ciphertext.objects.all()

    def perform_create(self, serializer):
        serializer.save()
        id = serializer.data['id']
        keystring = self.request.POST.get('keystring','0000000000')
        idlist.append(id)
        #outfile = open("data_out", "a")
        #outfile.write(str(id) + " ")
        #outfile.close()
        tree = Tree()
        tree.insert(id, keystring)

class CiphertextDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ciphertext.objects.all()
    serializer_class = CiphertextSerializer
    
    def perform_destroy(self, instance):
        id = self.request.path.split('/')[-2]
        #infile = open("data_out", "r")
        #idlist = infile.readline.split(" ")
        #infile.close()
        if int(id) not in idlist:
            instance.delete()
        else:
            instance.delete()
            idlist.remove(int(id))
            tree = Tree()
            tree.remove(int(id))
'''
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
#    def get_queryset(self):
#        user = self.request.user
#        return User.objects.filter(username=user.username)

#    def perform_create(self, serializer):
#        serializer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
'''
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
		#'users': reverse('user-list', request=request, format=format),
		'ciphertexts': reverse('ciphertext-list', request=request, format=format),
    })

