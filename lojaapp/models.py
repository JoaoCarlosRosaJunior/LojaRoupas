from operator import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    titulo = models.CharField(max_length=128)
    slug = models.SlugField(unique = True)

    def __str__(self):
        return self.titulo

class Produto(models.Model):
    titulo = models.CharField(max_length=128)
    slug = models.SlugField(unique = True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="Produtos")
    preco = models.PositiveIntegerField()
    venda = models.PositiveIntegerField()
    descricao = models.TextField()
    visualizacao = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.titulo

class Cliente(models.Model):
    user =  models.OneToOneField(User, on_delete = models.CASCADE)
    #slug = models.SlugField(User, on_delete=models.CASCADE)
    nome_completo = models.CharField(max_length = 128)
    endereco = models.CharField(max_length = 256, null = True, blank = True)
    criado_em = models.DateField(auto_now_add = True)
    email = models.EmailField(null = True, blank = True)

    def __str__(self):
        return self.nome_completo

class Carrinho(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete = models.SET_NULL, null = True, blank = True)
    total = models.PositiveIntegerField(default = 0)
    criado_em = models.DateField(auto_now_add = True)

    def __str__(self):
        return "Carrinho:" + str(self.id)

class CarrinhoProduto(models.Model): 
    carrinho = models.ForeignKey(Carrinho, on_delete = models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete = models.CASCADE)
    avaliacao = models.PositiveIntegerField()
    quantidade = models.PositiveIntegerField()
    subtotal = models.PositiveIntegerField()

    def __str__(self):
        return "Carrinho:" + str(self.carrinho.id) + "CarrinhoProduto" + str(self.id)

PEDIDO_STATUS = (
    ("Pedido Recebido", "Pedido Recebido"),
    ("Pedido Processando", "Pedido Processando"),
    ("Pedido a Caminho", "Pedido a Caminho"),
    ("Pedido Completado", "Pedido Completado"),
    ("Pedido Cancelado", "Pedido Cancelado")
)

class Pedido(models.Model):
    carrinho = models.ForeignKey(Carrinho, on_delete = models.CASCADE)
    ordenado_por = models.CharField(max_length = 256)
    endereco_envio = models.CharField(max_length = 128)
    telefone = models.CharField(max_length = 32)
    subtotal = models.PositiveIntegerField()
    total = models.PositiveIntegerField()
    pedido_status = models.CharField(max_length = 64, choices=PEDIDO_STATUS)
    criado_em = models.DateField(auto_now_add = True)

    def __str__(self):
        return "Pedido:" + str(self.id)
