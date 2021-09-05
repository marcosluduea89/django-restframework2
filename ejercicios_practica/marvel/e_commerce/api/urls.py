from django.urls import path
from e_commerce.api.marvel_api_views import *

# Importamos las API_VIEWS:
from e_commerce.api.api_views import *

urlpatterns = [
    # User APIs:
    path('user/login/', LoginUserAPIView.as_view()),

    # APIs de Marvel
    path('get_comics/',get_comics),
    path('purchased_item/',purchased_item),
    
    # Comic API View:
    path('comics/get', GetComicAPIView.as_view()),
    path('comics/<comic_id>/get', GetOneComicAPIView.as_view()),
    path('comics/post', PostComicAPIView.as_view()),
    path('comics/get-post', ListCreateComicAPIView.as_view()),
    path('comics/<pk>/update', RetrieveUpdateComicAPIView.as_view()),
    path('comics/<pk>/delete', DestroyComicAPIView.as_view()),

    # TODO: Wish-list API View

    path('wish/get', GetWishListAPIView.as_view()),
    path('wish/post', PostWishListAPIView.as_view()),
    path('wish/get-post', ListCreateWishListAPIView.as_view()),
    path('wish/<pk>/update', RetrieveUpdateWishListAPIView.as_view()),
    path('wish/<pk>/delete', DestroyWishListAPIView.as_view()),

    # api mixta con informaciond de los comics de la wishlist de un usuario en particular
    path('favs/<username>/get', GetUserFavsAPIView.as_view())

]