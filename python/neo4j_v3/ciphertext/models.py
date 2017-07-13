# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django_neomodel import DjangoNode
from neomodel import StructuredNode, StructuredRel
from neomodel import StringProperty, BooleanProperty, IntegerProperty
from neomodel import RelationshipTo

from time import sleep


alpha = 0.7

class Ciphertext(models.Model):
    content = models.TextField(blank=True, default='')
    keys = models.TextField(blank=False, default='non_sense')

class ROOT_HEAD(StructuredNode):
    root = RelationshipTo('Node', 'root')
    content_size = IntegerProperty(default=100)
    need_rebuild = RelationshipTo('Node', 'need_build')

    def __root(self):
        #print "------root-------"
        return None if self.root.all() == [] else self.root.all()[0]
    def __need_rebuild(self):
        #print "----need_rebuild----"
        return None if self.need_rebuild.all() == [] else self.need_rebuild.all()[0]

    def __insert_inner(self, node, id, content):
        print "---------insert_inner------------"
        if type(node) != type(Node(handle_id=0, content_size=10)):
            if len(node.all()) == 0:
                newnode = Node(handle_id=id, is_real=True,
                        content=content, content_size=self.content_size,
                        max_id=id, min_id=id).save()
                node.connect(newnode)
                #newnode.father.connect(node)
                return

            print 'here inner insert'
            node = node.all()[0]
            print type(node)
        else:
            pass
        if node.is_real:
            if node.Left() != None or node.Right() != None:
                print "[Fatal Error]: Node %d had at least one son while inserting new node!" % node.handle_id
            p = Node(handle_id=node.handle_id, is_real=True,
                     content=node.content, content_size=self.content_size,
                     max_id=node.handle_id, min_id=node.handle_id).save()
            q = Node(handle_id=id, is_real=True,
                     content=content, content_size=self.content_size,
                     max_id=id, min_id=id).save()
            if id < node.handle_id:
                node.left.connect(q)
                node.right.connect(p)
                q.father.connect(node)
                p.father.connect(node)
            else:
                node.left.connect(p)
                node.right.connect(q)
                q.father.connect(node)
                p.father.connect(node)
            #print node.max_id, node.min_id
            node.update()
            #print node.max_id, node.min_id
            #print node.is_real
            #print node.handle_id
            node.is_real = False
            node.save()
            #node.refresh()
            #print node.is_real
            return

        if id < node.handle_id:
            if node.Left() == None:
                self.__insert_inner(node.left, id, content)
            else:
                self.__insert_inner(node.Left(), id, content)
        else:
            if node.Right()== None:
                self.__insert_inner(node.right, id, content)
            else:
                self.__insert_inner(node.Right(), id, content)
        node.update()

        ls = 0 if node.Left() == None else node.Left().tree_size
        rs = 0 if node.Right() == None else node.Right().tree_size
        if (max(ls, rs) > node.tree_size * alpha):
            print "------ bigger than alpha---------"
            print "__init__ need_rebuild" + str(self.__need_rebuild())
            self.need_rebuild.connect(node)

    def __getid(self, node, key):
        print "-----------getid---------------------"
        result = []
        if node.content[key] == '0': return result
        if node.is_real:
            if node.content[key] == '1':
                result.append(node.handle_id)
            return result

        if node.Left() != None:
            result += self.__getid(node.Left(), key)
        if node.Right() != None:
            result += self.__getid(node.Right(), key)

        return result

    def __dfs_getid(self, node):
        print "-----------dfs-getid----------------"
        result = []
        if node.is_real:
            if node.Left() != None or node.Right() != None:
                print "[Fatal Error]: Node %d has at least one son while accessing it!" % node.handle_id
            result.append(node)
            return result

        if node.Left() != None:
            result += self.__dfs_getid(node.Left())
        if node.Right() != None:
            result += self.__dfs_getid(node.Right())
        node.delete()
        return result

    def __remove_inner(self, node, id):
        print "-----------remove-inner--------------"
        if node.is_real and node.handle_id == id:
            if node.Left() != None or node.Right() != None:
                print "[Fatal Error]: Node %d had at least one son while removing it"
            node.delete()
            return

        if id < node.handle_id:
            self.__remove_inner(node.Left(), id)
        else:
            self.__remove_inner(node.Right(), id)
        node.update()

        if node.is_real == False and node.tree_size == 1:
            node.delete()
            return

        ls = 0 if node.Left() == None else node.Left().tree_size
        rs = 0 if node.Right() == None else node.Right().tree_size

        if max(ls, rs) > node.tree_size * alpha:
            self.need_rebuild.connect(node)
            print "self.need_rebuild" + str(self.__need_rebuild())

    def __build(self, l, r, idseq, father):
        print "-----------build-----------------"
        print "l: " + str(l)
        print "r: " + str(r)
        if l == r:
            print "l == r"
            if idseq[l].Father() != None :
                print "have old father"
                oldfather = idseq[l].Father()
                idseq[l].father.disconnect(oldfather)
            idseq[l].father.connect(father)
            return idseq[l]

        node = Node(handle_id=0, content_size=self.content_size,
                    is_real=False).save()
        mid = (l + r) / 2

        ls = self.__build(l, mid, idseq, node)
        rs = self.__build(mid+1, r, idseq, node)
        if node.Left() != None:
            node.left.disconnect(node.Left())
        node.left.connect(ls)
        if node.Right() != None:
            node.right.disconnect(node.Right())
        node.right.connect(rs)

        node.update()
        return node

    def __rebuild_subtree(self):
        print "------rebuild-subtree-------"
        need_rebuild = self.__need_rebuild()
        father = need_rebuild.Father()
        print "Father " + str(father)
        idseq = self.__dfs_getid(need_rebuild)
        print "Idseq" + str(len(idseq))
        newnode = self.__build(0, len(idseq)-1, idseq, father)
        print "------ build-finished-------"
        if father == None:
            print "self.__root() " + str(self.__root())
            if self.__root() != None:
                self.root.disconnect(self.__root())
            self.root.connect(newnode)
            return

        if father.Left() == need_rebuild:
            print "father.Left() == need_rebuild"
            father.left.disconnect(need_rebuild)
            father.left.connect(newnode)
        else:
            print "father.Right() == need_rebuild"
            if father.Right() != None:
                father.right.disconnect(father.Right())
            #father.right.disconnect(need_rebuild)
            father.right.connect(newnode)

        while father != None:
            print "Update father"
            father.update()
            father = father.Father()

    def insert(self, id, content):
        self.__insert_inner(self.root, id, content)
        print "inner insert finshed"
        if self.__need_rebuild() != None:
            print '------Need_rebuild--------'
            self.__rebuild_subtree()

    def remove(self, id):
        self.__remove_inner(self.__root(), id)
        if self.__need_rebuild() != None:
            self.__rebuild_subtree()

    def query(self, key):
        result = self.__getid(self.__root(), key)
        return result

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

    def Left(self):
        return None if self.left.all() == [] else self.left.all()[0]

    def Right(self):
        return None if self.right.all() == [] else self.right.all()[0]

    def Father(self):
        return None if self.father.all() == [] else self.father.all()[0]

    def update(self):
        lsize = 0 if self.Left() == None else self.Left().tree_size
        rsize = 0 if self.Right() == None else self.Right().tree_size

        if self.Left() != None and self.Left().Father() == None:
            self.Left().father.connect(self)
        if self.Right() != None and self.Right().Father() == None:
            self.Right().father.connect(self)

        self.tree_size = lsize + rsize + 1
        nc = ""
        for i in range(0, self.content_size):
            lc = 0 if self.Left() == None else int(self.Left().content[i])
            rc = 0 if self.Right() == None else int(self.Right().content[i])
            nc += str(lc | rc)
        self.content = nc
        if self.tree_size > 1:
            self.min_id = self.Left().min_id if not self.Left() == None else self.Right().min_id
            self.max_id = self.Right().max_id if not self.Right() == None else self.Left().max_id
            self.handle_id = self.Right().min_id if not self.Right() == None else self.Left().max_id + 1
        #print self.handle_id
        #print self.tree_size
        self.save()
