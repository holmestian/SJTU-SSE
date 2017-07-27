DSSE-GraphDB
=====================
### *Dynamic Searchable Symmetric Encryption Based on Graph Database*

This project is an implementation of Dynamic SSE. We use keyword balanced binary tree to keep efficency in keyword searching. There are **several verions** for our project. We firstly finish a simple memory version then we transplant the algorthims to graph database(neo4j). You can check our competition report [here](https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/%E5%9F%BA%E4%BA%8E%E5%9B%BE%E6%95%B0%E6%8D%AE%E5%BA%93%E7%9A%84%E5%8F%AF%E6%90%9C%E7%B4%A2%E5%8A%A0%E5%AF%86%E7%B3%BB%E7%BB%9F.pdf) where we give **detailed algorthims**, **implementations** and **tests**.

### SSE: Memory Version
Memory Version doesn't mean loss of infomation when power is off. We use sqlite3 and tmp file to keep information (both tree and ciphers) persistent. The scapegoat tree was implemented in c++, which is covered with c and called by python. (using ctypes module)

### Environment1: ###

* Python 2.7 
* Django 1.10 
* Django rest-framework 3
###

    cd unauth_server/
    g++ -o treeLib.so -shared -fPIC ciphertext/tree.cpp
    python manage.py runserver [0.0.0.0:8000]

Go to *http://localhost:8000/* to check the API.

### SSE: Neo4j Version
Compared with Memory Version, this version is implemented in neo4j database, which provides supports for parallel computing(query). The whole codes are in python/neo4j_v3 folders and tranplant scapegoat tree into graph database, which guarantees high stability, efficiency and scalability. You can deploy this API by following steps.
### Environment2: ###

* Python 2.7
* Neo4j 3.0+
* Django 1.10+
* Django rest-framework 3
* neomodel / django-neomodel
* corsheaders (support for JSONP)
* sslserver (support for https)

**Tips**: You can install these packages using pip. To prevent conflicts, you'd better use virtual environment by installing virtualenv and virtualenv-wrapper. You can download neo4j from [offical website](https://neo4j.com/).

    pip install virtualenv
    pip install virtualenvwrapper
    ...(After a series of settings)
    pip install django1.11
    pip install restframework
    pip install corsheaders
    pip install neomodel
    pip install django-neomodel
    pip install sslserver

#### After Installation

    ~/neo4j-3.2.0/bin/neo4j start
    cd SJTU-SSE/python/neo4j_v3
    python manager.py runserver (0.0.0.0:[8000])

If you want to support https, you can replace the last command into 
```
python manage.py runsslserver --certificate [path to ssl-certificate] --key [path to ssl-key] 0.0.0.0:[8000]
```

Go to *http://localhost:8000/* to check the API.
You can also visit *http://localhost:7474/* to look through neo4j web browser where you can have a look at scapegoat tree in graph database.

#### Illustration for API 
We have deployed the service on  *http://115.159.88.104:2118/*
* Api-Root : &nbsp; **GET**  &nbsp;&nbsp; (/)
* Ciphers : &nbsp; **GET**, **POST**  &nbsp;&nbsp; (/ciphertext)
* Details : &nbsp; **GET**, **DELETE**, **PUT** &nbsp;&nbsp; (/ciphertext/id)
* Querys  : &nbsp; **GET** &nbsp;&nbsp; (/ciphertext/?key=3|5|7-2|1|8)
> When you search files that include some keys such as A, B and C and do not include some keys such as C, D and E, you should send **GET** http request to http://115.159.88.104:2118/ciphertext/?key=A|B|C-D|E|F where A~F are non-negative numbers.


### Screenshots for API
<p align="center">
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v3_ciphers.png", width=700, height=530 />
<img src="https://github.com/wangjksjtu/SJTU-SSE/blob/master/docs/neo4j_v3_graph.png", width=650, height=530/>
</p>

### SSE: Neo4j Many to Many API
We also implement many-to-many SSE in neo4j database. The environments and commands are similar to Neo4j Tree Version and the whole codes can be found python/neo4j_v2 folder in this repo. This API also supports create, delete, update, retrieve and search files. After deployment, you can also go to port 8000 and 7474 to check API and graph. 

### SSE: Neo4j with Django Demo (modified this [repo](https://github.com/johanlundberg/neo4j-django-tutorial/))
#### Quickstart
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


