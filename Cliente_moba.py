
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
    
    def comprar_skins(self, skin: Skin):
        if self._moeda_jogo >= skin.preco:
            self._moeda_jogo -= skin.preco
            self._skins.append(skin)
            print(f"{self.nome_perfil} voce comprou a skin {skin.nome}. Saldo restante na conta de {self._moeda_jogo} RP")
        else:
            print(f"saldo insuficiente para comprar a {skin.detalhe()}")
            
    def listar_skin(self):
        print(f"\n skins do invocador {self.nome_perfil}:")
        for i in self._skins:
            print(f"{i.detalhe()}\n")
        print(f"\n")
        
if __name__ == "__main__":
    
    fabrica = FabricaSkin()
    
    invocador = Cliente("Hide on Bush","Faker","melhordomundo@123",6000)        
    skin1 = fabrica.criar_skin("rara","Yasuo","Projeto Yasuo")    
    skin2 = fabrica.criar_skin("lendaria","Lee sin", "Lee Sin Punhos Divinos")
    skin3 = fabrica.criar_skin("ultimate","Lux","Lux Elementalista")
    
    invocador.comprar_skins(skin3)
    invocador.comprar_skins(skin2)
    invocador.comprar_skins(skin1)
    
    invocador.listar_skin()

    
    
