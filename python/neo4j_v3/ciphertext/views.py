# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ciphertext.serializers import CiphertextSerializer, CipherSerializer
from ciphertext.models import Ciphertext

from django.http import Http404

content_size = 100

class CiphertextViewSet(viewsets.ModelViewSet):
    serializer_class = CiphertextSerializer
    #queryset = Ciphertext.objects.all()

    def get_queryset(self):
        return Ciphertext.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        serializer = CiphertextSerializer(instance)
        serializer.delete(instance)
        #print "I am here: delete"
        #instance.delete()
    '''
    def destroy(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            print instance.id
            print instance.content
            print instance
            self.perform_destroy(instance)
            print "I am here: destory"
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
    '''
    def list(self, request):
        print "search here"
        qset = set()
        key = request.GET.get('key', '')
        context = {
            'request':request,
        }
        serializer = CiphertextSerializer(self.get_queryset(),
                context=context, many=True)
        if key:
            keys = key.split("-")
            for key in keys[0].split("|"):
                if not key: break
                if not (int(key) >= 0 and int(key) < content_size):
                    continue
                s = CiphertextSerializer(self.get_queryset()[0],
                        context=context)
                alist = s.search(int(key))
                print alist
                qset |= set(alist)
            if len(keys) == 2:
                for key in keys[1].split("|"):
                    if not key: break
                    if int(key) >= 0 and int(key) < content_size:
                        alist = s.search(int(key))
                    else:
                        continue
                    qset -= set(alist)
                print qset
            objs = Ciphertext.objects.filter(id__in=list(qset))
            return Response(CiphertextSerializer(objs,
                context=context, many=True).data)
        else:
            return Response(serializer.data)


@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ciphers': reverse('ciphertext-list', request=request, format=format),
    })
