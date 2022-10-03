from random import randint
from time import sleep
from threading import Thread, Lock
from colorama import Fore

class Filosofo(Thread):
    def __init__(self, id, garfo_esquerdo, garfo_direito):
        Thread.__init__(self)
        self.id = id
        self.nome = f"Filósofo {id}"
        self.tempo_alimentacao = randint(1,5) # Duração da refeição
        self.tempo_maximo_sem_comer = randint(25,50) # Tempo máximo permitido sem comer
        self.garfo_esquerdo = garfo_esquerdo       
        self.garfo_direito = garfo_direito
        self.pratos_consumidos = 0

    # Funcao principal
    def run(self):
        tempo_acumulado = 0
        while 1:
            tempo_aleatorio = randint(5, 15)
            print(Fore.GREEN + f"{self.nome} - pensando")
            sleep(tempo_aleatorio) 
            
            while not self.comer():
                tempo_acumulado += tempo_aleatorio

                if (tempo_acumulado + 5) > self.tempo_maximo_sem_comer:  
                    self.garfo_esquerdo.acquire(True)
                    self.garfo_direito.acquire(True)
                    print(Fore.RED + f"{self.nome} - comendo (starvation)")
                    sleep(self.tempo_alimentacao)
                    self.pratos_consumidos += 1
                    self.garfo_esquerdo.release()  # libera o garfo
                    self.garfo_direito.release()  # libera o garfo
                sleep(tempo_aleatorio)

            # Se conseguiu comer, OK
            # Se não conseguiu, tempo_acumulado é incrementado 
            tempo_acumulado = 0

            # Filosofo vai comer caso o tempo_acumulado extrapolar 
            # o tempo_maximo_sem_comer (solução do starvation)
            
                #print(Fore.GREEN + f"{self.nome} - pensando")

    # Tenta comer
    def comer(self):
        print(Fore.YELLOW + f"{self.nome} - esperando")
        garfo1, garfo2 = self.garfo_esquerdo, self.garfo_direito

        # Se os garfos estão ocupados, então nao consegue comer
        if (garfo1.locked() and garfo2.locked()): 
            return 0

        # Inverte a ordem dos garfos 
        elif garfo1.locked():
            garfo1, garfo2 = self.garfo_direito, self.garfo_esquerdo

        # Pega um garfo
        garfo1.acquire(True)

        # Tenta pegar outro garfo
        noLocked = garfo2.acquire(False)

        if noLocked:
            print(Fore.RED + f"{self.nome} - comendo")
            sleep(self.tempo_alimentacao)
            self.pratos_consumidos += 1
            garfo1.release()  # libera garfo 1
            garfo2.release()  # libera garfo 2
            print(Fore.GREEN + f"{self.nome} - pensando")
            return 1
        else:
            garfo1.release()  # libera o primeiro garfo (solução do deadlock)
            return 0

garfos = [Lock() for _ in range(5)]
mesa = [Filosofo(i+1, garfos[i%5], garfos[(i+1)%5]) for i in range(5)]

for filosofo in mesa:
    filosofo.start()  
    sleep(1)