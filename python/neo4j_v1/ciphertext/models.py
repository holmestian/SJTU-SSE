from django.db import models
from django.core.urlresolvers import reverse
from SJTU_SSE_v2 import db

class NodeHandle(models.Model):
    handle_id = models.CharField(max_length=64, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    def __str__(self):
        return 'NodeHandle for node %d' % self.node()['handle_id']

    def node(self):
        return db.get_node(self.handle_id, self.__class__.__name__)

    def delete(self, **kwargs):
        """
                Delete that node handle and the handles node.
                """
        db.delete_node(self.handle_id, self.__class__.__name__)
        super(NodeHandle, self).delete()
        return True

    delete.alters_data = True


class Ciphertext(NodeHandle):

    def __str__(self):
        return self.content

#    def _title(self):
#        try:
#            return self.node().properties.get('content', 'Missing title')
#        except AttributeError:
#            return 'Missing node?'
#    title = property(_title)

    def get_absolute_url(self):
        return reverse('cipher_detail', args=[str(self.id)])

    def _content(self):
        try:
            return self.node().properties.get('content', 'Missing content')
        except AttributeError:
            return 'Missing node???'
    content = property(_content)

    def _keys(self):
        keys = []
        for key in db.get_keys(self.handle_id):
            keys.append({'key': Key.objects.get(handle_id=key['handle_id'])})
        return keys
    keys = property(_keys)

class Key(NodeHandle):

    def __str__(self):
        return self.key

    def _key(self):
        try:
            return self.node().properties.get('key', 'Missing key')
        except AttributeError:
            return 'Miss node??'
    key = property(_key)

    def get_absolute_url(self):
        return reverse('key_detail', args=[str(self.id)])

    def _ciphers(self):
        ciphers = []
        for cipher in db.get_ciphers(self.handle_id):
            ciphers.append({'cipher': Ciphertext.objects.get(handle_id=cipher['handle_id'])})
        return ciphers
    ciphers = property(_ciphers)
