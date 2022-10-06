from random import randint
from time import sleep
from threading import Thread, Lock
from colorama import Fore

class Filosofo(Thread):
    def __init__(self, id, garfo_esquerdo, garfo_direito):
        Thread.__init__(self)
        self.id = id
        self.nome = f"Filósofo {id}"
        self.tempo_alimentacao = randint(1,3) # Duração da refeição
        self.tempo_maximo_sem_comer = randint(13,25) # Tempo máximo permitido sem comer
        self.garfo_esquerdo = garfo_esquerdo       
        self.garfo_direito = garfo_direito
        self.pratos_consumidos = 0

    # Funcao principal
    def run(self):
        tempo_acumulado = 0
        while 1:
            tempo_aleatorio = randint(3, 8)
            print(Fore.GREEN + f"{self.nome} - pensando")
            sleep(tempo_aleatorio) 
            
            # Enquanto não conseguir comer, vai acumulando tempo sem comer
            while not self.comer():
                tempo_acumulado += tempo_aleatorio
                
                # Se passar muito tempo sem comer, come imediatamente
                if (tempo_acumulado + 3) > self.tempo_maximo_sem_comer:  
                    self.garfo_esquerdo.acquire(True)
                    self.garfo_direito.acquire(True)
                    print(Fore.RED + f"{self.nome} - comendo (starvation)")
                    sleep(self.tempo_alimentacao)
                    self.pratos_consumidos += 1
                    self.garfo_esquerdo.release()  # libera o garfo
                    self.garfo_direito.release()  # libera o garfo
                sleep(tempo_aleatorio)

            tempo_acumulado = 0

    # Tenta comer
    def comer(self):
        print(Fore.YELLOW + f"{self.nome} - esperando")
        garfo1, garfo2 = self.garfo_esquerdo, self.garfo_direito
        
        # Tenta pegar os dois garfos com delay (um garfo de cada vez);
        # Começa pelo lado em que há um garfo disponivel.
        if (not garfo1.locked()):
            lockedGarfo1 = not garfo1.acquire(True)
            sleep(0.5)
            lockedGarfo2 = not garfo2.acquire(True)

        elif (not garfo2.locked()): 
            lockedGarfo2 = not garfo2.acquire(True)
            sleep(0.5)
            lockedGarfo1 = not garfo1.acquire(True)

        # Garfos ocupados, não consegue comer
        else:
            return False 

        
        # Se conseguiu pegar os garfos, então come
        if (not lockedGarfo1 and not lockedGarfo2):
            print(Fore.RED + f"{self.nome} - comendo")
            sleep(self.tempo_alimentacao)
            self.pratos_consumidos += 1
            garfo1.release()  # libera garfo 1
            garfo2.release()  # libera garfo 2
            return True

        # Se não, devolve o garfo (solução do deadlock)
        elif (lockedGarfo1):
            garfo1.release()
            return False
        else:
            garfo2.release()
            return False

garfos = [Lock() for _ in range(5)]
mesa = [Filosofo(i+1, garfos[i], garfos[(i+1)%5]) for i in range(5)]

for filosofo in mesa:
    filosofo.start()  
    sleep(0.2)