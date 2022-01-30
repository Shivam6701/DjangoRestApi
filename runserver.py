from waitress import serve

from  DjangoRestApi.wsgi import application

if __name__=='__main__':
    serve(application,host='localhost',port='7000')