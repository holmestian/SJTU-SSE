## This is a simple API without user and authorization. ##

### Environment ###

* Python2.7 
* Django1.10 
* Django rest-framework 3
###

    cd unauth_server/
    g++ -o treeLib.so -shared -fPIC ciphertext/tree.py
    python manage.py runserver [0.0.0.0:8000]

You can visit *http://localhost:8000/* to check the API.
