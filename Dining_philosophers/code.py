from random import randint
from time import sleep
from threading import Thread, Lock
from colorama import Fore

class Filosofo(Thread):
    def __init__(self, id, garfo_esquerdo, garfo_direito):
        Thread.__init__(self)
        self.id = id
        self.nome = f"Filósofo {id}"
        self.tempo_alimentacao = randint(2,3) # Duração da refeição
        self.tempo_maximo_sem_comer = randint(3,4) # Tempo máximo permitido sem comer
        self.garfo_esquerdo = garfo_esquerdo
        self.garfo_direito = garfo_direito

    # Funcao principal
    def run(self):
        breakLoopMessage = False
        tempo_acumulado = 0

        while 1:
            print(Fore.GREEN + f"{self.nome} - pensando")
            sleep(randint(5, 6))
            
            # Enquanto não conseguir comer, vai acumulando tempo
            # A cada segundo, uma nova tentativa de comer 
            while not self.comer(tempo_acumulado):
                tempo_acumulado += 1
                
                if not breakLoopMessage:
                    print(Fore.YELLOW + f"{self.nome} - Esperando")
                    breakLoopMessage = True
                
                sleep(1)

            breakLoopMessage = False
            tempo_acumulado = 0

    # Tenta comer, se conseguir então retorna True
    def comer(self, tempo_acumulado):
        garfo1, garfo2 = self.garfo_esquerdo, self.garfo_direito

        # Se passar muito tempo sem comer, come imediatamente (solução do starvation)
        if tempo_acumulado >= self.tempo_maximo_sem_comer:
            garfo1.acquire(True)
            garfo2.acquire(True)
            print(Fore.RED + f"{self.nome} - comendo (starvation)")
            sleep(self.tempo_alimentacao)
            garfo1.release()  # libera o garfo
            garfo2.release()  # libera o garfo
            return True

        # Tenta pegar os garfos (solução do deadlock)
        if not garfo1.locked():
            garfo1.acquire(False)
        else:
            return False

        if not garfo2.locked():
            garfo2.acquire(False)
        else:
            garfo1.release()
            return False

        # Se conseguiu pegar os garfos, então come
        print(Fore.RED + f"{self.nome} - comendo")
        sleep(self.tempo_alimentacao)
        garfo1.release()  # libera garfo 1
        garfo2.release()  # libera garfo 2
        return True

garfos = [Lock() for _ in range(5)]
mesa = [Filosofo(i+1, garfos[i], garfos[(i+1)%5]) for i in range(5)]

for filosofo in mesa:
    filosofo.start()
    sleep(0.2)