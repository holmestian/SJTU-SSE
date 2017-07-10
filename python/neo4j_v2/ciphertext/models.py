# -*- coding: utf-8 -*-
from __future__ import unicode_literals
#from django.db import models
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StructuredRel
from neomodel import StringProperty, BooleanProperty, UniqueIdProperty
from neomodel import RelationshipTo

class Cipher(DjangoNode):
    #uid = UniqueIdProperty()
    content = StringProperty()

    def __str(self):
        return str(self.id)


class IsKeyRel(StructuredRel):
    real = BooleanProperty(default=True)

class Key(DjangoNode):
    #uid = UniqueIdProperty()
    keystr = StringProperty(unique_index=True)
    is_key = RelationshipTo('Cipher', 'is_key', model = IsKeyRel)

#class Ciphertext(models.Model)
#    keys = models.CharField(blank=False, default='nonsense')
#    content = models.TextField(blank=True, default='')
#
#    def __str(self):
#        return self(self.id) + ": " + "keySet[" + self.keys + "]"
