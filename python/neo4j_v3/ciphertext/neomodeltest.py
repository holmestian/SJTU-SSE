from neomodel import db
from neomodel import StructuredNode, StringProperty, IntegerProperty
from neomodel import RelationshipTo, RelationshipFrom, UniqueIdProperty

db.set_connection('bolt://neo4j:wjkjk01@localhost:7687')

class Country(StructuredNode):
    code = StringProperty(unique_index=True, required=True)
    non_sense = StringProperty(default = '123')
    # traverse incoming IS_FROM relation, inflate to Person objects
    inhabitant = RelationshipFrom('Person', 'IS_FROM')


class Person(StructuredNode):
    uid = UniqueIdProperty()
    name = StringProperty(unique_index=True)
    age = IntegerProperty(index=True, default=0)

    # traverse outgoing IS_FROM relations, inflate to Country objects
    country = RelationshipTo(Country, 'IS_FROM')

    def change_name(self, name):
        self.name = name
        self.save()
        #print self.name

if __name__ == "__main__":

    print "Hello"

    jim = Person(name='jim', age=3).save()
    #jim = Person.nodes.get(age=3)
    #print type(jim)
    jim.change_name("tom")

    #print jim.country
    #jim.age = 4
    #jim.save() # validation happens here
    #print jim
    #jim.delete()
    #jim.refresh() # reload properties from neo
    #print jim

    #germany = Country(code='DE').save()
    #america = Country(code='AC').save()
    #canada = Country(code='CA').save()

    #jim.country.connect(germany)
    #print jim.country
    #jim.country.connect(america)
    #print jim.country
    #print jim.country.all()
    #jim.delete()
    #country = jim.country.all()[0]
    #print country
    #country.non_sense = "234"
    #country.save()
    #print country.non_sense



