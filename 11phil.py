from multiprocessing import Process, Manager
from multiprocessing import Condition, Lock
from multiprocessing import Value
from multiprocessing import current_process
import time, random

NPHIL = 8
            

class Table():
    
    def __init__(self, NPHIL, manager):
        self.NPHIL = NPHIL
        self.tenedores = manager
        self.mutex = Lock()
        self.camarero = Condition(self.mutex)
    
    
    def tenedores_libres(self,num):
        return (self.tenedores[num] == True and self.tenedores[(num + 1%(self.NPHIL))] == True)
    
    def wants_eat(self, num):
        self.camarero.acquire()
        while not(self.tenedores[num] and self.tenedores[(num+1)%(self.NPHIL)]):
            print ("Filosofo ",num, "espera...")      
            self.camarero.wait() 
        print (f"Filosofo {num} toma los tenedores {num} y {(num+1)%(self.NPHIL)}")
        self.tenedores[num] = False
        self.tenedores[(num +1)%(self.NPHIL)] = False
        print(self.tenedores)
        self.camarero.release()
        
    def wants_think(self, num):
        self.camarero.acquire()
        print(f"Filosofo {num} deja los tenedores {num} y {(num+1)%(self.NPHIL)}")
        self.tenedores[num] = True
        self.tenedores[(num+1)%(self.NPHIL)] = True
        print(self.tenedores)
        self.camarero.notify_all()
        self.camarero.release()
        
        
def delay(n=3):
     time.sleep(random.random()/n)

           
def philosopher_task(i, table):
    for n in range(NPHIL):
           print(f"Filosofo {i} esta pensando")
           print(f"Filosofo {i} quiere comer")
           table.wants_eat(i)
           print(f"Filosofo {i} esta comiendo por {n+1}º vez")
           table.wants_think(i)
           print(f"Filosofo {i} deja de comer y quiere pensar")


        




def main():
    manager = Manager()
    tenedores = manager.list()
    
    for i in range(NPHIL):
        tenedores.append(True)
    
    
    
    table=Table(NPHIL, tenedores)
    philosofers = []
    for i in range(NPHIL):
        philosofers.append(Process(target=philosopher_task, args=(i,table)))
     
    for i in range(NPHIL):
        philosofers[i].start()
    for i in range(NPHIL):
        philosofers[i].join()
        


 
if __name__ == "__main__":
    main()
              