# Primero, importamos los serializadores
from django.http import response
from e_commerce.api.serializers import *

# Segundo, importamos los modelos:
from django.contrib.auth.models import User
from e_commerce.models import Comic,WishList

# Luego importamos las herramientas para crear las api views con Django REST FRAMEWORK:

# (GET) Listar todos los elementos en la entidad:
from rest_framework.generics import ListAPIView

# (POST) Inserta elementos en la DB
from rest_framework.generics import CreateAPIView

# (GET-POST) Para ver e insertar elementos en la DB
from rest_framework.generics import ListCreateAPIView

from rest_framework.generics import RetrieveUpdateAPIView

from rest_framework.generics import DestroyAPIView

# Esto en realidad lo podemos hacer como:
# from rest_framework.generics import (
#     ListAPIView,
#     CreateAPIView,
#     ListCreateAPIView,
#     RetrieveUpdateAPIView,
#     DestroyAPIView)
# de manera más prolija

# Importamos librerías para gestionar los permisos de acceso a nuestras APIs
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import JSONParser


mensaje_headder = '''
Ejemplo de header:

`headers = {
  'Authorization': 'Token 92937874f377a1ea17f7637ee07208622e5cb5e6',
  'actions': 'PUT',
  'Content-Type': 'application/json',
  'Cookie': 'csrftoken=cfEuCX6qThpN6UC9eXypC71j6A4KJQagRSojPnqXfZjN5wJg09hXXQKCU8VflLDR'
}`
'''
# NOTE: APIs genéricas:

class GetComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class PostComicAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO POST]`
    Esta vista de API nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class ListCreateComicAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-POST]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    Tambien nos permite hacer un insert en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class RetrieveUpdateComicAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET-PUT-PATCH]`
    Esta vista de API nos permite actualizar un registro, o simplemente visualizarlo.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class DestroyComicAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO DELETE]`
    Esta vista de API nos devuelve una lista de todos los comics presentes 
    en la base de datos.
    '''
    queryset = Comic.objects.all()
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

# NOTE: APIs MIXTAS:

class GetOneComicAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API nos devuelve un comic en particular de la base de datos.
    '''
    serializer_class = ComicSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        '''
        Sobrescribimos la función `get_queryset` para poder filtrar el request 
        por medio de la url. En este caso traemos de la url por medio de `self.kwargs` 
        el parámetro `comic_id` y con él realizamos una query para traer 
        el comic del ID solicitado.  
        '''
        try:
            comic_id = self.kwargs['comic_id']
            queryset = Comic.objects.filter(id=comic_id)
            return queryset
        except Exception as error:
            return {'error': f'Ha ocurrido la siguiente excepción: {error}'}

class LoginUserAPIView(APIView):
    '''
    Vista de API personalizada para recibir peticiones de tipo POST.
    Esquema de entrada:
    {"username":"root", "password":12345}
    
    Utilizaremos JSONParser para tener  'Content-Type': 'application/json'
    '''
    parser_classes = [JSONParser]
    authentication_classes = []
    permission_classes = []

    def post(self, request,format=None):
        '''
        Esta función sobrescribe la función post original de esta clase,
        recibe "request" y hay que setear format=None, para poder recibir los datos en request.data 
        la idea es obtener los datos enviados en el request y autenticar al usuario con la 
        función "authenticate()", la cual devuelve el estado de autenticación.
        \nLuego con estos datos se consulta el Token generado para el usuario, si no lo tiene asignado,
        se crea automáticamente.
        \nEsquema de entrada:
        \n`{"username":"root", "password":12345}`
        \nUtilizaremos JSONParser para tener  `'Content-Type': 'application/json'`
        '''
        user_data = {}
        try:
            # Obtenemos los datos del request:
            username = request.data.get('username')
            password = request.data.get('password')
            # Obtenemos el objeto del modelo user, a partir del usuario y contraseña,
            # NOTE: es importante el uso de este método, porque aplica el hash del password!
            account = authenticate(username=username, password=password)

            if account:
                # Si el usuario existe y sus credenciales son validas, tratamos de obtener el TOKEN:
                try:
                    token = Token.objects.get(user=account)
                except Token.DoesNotExist:
                    # Si el TOKEN del usuario no existe, lo creamos automáticamente:
                    token = Token.objects.create(user=account)
                # Con todos estos datos, construimos un JSON de respuesta:
                user_data['user_id'] = account.pk
                user_data['username'] = username
                user_data['first_name'] = account.first_name
                user_data['last_name'] = account.first_name
                user_data['email']=account.email
                user_data['is_active'] = account.is_active
                user_data['token'] = token.key                
                # Devolvemos la respuesta personalizada
                return Response(user_data)
            else:
                # Si las credenciales son invalidas, devolvemos algun mensaje de error:
                user_data['response'] = 'Error'
                user_data['error_message'] = 'Credenciales invalidas'
                return Response(user_data)

        except Exception as error:
            # Si aparece alguna excepción, devolvemos un mensaje de error
            user_data['response'] = 'Error'
            user_data['error_message'] = error
            return Response(user_data)

# TODO: Agregar las vistas genericas que permitan realizar un CRUD del modelo de wish-list.

class GetWishListAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
     `[METODO GET]`
     Esta vista de API nos devuelve una lista de todos los Wishlists presentes 
     en la base de datos.
     '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class PostWishListAPIView(CreateAPIView):
    __doc__ = f'''{mensaje_headder}
     `[METODO GET]`
     Esta vista de API permite insertar en la base de datos.
     '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class ListCreateWishListAPIView(ListCreateAPIView):
    __doc__ = f'''{mensaje_headder}
     `[METODO GET]`
     Esta vista de API permite ver una lista de comic y insertar en la base de datos.
     '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class RetrieveUpdateWishListAPIView(RetrieveUpdateAPIView):
    __doc__ = f'''{mensaje_headder}
     `[METODO GET]`
     Esta vista de API permite actualizar un registro.
     '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 

class DestroyWishListAPIView(DestroyAPIView):
    __doc__ = f'''{mensaje_headder}
     `[METODO GET]`
     Esta vista de API permite eliminar un registro.
     '''
    queryset = WishList.objects.all()
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser] 


# TODO: Crear una vista generica modificada para traer todos los comics que tiene un usuario


class GetUserFavsAPIView(ListAPIView):
    __doc__ = f'''{mensaje_headder}
    `[METODO GET]`
    Esta vista de API mixta que nos devuelve los comics favoritos de un usuario en particular.
    '''
    serializer_class = WishListSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_queryset(self):
        '''
        Sobrescribimos la función `get_queryset` para poder filtrar el request 
        por medio de la url. En este caso traemos de la url por medio de `self.kwargs` 
        el parámetro `username` y con él realizamos la logica para  traer 
        la lista de comic wishlist.  
        '''
        # declaramps una lista de diccionarios con la informacion de los comics 
        json_wishlist =[] 
        try:
            # nos traemos el username de la url
            username = self.kwargs['username']
            user = User.objects.filter(username=username) # buscamos el user(de la base de datos) en base al pasado por parametro url
            wish_list = WishList.objects.filter(user_id=user.first(), favorite=True) # nos traemos la lista de objetos wish del usuario
            # print (wish_list)
            #hacemos una lista con los ids de comics
            
            comic_ids = []
            for comic_id in wish_list:
                comic_ids.append(comic_id['comic_id'])
                    
                
            for id_comic in comic_ids:
                comic_obj = Comic.objects.filter(id=id_comic)
                wishlist = {}
                wishlist['marvel_id'] = comic_obj.marvel_id
                wishlist['title'] = comic_obj.title
                wishlist['description'] = comic_obj.description
                wishlist['price'] = comic_obj.price
                wishlist['stock_qty'] = comic_obj.stock_qty
                wishlist['picture'] = comic_obj.picture
                json_wishlist.append(wishlist)
                    

            return response(json_wishlist)

        
        
        except Exception as error:
            return {'error': f'Ha ocurrido la siguiente excepción: {error}'}