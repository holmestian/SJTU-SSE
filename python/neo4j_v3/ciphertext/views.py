# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.reverse import reverse
from rest_framework.response import Response
from ciphertext.serializers import CiphertextSerializer, CipherSerializer
from ciphertext.models import Ciphertext

from ciphertext.models import ROOT_HEAD, Node

from django.http import Http404

content_size = 100

class CiphertextViewSet(viewsets.ModelViewSet):
    serializer_class = CiphertextSerializer
    #queryset = Ciphertext.objects.all()

    def get_queryset(self):
        qset = set()
        key = self.request.GET.get('key', '')
        context = {
            'request':self.request,
        }
        #serializer = CiphertextSerializer(self.get_queryset(),
        #        context=context, many=True)
        if key:
            keys = key.split("-")
            for key in keys[0].split("|"):
                if not key: break
                if not (int(key) >= 0 and int(key) < content_size):
                    continue
                s = CiphertextSerializer(Ciphertext.objects.first(),
                        context=context)
                alist = s.search(int(key))
#                print alist
                qset |= set(alist)
            if len(keys) == 2:
                for key in keys[1].split("|"):
                    if not key: break
                    if int(key) >= 0 and int(key) < content_size:
                        alist = s.search(int(key))
                    else:
                        continue
                    qset -= set(alist)
#                print qset
            objs = Ciphertext.objects.filter(id__in=list(qset))
            return objs
        else:
            #return Response(serializer.data)
            return Ciphertext.objects.all()

    def perform_create(self, serializer):
        serializer.save()

    def perform_destroy(self, instance):
        serializer = CiphertextSerializer(instance)
        serializer.delete(instance)
        #print "I am here: delete"
        #instance.delete()

@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'ciphers': reverse('ciphertext-list', request=request, format=format),
    })

@api_view(['GET'])
def api_graph(request, format=None):
    root_head = ROOT_HEAD.nodes.all()[0]
    root_id = root_head.root.all()[0].id
    #print root_id
    nodes = Node.nodes.all()
    #js1 = {'nodes':[{'id':root_id, 'label':'ROOT_HEAD', 'color':'#e04141'}]}
    #js2 = js1
    #js1['nodes'] += js2['nodes']
    js_w = {'nodes':[], 'edges':[]}
    #print type(root_head)
    #print len(nodes)
    for node in nodes:
        handle_id = node.id
        js = None
        if handle_id == root_id:
            js = {'id':root_id, 'label':'ROOT', 'color':'#e04141'}
        else:
            js = {'id':handle_id, 'label':str(node.tree_size), 'color':'#e09c41'}
        if node.is_real:
            js['color'] = '#41e0c9'
            js['label'] = 'FILE'
            js['handle_id'] = node.handle_id
        js_w['nodes'] += [js]
        if node.left.all() != []:
            left_id = node.left.all()[0].id
            js = {'from':handle_id, 'to':left_id}
            js_w['edges'] += [js]
        if node.right.all() != []:
            right_id = node.right.all()[0].id
            js = {'from':handle_id, 'to':right_id}
            js_w['edges'] += [js]
    #print type(nodes)
    return Response(js_w)
