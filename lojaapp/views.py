from django.shortcuts import render, redirect
from django.views.generic import View,TemplateView
from .models import *
# Create your views here.

class HomeView(TemplateView): 
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_list'] = Produto.objects.all()
        return context

class SobreView(TemplateView): 
    template_name = "sobre.html"

class ContatoView(TemplateView): 
    template_name = "contato.html"

class ProdutosView(TemplateView): 
    template_name = "produtos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        url_slug = self.kwargs['slug']
        produto = Produto.objects.get(slug=url_slug)
        produto.visualizacao += 1
        produto.save()
        context['produto'] = produto
        return context

class TodosProdutosView(TemplateView): 
    template_name = "todos-produtos.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todas_categorias'] = Categoria.objects.all()
        return context

class CarrinhoView(TemplateView): 
    template_name = "carrinho.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        carrinho_id = self.request.session.get("carro_id", None)
        if carrinho_id:
            carrinho = Carrinho.objects.get(id=carrinho_id)
        else: 
            carrinho = None
        context['carrinho'] = carrinho
        return context

class AddCarrinhoView(TemplateView): 
    template_name = "addcarrinho.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        produto_id = self.kwargs['pro_id']
        produto_object = Produto.objects.get(id = produto_id)
        carrinho_id = self.request.session.get("carro_id", None)
        if carrinho_id:
            carrinho_object = Carrinho.objects.get(id=carrinho_id)
            produto_no_carrinho = carrinho_object.carrinhoproduto_set.filter(produto = produto_object)
            if produto_no_carrinho.exists():
                carrinhoproduto = produto_no_carrinho.last()
                carrinhoproduto.quantidade += 1
                carrinhoproduto.subtotal += produto_object.preco
                carrinhoproduto.save()
                carrinho_object.total += produto_object.preco
                carrinho_object.save()
            else: 
                carrinhoproduto = CarrinhoProduto.objects.create(
                    carrinho = carrinho_object,
                    produto = produto_object,
                    avaliacao = produto_object.preco,
                    quantidade = 1,
                    subtotal = produto_object.preco,
                )

                carrinho_object.total += produto_object.preco
                carrinho_object.save()
        else: 
            carrinho_object = Carrinho.objects.create(total=0)
            self.request.session['carro_id'] = carrinho_object.id

            carrinhoproduto = CarrinhoProduto.objects.create(
                    carrinho = carrinho_object,
                    produto = produto_object,
                    avaliacao = produto_object.preco,
                    quantidade = 1,
                    subtotal = produto_object.preco,
                )

            carrinho_object.total += produto_object.preco
            carrinho_object.save()
        return context

class ManipularCarroView(View): 
    def get_context_data(self, request,*args,**kwargs):
        cp_id = self.kwargs["cp_id"]
        acao = request.GET.get("acao")
        cp_object = CarrinhoProduto.objects.get(id=cp_id)
        carrinho_object = cp_object.carrinho

        if acao =="inc":
            cp_object.quantidade += 1
            cp_object.subtotal += cp_object.avaliacao
            cp_object.save()
            carrinho_object.total += cp_object.avaliacao
            carrinho_object.save()
        elif acao =="dcr":
            pass
        elif acao =="rmv":
            pass
        else:
            pass
        return redirect("lojaapp:carrinho")