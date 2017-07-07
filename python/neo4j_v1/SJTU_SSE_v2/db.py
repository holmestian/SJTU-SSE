from re import escape
from django.conf import settings
from SJTU_SSE_v2.contextmanager import Neo4jDBSessionManager

__author__ = 'wangjk'

manager = Neo4jDBSessionManager(settings.NEO4J_RESOURCE_URI, settings.NEO4J_USERNAME, settings.NEO4J_PASSWORD)


def get_node(handle_id, label):
    q = 'MATCH (n:%s { handle_id: {handle_id} }) RETURN n' % label  # Ugly hack
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            return record['n']


def delete_node(handle_id, label):
    q = '''
        MATCH (n:%s { handle_id: {handle_id} })
        OPTIONAL MATCH (n)-[r]-()
        DELETE n, r
        ''' % label
    with manager.session as s:
        s.run(q, {'handle_id': handle_id})

def get_keys(handle_id):
    q = """
        MATCH (c:Ciphertext {handle_id: {handle_id}})<-[r:is_key]-(key)
        RETURN key.handle_id, key.key
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['key.handle_id'], 'keystring': record['key.key']}

def get_ciphers(handle_id):
    q = """
        MATCH (k:Key {handle_id: {handle_id}})-[r]->(ciphertext)
        RETURN ciphertext.handle_id, COLLECT(r) as relationships
        """
    with manager.session as s:
        result = s.run(q, {'handle_id': handle_id})
        for record in result:
            yield {'handle_id': record['ciphertext.handle_id'], 'relationships': record['relationships']}

#def create_key(_key, _name):
#    MERGE (n:Key {name: _name, key:_key})

#def create_cipher(_content, _name):

