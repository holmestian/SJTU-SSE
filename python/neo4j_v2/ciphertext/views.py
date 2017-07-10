# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from ciphertext.serializers import CipherSerializer
from ciphertext.models import Cipher, Key
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.decorators import api_view

from rest_framework import viewsets
from rest_framework.decorators import detail_route, list_route

from django.shortcuts import render
#from django.http import HttpResponseRedirect

from neomodel import db

db.set_connection('bolt://neo4j:wjkjk01@localhost:7687')

def get_by_id(pk):
    query = "MATCH (n) WHERE ID(n) = {id} RETURN n"
    results, meta = db.cypher_query(query, dict(id = pk))
    if len(results) == 0:
        return None
    else:
        return Cipher.inflate(results[0][0])

def search_by_key(key):
    query = '''
            MATCH (k:Key {keystr: {keystr}})-[r]->(cipher)
            RETURN cipher
            '''
    results, meta = db.cypher_query(query, dict(keystr = key))
    if len(results) == 0:
        return None
    else:
        return results

def delete_by_id(pk):
    query = '''
            MATCH (n:Cipher)
            WHERE ID(n) = {pk}
            DETACH DELETE n
            '''
    results = db.cypher_query(query, dict(pk=pk))

def update_cipher(cipher, pk, content, keys):
    query = '''
            MATCH (n:Cipher)<-[r:is_key]-(:Key)
            WHERE ID(n) = {pk}
            DELETE r
            '''
    print "hello3"
    cipher.content = content
    results = db.cypher_query(query, dict(pk=pk))
    for key in keys.split(" "):
        oldKey = Key.nodes.get_or_none(keystr=key)
        print "hello4"
        if not oldKey == None:
            print "hello6"
            oldKey.is_key.connect(cipher)
            print "hello5"
        else:
            print "hello7"
            newKey = Key(keystr=key).save()
            print "hello8"
            newKey.is_key.connect(cipher)
    return cipher

class CipherViewSet(viewsets.ModelViewSet):
    #queryset = Cipher.nodes.all()
    serializer_class = CipherSerializer
    #print queryset

    def get_queryset(self):
        return Cipher.nodes.all()

    def list(self, request):
        key = request.GET.get('key', '')
        slist = []
        if key:
            #key = key.lower().capitalize()
            ciphers = search_by_key(key)

            if ciphers == None:
                return Response(None)
            else:
                for c in ciphers:
                    dic = Cipher.inflate(c[0])
                    serializer = CipherSerializer(dic)
                    slist.append(serializer.data)
                return Response(slist)
        else:
            l = len(Cipher.nodes.all())
            for i in range(0, l):
                serializer = CipherSerializer(Cipher.nodes.all()[i])
                slist.append(serializer.data)
            return Response(slist)

    def perform_create(self, serializer):
        serializer.save()

    def retrieve(self, request, pk):
        cipher = get_by_id(int(pk))
        if cipher == None:
            return Response(None)
        serializer = CipherSerializer(cipher)
        return Response(serializer.data)

    def destroy(self, request, pk):
        print int(pk)
        result = delete_by_id(int(pk))
        return Response(None)

    def update(self, request, pk):
        content = request.POST['content']
        keys = request.POST['keys']
        cipher = get_by_id(int(pk))
        if cipher == None:
            return Response(None)
        cipher = update_cipher(cipher, int(pk), content, keys)
        serializer = CipherSerializer(cipher)
        return Response(serializer.data)
        #self.destroy(request, pk)
        #dic = dict()
        #c = Cipher(content=content)
        #print c
        #print type(c)
        #serializer = CipherSerializer(c)
        #print serializer.data
        #serializer.save()
        #return Response(None)

#    @detail_route(methods=['post'])
#    def create_cipher(self, request):
#        serializer = CipherSerializer(data=request.data)
#        if serializer.is_valid():
#            serializer.save()
#        else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

'''
class CipherList(generics.ListCreateAPIView):
    serializer_class = CipherSerializer
    q = Cipher.nodes.all()
    print q

    def get_queryset(self):
        #key = self.request.GET.get('key', 'non_sense')
        return Cipher.nodes.all()

    def perform_create(self, serializer):
        instance = serializer.save()
        #content = serializer.validated_data['content']
        #print content
        #keys = serializer.validated_data['keys'].rstrip()
        #for key in keys.split(" "):
            #print key
'''
'''
class CipherDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CipherSerializer

    def get_queryset(self):
        id = self.request.build_absolute_uri().split('/')[-2]
        print Cipher.nodes.all()
'''
'''
class CiphertextList(generics.ListCreateAPIView):
    serializer_class = CiphertextSerializer
    q = Ciphertext.objects.all()

    def get_queryset(self):
        keys = self.request.GET.get('keys', '')
        key = self.request.GET.get('key', '')
'''

class KeyList(generics.ListCreateAPIView):
    pass

class KeyDetail(generics.RetrieveUpdateDestroyAPIView):
    pass

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ciphers': reverse('cipher-list', request=request, format=format),
    })
