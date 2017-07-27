from neomodel import (StructuredNode, StringProperty, IntegerProperty, RelationshipTo, RelationshipFrom)
from neomodel import config
from neomodel import UniqueIdProperty

config.DATABASE_URL = 'bolt://neo4j:wjkjk01@localhost:7687'


class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)

    inhabitant = RelationshipFrom('Person', 'IS_FROM')

class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    country = RelationshipTo(Country, 'IS_FROM')
