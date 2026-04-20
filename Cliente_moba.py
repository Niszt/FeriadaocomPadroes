
from  abc import ABC, abstractmethod

class Skin(ABC):
    def __init__(self,nome,campeao, preco): 
        self.nome = nome
        self.campeao = campeao
        self.preco = preco
    @abstractmethod
    def detalhe(self):
        pass

class SkinUltimate(Skin):
    def detalhe(self):
        return f"skin Ultimate {self.campeao} {self.nome}  - preco {self.preco} RP"

class SkinRara(Skin):
    def detalhe(self):
        return f"skin Rara {self.campeao} {self.nome} - preco {self.preco} RP"
             
class SkinLendaria(Skin):
    def detalhe(self):
        return f"skin Lendaria {self.campeao} {self.nome} - preco {self.preco} RP"

class FabricaSkin:
    @staticmethod
    def criar_skin(raridade,nome, campeao):
        if raridade =='ultimate':
            return SkinUltimate(nome, campeao, 3250)
        elif raridade == 'rara':
            return SkinRara(nome, campeao, 1350)
        elif raridade == 'lendaria':
            return SkinLendaria(nome, campeao, 1820)
        else:
            raise ValueError(f"Raridade {raridade} desconhecida")

class SkinWildRift:
    def __init__(self, titulo, personagem, custo_wild_cores):
        self.titulo = titulo
        self.personagem = personagem
        self.custo_wild_cores = custo_wild_cores
        
    def info_skin_mobile(self):
        return f"Skin Mobile {self.personagem} {self.titulo} - Custo: {self.custo_wild_cores} WC"

class AdaptadorSkinCelulol(Skin):
    def __init__(self, skin_externa: SkinWildRift):
        preco_rp = int(skin_externa.custo_wild_cores*1.8)
        super().__init__(
            nome=skin_externa.titulo,
            campeao = skin_externa.personagem,
            preco = preco_rp
        )
        self._skin_externa = skin_externa
    
    def detalhe(self):
        return f"{self._skin_externa.info_skin_mobile()}"

class SkinDecorador(Skin):
    def __init__(self,skin_original: Skin):
        self._skin_original = skin_original
        super().__init__(skin_original.nome,skin_original.campeao,skin_original.preco)
    
    @abstractmethod
    def detalhe(self):
        pass

class DecoradorBorda(SkinDecorador):
    def __init__(self, skin_original:Skin):
        super().__init__(skin_original)
        self.preco = self._skin_original.preco + 350
    def detalhe(self):
        return f"{self._skin_original.detalhe()}"+" com borda personalizada"
    
class DecoradorVoz(SkinDecorador):
    def __init__(self, skin_original:Skin):
        super().__init__(skin_original)
        self.preco = self._skin_original.preco + 500
    def detalhe(self):
        return f"{self._skin_original.detalhe()}"+" com pacote de voz personalizado"
    
class Inventario():
    def __init__(self):
        self._skins=[]
        
    def add_skin(self, skin: Skin):
        self._skins.append(skin)
               
    def listar_skin(self, nome_perfil):
        print(f"\n skins do invocador {nome_perfil}:")
        for i in self._skins:
            print(f"{i.detalhe()}\n")
        print(f"\n")
                
    
class Observador(ABC):
    @abstractmethod
    def atualizar(self, msg):
        pass
        
class Cliente(Observador):
    def __init__(self, nome_perfil,_nome_usuario,_senha,moeda_jogo, nivel=1):
        self.nome_perfil = nome_perfil
        self._nome_usuario = _nome_usuario
        self._senha = _senha
        self._moeda_jogo = moeda_jogo
        self._amigos = []
        self.inventario = Inventario()
        self.nivel = nivel
        self.banido = False
        
    def atualizar(self, msg):
        print(f"aviso para {self.nome_perfil}: {msg}")

    def add_amigo(self, amigo : Observador):
        self._amigos.append(amigo)
        
    def atualizar(self, msg):
        print(f"aviso para {self.nome_perfil}: {msg}")
        
    def notificar_amigos(self,msg):
        for amigo in self._amigos:
            amigo.atualizar(msg)

class LojaRiot:
    _intancia = None
    def __new__(cls):
        if cls._intancia is None:
            cls._intancia = super().__new__(cls)
            print("\n Loja criada")
        return cls._intancia
    
    def comprar_skins(self, cliente:Cliente, skin):
        print(f"\n processando a compra da skin {skin.nome}")
        if cliente._moeda_jogo >= skin.preco:
            cliente._moeda_jogo -= skin.preco
            cliente.inventario.add_skin(skin)
            print(f"{cliente.nome_perfil} voce comprou a skin {skin.nome}. Saldo restante na conta de {cliente._moeda_jogo} RP")
        else:
            print(f"saldo insuficiente para comprar a {skin.detalhe()}")

