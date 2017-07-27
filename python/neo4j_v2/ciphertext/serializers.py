from rest_framework import serializers
from ciphertext.models import Key, Cipher
from rest_framework.reverse import reverse

#class CipherSerializer(serializers.HyperlinkedModelSerializer):
class CipherSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField(allow_blank=True)
    keys = serializers.CharField(write_only=True,
            allow_blank=False, default='non_sense')

    def create(self, validated_data):
        print type(validated_data)
        print validated_data
        content = validated_data['content']
        c = Cipher(content=content).save()
        print c.id

        keys = validated_data['keys']
        for key in keys.split(" "):
            print key
            #key = key.lower().capitalize()
            oldKey = Key.nodes.get_or_none(keystr=key)
            if oldKey:
                oldKey.is_key.connect(c)
            else:
                newKey = Key(keystr=key).save()
                newKey.is_key.connect(c)
        return c

#    def update(self, instance, validated_data):
#        instance.content = validated_data.get('content',instance.content)
#        instance.keys = validated_data.get('keys', instance.keys)
#        instance.save()
#        return instance

#class KeySerializer(serializers.HyperlinkedModelSerializer):
#    key = serializers.CharField(blank=False)
#
#    class Meta:
#        model = Key
#        fields = ('url', 'id')
