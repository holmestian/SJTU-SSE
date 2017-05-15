from rest_framework import generics
#from django.contrib.auth.models import User
from ciphertext.serializers import CiphertextSerializer
from ciphertext.models import Ciphertext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from ciphertext.tree import Tree

idlist = []

class CiphertextList(generics.ListCreateAPIView):
    #queryset = Ciphertext.objects.all()
    serializer_class = CiphertextSerializer
    q = Ciphertext.objects.all()
    try:
        for obj in q:
            tree = Tree()
            if obj.id not in idlist:
                idlist.append(obj.id)
                tree.insert(obj.id, obj.keystring)
    except:
        pass
    def get_queryset(self):
        keystring = self.request.GET.get('keystring','')
        key = self.request.GET.get('key','')
        if keystring:
            return Ciphertext.objects.filter(keystring=keystring)
        elif key:
            try:
                if len(idlist) == 0:
                    #return Ciphertext.objects.filter(id=None)
                    return {}
                keys= key.split("-")
                tree = Tree()
                aset = set()
                for key in keys[0].split("|"):
                    alist = tree.query(int(key))
                    if alist == ['']: continue
                    aset |= set(alist)
                if len(keys) == 2:
                    for key in keys[1].split("|"):
                        if not key: break
                        if int(key) >= 0 and int(key) < 100:
                            alist = tree.query(int(key))
                        else: continue
                        if alist == ['']: continue
                        aset -= set(alist)
                if not len(aset):
                    #return Ciphertext.objects.filter(id=None)
                    return {}
                alist = list(aset)
                return Ciphertext.objects.filter(id__in=alist)
            except: return {}
        else: return Ciphertext.objects.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        id = instance.id
        keystring = instance.keystring
        idlist.append(id)
        #outfile = open("data_out", "a")
        #outfile.write(str(id) + " ")
        #outfile.close()
        tree = Tree()
        tree.insert(id, keystring)

class CiphertextDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ciphertext.objects.all()
    serializer_class = CiphertextSerializer
    try:
    	obj = queryset[0]
    	if obj.id not in idlist:
        	tree = Tree()
        	tree.insert(obj.id, obj.keystring)
    except:
        pass

    def perform_update(self, serializer):
        instance = serializer.save()
        id = instance.id
        keystring = instance.keystring
        #outfile = open("tmp2", "w")
        #outfile.write(str(id) + " " + keystring)
        tree = Tree()
        if id in idlist:
            tree.remove(id)
            tree.insert(id, keystring)
        else:
            idlist.append(id)
            tree.insert(id, keystring)
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

