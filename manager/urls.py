from django.urls import path
from .views import IndexM_View, ProdutoCreate, ProdutoList, ProdutoUpdate 
from .views import Catalogo, Checkin, ProdutoCompra, Sucesso
from .views import cart_add, cart_detail, cart_remove
# from .views import form_CriarProduto
# from . import views

app_name = 'manager'

# pk permite acessar, é a chave primária/id do produto em questão

urlpatterns = [
    path('', IndexM_View.as_view(), name='index'),
    path('cadastro/', ProdutoCreate.as_view(), name='add'),
    path('lista/', ProdutoList.as_view(), name= 'list'),
    path('att/<int:pk>/', ProdutoUpdate.as_view(), name='att'),
    
    path('catalogo/', Catalogo.as_view(), name= 'catalog'),
    path('checkin/', Checkin.as_view(), name= 'checkin'),
    path('final/', Sucesso.as_view(), name= 'final'),

    path('produto/<int:pk>', ProdutoCompra.as_view(), name= 'produto'),

    path('cart/', cart_detail, name="cart"),
    path('add/<int:pk>/', cart_add, name="cartadd"),
    path('del/<int:pk>/', cart_remove, name="cartdel"),

    # path('cadastro/', form_CriarProduto, name='manager_produto'),
    # path('editar/', form_editarproduto, name='form_criarproduto'),
    # path('lista/', lista_produtos, name='lista_produtos'),
]