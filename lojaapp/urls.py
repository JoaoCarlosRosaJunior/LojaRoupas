from django.urls import path,include
from .views import *


app_name = "lojaapp"

urlpatterns = [
    path("",HomeView.as_view(), name="home"),
    path("sobre/",SobreView.as_view(), name="sobre"),
    path("contato/",ContatoView.as_view(), name="contato"),
    path("produtos/<slug:slug>",ProdutosView.as_view(), name="produtos"),
    path("todos-produtos/",TodosProdutosView.as_view(), name="todos-produtos"),
    path("carrinho/", CarrinhoView.as_view(), name="carrinho"),
    path("addcarrinho-<int:pro_id>/", AddCarrinhoView.as_view(), name="addcarrinho"),
    path("manipular-carro/<int:cp_id>/", ManipularCarroView.as_view(), name="manipularcarro"),
]