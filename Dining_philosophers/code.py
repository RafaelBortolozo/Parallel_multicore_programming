from random import randint
from time import sleep
from threading import Thread, Lock

pratos = [0, 0, 0, 0, 0]
nomes = ['Filósofo 1', 'Filósofo 2', 'Filósofo 3', 'Filósofo 4', 'Filósofo 5']
garfos = [Lock() for _ in range(5)]
timeToEat = [randint(1, 5) for _ in range(5)] 
timeToWait = [randint(25, 50) for _ in range(5)] 
mesa = [Filosofo(nomes[i], garfos[i % 5], garfos[(i + 1) % 5], timeToEat[i], timeToWait[i]) for i in range(5)]

for filosofo in mesa:
    filosofo.start()  
    sleep(1)

class Filosofo(Thread):
    alive = True

    def __init__(self, nome, garfo_esquerdo, garfo_direito, tempo_comendo, tempo_esperando):
        Thread.__init__(self)
        self.nome = nome
        self.tempo_comendo = tempo_comendo
        self.tempo_esperando = tempo_esperando
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito

    def run(self):
        while self.alive:
            tempo_aguardando = 0
            random = randint(5, 15)

            print(f"\n{self.nome} está pensando")
            sleep(random) 
            pronto_para_comer = self.comer()

            if pronto_para_comer == 1: #verificação se ele conseguiu comer ou nao
                tempo_aguardando = 0
            else:
                tempo_aguardando += random

            if (tempo_aguardando + 5) > self.tempo_esperando:  #resolução do starvation
                self.garfo_esquerdo.acquire(True)
                self.garfo_direito.acquire(True)
                print(f"\n{self.nome} começou a comer")
                sleep(self.tempo_comendo)
                print(f"\n{self.nome} parou de comer")
                pratos[nomes.index(self.nome)] += 1
                print("Quantidade que cada filósofo comeu: ", pratos)
                self.garfo_esquerdo.release()  # libera o garfo 1
                self.garfo_direito.release()  # libera o garfo 2

    def comer(self):
        garfo1, garfo2, nome = self.garfo_esquerdo, self.garfo_direito, self.nome

        print(f"\n{self.nome} quer comer e tenta pegar um garfo")

        garfo1.acquire(True)
        noLocked = garfo2.acquire(False)  # verifica se o segundo não está sendo usado

        if noLocked:
            print(f"\n{self.nome} começou a comer")
            sleep(self.tempo_comendo)
            print(f"\n{self.nome} parou de comer")
            pratos[nomes.index(self.nome)] += 1  # quantas vezes cada filosofo comeu
            print("Quantidade que cada filósofo comeu: ", pratos)
            garfo1.release()  # libera o garfo 1
            garfo2.release()  # libera o garfo 2
            return 1
        else:
            garfo1.release()  # libera o primeiro garfo pra não gerar deadlock
            print(f"\n{self.nome} não conseguiu comer")
            return 0
