from random import randint
from time import sleep
from threading import Thread, Lock
from colorama import Fore

pratos = [0, 0, 0, 0, 0]

class Filosofo(Thread):
    vivo = True

    def __init__(self, nome, garfo_esquerdo, garfo_direito, tempo_alimentacao, tempo_esperando):
        Thread.__init__(self)
        self.nome = nome
        self.tempo_alimentacao = tempo_alimentacao # Duracao da refeicao
        self.tempo_esperando = tempo_esperando # Tempo acumulado esperando pra comer
        self.garfo_esquerdo = garfo_esquerdo       
        self.garfo_direito = garfo_direito

    # Funcao principal
    def run(self):
        while 1:
            tempo_acumulado = 0
            tempo_aleatorio = randint(5, 15)

            print(Fore.GREEN + f"{self.nome} - pensando")
            sleep(tempo_aleatorio) 
            comeu = self.comer()

            if comeu == 1: #verificação se ele conseguiu comer ou nao
                tempo_acumulado = 0
            else:
                tempo_acumulado += tempo_aleatorio

            # Come caso passar muito tempo, resolução do starvation
            if (tempo_acumulado + 5) > self.tempo_esperando:  
                self.garfo_esquerdo.apanhar(True)
                self.garfo_direito.apanhar(True)
                print(Fore.RED + f"{self.nome} - comendo")
                sleep(self.tempo_alimentacao)
                print(Fore.GREEN + f"{self.nome} - pensando")
                pratos[nomes.index(self.nome)] += 1
                # print("Quantidade que cada filósofo comeu: ", pratos)
                self.garfo_esquerdo.release()  # libera o garfo 1
                self.garfo_direito.release()  # libera o garfo 2

    # Tenta comer. Caso contrario, solta os garfos e espera
    def comer(self):
        garfo1, garfo2 = self.garfo_esquerdo, self.garfo_direito

        # Pega um garfo
        print(Fore.YELLOW + f"{self.nome} - esperando")
        garfo1.apanhar(True)

        # Tenta pegar outro garfo
        noLocked = garfo2.apanhar(False)  # verifica se o segundo garfo não está sendo usado

        if noLocked:
            print(Fore.RED + f"{self.nome} - comendo")
            sleep(self.tempo_alimentacao)
            print(Fore.GREEN + f"{self.nome} - pensando")
            pratos[nomes.index(self.nome)] += 1  # quantas vezes cada filosofo comeu
            garfo1.release()  # libera o garfo 1
            garfo2.release()  # libera o garfo 2
            return 1
        else:
            garfo1.release()  # libera o primeiro garfo, evitando deadlock
            # print(f"\n{self.nome} não conseguiu comer")
            # print(Fore.YELLOW + f"{self.nome} - não comeu")
            return 0

nomes = ['Filósofo 1', 'Filósofo 2', 'Filósofo 3', 'Filósofo 4', 'Filósofo 5']
garfos = [Lock() for _ in range(5)]
timeToEat = [randint(1, 5) for _ in range(5)] 
timeToWait = [randint(25, 50) for _ in range(5)] 
mesa = [Filosofo(nomes[i], garfos[i % 5], garfos[(i + 1) % 5], timeToEat[i], timeToWait[i]) for i in range(5)]

for filosofo in mesa:
    filosofo.start()  
    sleep(1)