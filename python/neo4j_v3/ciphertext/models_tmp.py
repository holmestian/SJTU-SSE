# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
#from django_neomodel import DjangoNode
from neomodel import StructuredNode, StructuredRel
from neomodel import StringProperty, BooleanProperty, IntegerProperty
from neomodel import RelationshipTo

#alpha = 0.7

class Ciphertext(models.Model):
    content = models.TextField(blank=True, default='')
    keys = models.TextField(blank=False, default='non_sense')

class ROOT_HEAD(StructuredNode):
    root = RelationshipTo('Node', 'root')
    content_size = IntegerProperty(default=100)
    need_rebuild = RelationshipTo('Node', 'need_build')

#class IsFatherRel(StructuredRel):
#    depth = IntegerProperty(blank=False)
#    max_id = IntegerProperty(blank=False)

class Node(StructuredNode):
    handle_id = IntegerProperty(blank=False)
    is_real = BooleanProperty(default = False)
    tree_size = IntegerProperty(default = 1)
    content = StringProperty(default='')
    content_size = IntegerProperty()
    max_id = IntegerProperty(default=0)
    min_id = IntegerProperty(default=0)
    left = RelationshipTo('Node', 'left')
    right = RelationshipTo('Node', 'right')
    father = RelationshipTo('Node', 'father')
    #depth = IntegerProperty(blank=False, default=1)
    def update(self):
        lsize = 0 if len(self.left.all()) == 0 else self.left.all()[0].tree_size
        rsize = 0 if len(self.right.all()) == 0 else self.right.all()[0].tree_size
        self.tree_size = lsize + rsize + 1
        nc = ""
        for i in range(0, self.content_size):
            lc = 0 if len(self.left.all()) == 0 else int(self.left.all()[0].content[i])
            rc = 0 if len(self.right.all()) == 0 else int(self.right.all()[0].content[i])
            nc += str(lc | rc)
        if self.tree_size > 1:
            self.min_id = self.left.all()[0].min_id if not len(self.left.all()) == 0 else self.right.all()[0].min_id
            self.max_id = self.right.all()[0].max_id if not len(self.right.all()) == 0 else self.left.all()[0].max_id
            self.id = self.right.all()[0].min_id if not len(self.right.all()) == 0 else self.left.all()[0].max_id + 1

