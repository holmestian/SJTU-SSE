from neomodel import db
from models import Cipher

db.set_connection('bolt://neo4j:wjkjk01@localhost:7687')

def delete_by_id(pk):
    query = '''
            MATCH (n:Cipher)
            WHERE ID(n) = {id}
            DETACH DELETE n
            '''
    results, meta = db.cypher_query(query, dict(id=pk))
    print results
    print meta

def get_by_id(pk):
    query = "MATCH (n) WHERE ID(n) = {id} RETURN n"
    results, meta = db.cypher_query(query, dict(id = pk))
    if len(results) == 0:
        return None
    else:
        return Cipher.inflate(results[0][0])
    #print results[0]
    #print results[0][0]
    #test = Cipher.inflate(results[0][0])
    #print test
    #return Cipher.inflate(results[0]) if len(results) > 0 else None

if __name__ == "__main__":
    print get_by_id(15)
    print get_by_id(21)
    delete_by_id(21)
    print get_by_id(21)
