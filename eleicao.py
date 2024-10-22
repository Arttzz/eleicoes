import pickle
from typing import List
from common import *
from Interface_Eleicao import Transparencia
import csv

class Urna(Transparencia):
    mesario : Pessoa
    __secao : int
    __zona : int
    __eleitores_presentes : List[Eleitor] = []
    __votos = {} #dicionario chave = numero do candidato, valor é a quantidade de votos

    def __init__(self, mesario : Pessoa, secao : int, zona : int,
                 candidatos : List[Candidato], eleitores : List[Eleitor]):
        self.mesario = mesario
        self.__secao = secao
        self.__zona = zona
        self.__nome_arquivo = f'{self.__zona}_{self.__secao}.pkl'
        self.__candidatos = candidatos
        self.__eleitores : List[Eleitor] = []
        for eleitor in eleitores:
            if eleitor.zona == zona and eleitor.secao == secao:
                self.__eleitores.append(eleitor)

        for candidato in self.__candidatos:
            self.__votos[candidato.get_numero()] = 0
        self.__votos['BRANCO'] = 0
        self.__votos['NULO'] = 0

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def get_eleitor(self, titulo : int):
        for eleitor in self.__eleitores:
            if eleitor.get_titulo() == titulo:
                return eleitor
        return False
    
    def get_secao(self):
            return self.__secao
    
    def get_zona(self):
            return self.__zona

    def registrar_voto(self, eleitor : Eleitor, n_cand : int):
        self.__eleitores_presentes.append(eleitor)
        if n_cand in self.__votos:
            self.__votos[n_cand] += 1
        else:
            self.__votos['NULO'] += 1

        with open(self.__nome_arquivo, 'wb') as arquivo:
            pickle.dump(self.__votos, arquivo)

    def to_csv(self):
        with open(f'{self.__zona}_{self.__secao}.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Seção', 'Zona', 'Titulos dos Eleitores Presentes'])

            for eleitores in self.__eleitores:
                writer.writerow([self.get_secao(), self.get_zona(), eleitores.get_titulo()])
                
    def to_txt(self):
        with open(f'{self.__zona}_{self.__secao}.txt', mode='w') as file:
            for eleitores in self.__eleitores:
                file.write(eleitores.__str__())
            
    def __str__(self):
        info =  f'Urna da seção {self.__secao}, zona {self.__zona}\n'
        info += f'Mesario {self.mesario}\n'
        return info
    
    
if __name__ == "__main__":
    c1 = Candidato("Arthur", "123132314", "123424214", 99)
    c2 = Candidato("Diana", "12331", "123414", 68)

    e1 = Eleitor("Jose", "123144", "12114", 1, 54, 214)
    e2 = Eleitor("Cleber", "123144", "12114", 2, 54, 214)
    e3 = Eleitor("Cleber", "123144", "12114", 3, 54, 214)

    urna = Urna(e3, 54, 214, [c1, c2], [e1, e2, e3])
    urna.registrar_voto(e1, 99)
    urna.to_csv()
    urna.to_txt()
    print(urna)