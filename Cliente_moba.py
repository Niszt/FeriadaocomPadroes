
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
        
            
    
class Cliente():
    def __init__(self, nome_perfil,_nome_usuario,_senha,moeda_jogo):
        self.nome_perfil = nome_perfil
        self._nome_usuario = _nome_usuario
        self._senha = _senha
        self._moeda_jogo = moeda_jogo
        self._amigos = []
        self._skins = []
    
    def add_skin(self, skin: Skin):
        self._skins.append(skin)
               
    def listar_skin(self):
        print(f"\n skins do invocador {self.nome_perfil}:")
        for i in self._skins:
            print(f"{i.detalhe()}\n")
        print(f"\n")


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
            cliente.add_skin(skin)
            print(f"{cliente.nome_perfil} voce comprou a skin {skin.nome}. Saldo restante na conta de {cliente._moeda_jogo} RP")
        else:
            print(f"saldo insuficiente para comprar a {skin.detalhe()}")
        
if __name__ == "__main__":
    
    fabrica = FabricaSkin()
    loja = LojaRiot()
    invocador1 = Cliente("Hide on Bush#SKT","Faker","melhordomundo@123",6000)   
    invocador2 = Cliente("Nick#BR1","Nick","souNick21314",12000)     
    skin1 = fabrica.criar_skin("rara","Yasuo","Projeto Yasuo")    
    skin2 = fabrica.criar_skin("lendaria","Lee sin", "Lee Sin Punhos Divinos")
    skin3 = fabrica.criar_skin("ultimate","Lux","Lux Elementalista")
    loja.comprar_skins(invocador1,skin3)
    loja.comprar_skins(invocador1,skin2)
    loja.comprar_skins(invocador1,skin1)
    loja.comprar_skins(invocador2,skin3)
    loja.comprar_skins(invocador2,skin2)
    loja.comprar_skins(invocador2,skin1)
    invocador1.listar_skin()
    invocador2.listar_skin()

    
    