# primeiro crio a interface que representa o que o objeto real e proxy vao usar
class IPartida(ABC):
    @abstractmethod
    def buscar_partida(self, cliente : Cliente):
        pass

# comecando pelo objeto real
class FilaRanqueada(IPartida):
    def buscar_partida(self, cliente):
        print(f"{cliente.nome_perfil} entrou na fila. Buscando mais 9 jogadores.")

class Proxy_FilaRanqueada(IPartida):
    def __init__(self):
        self._partida_real = FilaRanqueada()
        # self._amigos = []
        
    def buscar_partida(self, cliente:Cliente):
        if cliente.banido:
            print(f"{cliente.nome_perfil} está banido por ser tóxico no chat!")
        elif cliente.nivel < 30:
            print(f"para jogar na fila ranqueada é necessário ter no mínimo lvl 30. O invocador {cliente.nome_perfil} é nível {cliente.nivel}.")
        else:
            print("Tudo certo! Liberando acesso ao Servidor..")
            cliente.notificar_amigos(f"O invocador {cliente.nome_perfil} entrou em um grupo para jogar ranqueada")
            self._partida_real.buscar_partida(cliente)
            
        
        
class FachadaClientLoL:
    # aqui eu vou trazer as classes que interagem com o usuario
    def __init__(self):
        self.fabrica = FabricaSkin()
        self.loja = LojaRiot()
        self.ranked = Proxy_FilaRanqueada()
    # encapsulei o metodo que cria e que compra skin da loja 
    def criar_skin(self,raridade,nome_skin, campeao):
        return self.fabrica.criar_skin(raridade,campeao,nome_skin)
    
    def criar_skin_externa(self,titulo,personagem,custo):
        skin_externa = SkinWildRift(titulo, personagem, custo)
        return AdaptadorSkinCelulol(skin_externa)
    def add_borda(self, skin: Skin):
        return DecoradorBorda(skin)
    def add_voz(self, skin: Skin):
        return DecoradorVoz(skin)
    
    def compra_skin(self,cliente:Cliente, skin:Skin):
        self.loja.comprar_skins(cliente,skin)
    
    def Iniciar_ranked(self,cliente:Cliente):
        self.ranked.buscar_partida(cliente)
    
    def adicionar_amigo(self,jogador:Cliente,amigo:Cliente):
        jogador.add_amigo(amigo)
        print(f"\n{amigo.nome_perfil} foi adicionado a sua lista de amizade")
    
if __name__ == "__main__":
    cliente_lol = FachadaClientLoL()
    
    invocador1 = Cliente("Hide on Bush#SKT","Faker","melhordomundo@123",6000,nivel=700)   
    invocador2 = Cliente("Nick#BR1","Nick","souNick21314",12000,nivel=350)  
    invocador3 = Cliente("Tyler1", "hehexd", "senha789", 0, nivel=100)
    invocador4 = Cliente("LuluDeDemacia", "luluhahaha", "senha9089", 0, nivel=10)
    invocador3.banido = True 
    
    cliente_lol.adicionar_amigo(invocador1, invocador2)
    cliente_lol.adicionar_amigo(invocador2, invocador3)
    cliente_lol.adicionar_amigo(invocador2,invocador4)
    
    skin1 = cliente_lol.criar_skin("rara","Yasuo","Projeto Yasuo")    
    skin2 = cliente_lol.criar_skin("lendaria","Lee sin", "Lee Sin Punhos Divinos")
    skin3 = cliente_lol.criar_skin("ultimate","Lux","Lux Elementalista")
    skin3_borda = cliente_lol.add_borda(skin3)
    skin3_borda_voz = cliente_lol.add_voz(skin3_borda)
    skin_astramante_adaptada = cliente_lol.criar_skin_externa("Astramante", "Twisted Fate", 990)
    cliente_lol.compra_skin(invocador1,skin3)
    cliente_lol.compra_skin(invocador1,skin2)
    cliente_lol.compra_skin(invocador1,skin1)
    # cliente_lol.compra_skin(invocador2,skin3)
    cliente_lol.compra_skin(invocador2,skin2)
    cliente_lol.compra_skin(invocador2,skin1)
    cliente_lol.compra_skin(invocador2,skin_astramante_adaptada)
    cliente_lol.compra_skin(invocador2,skin3_borda_voz)
    cliente_lol.compra_skin(invocador1,skin3_borda)
    cliente_lol.compra_skin(invocador3,skin3_borda)
    
    invocador1.inventario.listar_skin(invocador1.nome_perfil)
    invocador2.inventario.listar_skin(invocador2.nome_perfil)
    
    cliente_lol.Iniciar_ranked(invocador1)
    cliente_lol.Iniciar_ranked(invocador2)
    cliente_lol.Iniciar_ranked(invocador3)
    cliente_lol.Iniciar_ranked(invocador4)
    
    
