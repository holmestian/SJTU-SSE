SJTU-SSE
=====================
### *Dynamic Searchable Symmetric Encryption*

This project is an implementation of Dynamic SSE. We use keyword balanced binary tree to keep efficency in keyword searching. There are **several verions** for our project. We firstly finish a simple memory version then we transplant the algorthims to graph database(neo4j). You can check our competition report [here](https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/%E5%9F%BA%E4%BA%8E%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84%E5%8F%AF%E6%90%9C%E7%B4%A2%E5%8A%A0%E5%AF%86%E7%B3%BB%E7%BB%9F.pdf) where we give **detailed algorthims**, **implementations** and **tests**.

### SSE: Memory Version
Memory Version doesn't mean loss of infomation when power is off. We use sqlite3 and tmp file to keep information (both tree and ciphers) persistent. The scapegoat tree was implemented in c++, which is covered with c and called by python. (using ctypes module)

### Environment ###

* Python 2.7 
* Django 1.10 
* Django rest-framework 3
###

    cd unauth_server/
    g++ -o treeLib.so -shared -fPIC ciphertext/tree.cpp
    python manage.py runserver [0.0.0.0:8000]

Go to *http://localhost:8000/* to check the API.

### SSE: Neo4j with Django Demo (modified this [repo](https://github.com/johanlundberg/neo4j-django-tutorial/))
#### How to start
Clone this repository:

```
git clone https://github.com/wangjksjtu/SJTU-SSE.git
cd python/neo4j_v1
```

Create virtualenv inside the repository and activate it:

```
mkvirtualenv django_neo4j
```

Install the packages that you need.

```
pip install -r requirements.txt
```

Start neo4j server.

```
cd ~/neo4j-3.2.0/bin
./neo4j start
```
#### After Neo4j is started
Go to *http://localhost:7474* in your favorite browser and update the default password. 

Copy the Cypher statements below and paste it in the query window at the top:
```
CREATE (c0:Ciphertext {name:'C0', content:'Welcome to Cyberspace Security College'})
CREATE (c1:Ciphertext {name:'C1', content:'We should apply CNN in Password Cracking'})
CREATE (c2:Ciphertext {name:'C2', content:'Cyberspace Security may be soloved by Deep learning methods'})
CREATE (c3:Ciphertext {name:'C3', content:'Password Guessing is a hot problem in Information Security'})
CREATE (c4:Ciphertext {name:'C4', content:'We should combine CNN, Password, Security, Cyberspace and Deep learning together'})
CREATE (c5:Ciphertext {name:'C5', content:'This is a sentence without keywords'})

CREATE (k1:Key {name:'K1', key:'Cyberspace'})
CREATE (k2:Key {name:'K2', key:'Password'})
CREATE (k3:Key {name:'K3', key:'Security'})
CREATE (k4:Key {name:'K4', key:'Deep learning'})
CREATE (k5:Key {name:'K5', key:'CNN'})

CREATE
   (k1)-[:is_key]->(c0),
   (k1)-[:is_key]->(c2),
   (k1)-[:is_key]->(c4),
   (k2)-[:is_key]->(c1),
   (k2)-[:is_key]->(c3),
   (k2)-[:is_key]->(c4),
   (k3)-[:is_key]->(c0),
   (k3)-[:is_key]->(c2),
   (k3)-[:is_key]->(c3),
   (k3)-[:is_key]->(c4),
   (k4)-[:is_key]->(c2),
   (k4)-[:is_key]->(c3),
   (k5)-[:is_key]->(c1),
   (k5)-[:is_key]->(c4)
```
Edit the settings.py file and change NEO4J_PASSWORD to the one you previously set in the neo4j web frontend.
```
vim SJTU_SSE_v2/settings.py
```

After editing settings.py, issue the following commands:

```
python manage.py migrate
python manage.py bootstrap
python manage.py runserver
```
You can visit this [repo](https://github.com/johanlundberg/neo4j-django-tutorial/) for more infomation.
Go to *http://localhost:8000/* to check the demo.

### Screenshots for Demo
<p align="center">
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v1_home.png" />
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v1_keys.png", width=700, height=430 />
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v1_admin.png", width=600, height=430/>
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v1_graph.png", width=600, height=430/>
</p>
