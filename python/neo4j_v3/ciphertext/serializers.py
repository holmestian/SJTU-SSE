from rest_framework import serializers
from ciphertext.models import Ciphertext
from rest_framework.reverse import reverse
from rest_framework.utils import model_meta
from ciphertext.models import ROOT_HEAD, Node

from neomodel import db
db.set_connection('bolt://neo4j:wjkjk01@localhost:7687')

content_size = 100

q = "MATCH (n:ROOT_HEAD) RETURN n"
results, meta = db.cypher_query(q)
if (len(results) == 0):
    Tree = ROOT_HEAD(content_size=content_size).save()
#    print Tree.root
else:
    tree = results[0][0]
    Tree = ROOT_HEAD.inflate(tree)
#print type(Tree)
#print Tree.root.all()

class CipherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ciphertext
        fields = ('id', 'content', 'keys')

class CiphertextSerializer(serializers.HyperlinkedModelSerializer):

    def create(self, validated_data):
        #print validated_data
        try:
            keys = validated_data['keys']
            obj = Ciphertext.objects.create(**validated_data) 
            Tree.insert(obj.id, keys)
            obj.save()
            return obj
            #print "I am here: create"
        except:
            print "error"
            return Ciphertext.objects.all()[0]
            
    def update(self, instance, validated_data):
        #print validated_data
 #       raise_errors_on_nested_writes('update', self, validated_data)
        info = model_meta.get_field_info(instance)

        for attr, value in validated_data.items():
            if attr in info.relations and info.relations[attr].to_many:
                set_many(instance, attr, value)
            else:
                setattr(instance, attr, value)
        instance.save()
        #print "I am here: update"
        Tree.remove(instance.id)
        Tree.insert(instance.id, instance.keys)
        return instance

    def delete(self, instance):
        instance.delete()
        Tree.remove(instance.id)
        #print "I am here: delete"
        #instance.delete()

    def search(self, key):
        idlist = Tree.query(key)
        return idlist

    class Meta:
        model = Ciphertext
        fields = ('url', 'id', 'content', 'keys')
