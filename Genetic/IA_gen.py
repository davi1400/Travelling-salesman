# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 17:46:17 2019

@author: vitor
"""
import numpy as np
import time


class Node(object):


    def __init__(self, state):
        self.state=state
        self.go= None
        self.come =None
        
    def cost(self):
        return abs(self.state-self.go.state)

class Problem(object):
    
    def __init__(self, length):
        self.len=length
        self.world=[]
        for i in range(length):
            aux=Node(i)
            if(i>0):
                aux.come=self.world[i-1]
                self.world.append(aux)
                self.world[i-1].go=self.world[i]
            else:
                self.world.append(aux)
        
        self.world[length-1].go=self.world[0]  
        self.world[0].come=self.world[length-1] 
    
    def change(self,first,second):
        aux=self.world[first].state
        self.world[first].state=self.world[second].state
        self.world[second].state=aux
        
    def shuffle(self):
        aux=np.arange(self.len)
        np.random.shuffle(aux)
        for i in range(self.len):
            self.world[i].state=aux[i]
            
    def vec(self):
        aux=[]
        for i in range(self.len):
            aux.append(self.world[i].state)
        return aux
    
    def cost(self):
        aux=self.world[0]
        c=0
        for i in range(self.len):
            c=c+aux.cost()
            aux=aux.go
        return c
        
      
class Genetic():
    def __init__(self, length,population):
        self.len_popu=population
        self.population=[]
        self.len=length
        for i in range(population):
            aux=Problem(length)
            aux.shuffle()
            self.population.append(aux)
    
    def mutation(self,indices):
        aux=np.arange(self.len_popu)
        np.random.shuffle(aux)
        print("Mutação")
        new_pop=[]
        for i in range(int(0.1*self.len_popu)):
            aux_world=self.population[indices[i]]
            chang=np.arange(self.len)
            np.random.shuffle(chang)
            aux_world.change(chang[0],chang[1])
            new_pop.append(aux_world)
        return new_pop
    
    def reproduction(self,p1,p2):

        child1=Problem(self.len)
        child2=Problem(self.len)
        for i in range(self.len):
            child1.world[i].state=self.len+1
            child2.world[i].state=self.len+1
        
        cut=[int(self.len/3),int(2*self.len/3)]
        
        for i in range(cut[1]-cut[0]):
            child1.world[cut[0]+i].state=p1.world[cut[0]+i].state
            child2.world[cut[0]+i].state=p2.world[cut[0]+i].state
            
        i=cut[1]
        while(i!=cut[0]):
            j=i

            while(True):
#                print(j)
#                print(p2.world[j].state)
                if(np.shape(np.where(np.asanyarray(child1.vec())==p2.world[j].state)[0])[0]==0):
                    child1.world[i].state=p2.world[j].state
                    break
                else:
                    j=(j+1)%self.len
            i=(i+1)%self.len
        
        i=cut[1]
        while(i!=cut[0]):
            j=i
            while(True):
                if(np.shape(np.where(np.asanyarray(child2.vec())==p1.world[j].state)[0])[0]==0):
                    child2.world[i].state=p1.world[j].state
                    break
                else:
                    j=(j+1)%self.len
            i=(i+1)%self.len                    
                
            
        return child1,child2
    
    def selection(self):
        print("Seleção")

        pop_cost=[]
        for i in range(self.len_popu):
            pop_cost=np.append(pop_cost,self.population[i].cost())
    

        ind=np.asanyarray(pop_cost).argsort()[:int(0.1*self.len_popu)]

        new_pop=[]
        for i in range(int(0.1*self.len_popu)):
            new_pop=np.append(new_pop,self.population[ind[i]])
        return new_pop, ind
    
    def new_population(self):
        newpop, ind= self.selection()
        indices=np.arange(self.len_popu)
        indices=np.delete(indices,ind)
        
        np.random.shuffle(indices)
        
        newpop=np.append(newpop,self.mutation(indices[:int(0.1*self.len_popu)]))
        indices=indices[(int(0.1*self.len_popu)):]
        
        for i in range(0,(np.shape(indices)[0]-1),2):
            newpop=np.append(newpop,self.reproduction(self.population[indices[i]],self.population[indices[i+1]]))
        print("Reprodução")
        return newpop
    
    def solve(self):
        for i in range(100):
            self.population=self.new_population()
            self.len_popu=np.shape(self.population)[0]
            print(i)

        best, ind=self.selection()
        
        return best

t=[]
b=[]
for i in range(10):   
    avg_time = time.time()    
    test= Genetic(10,100)
    best=test.solve()
    avg_time=time.time()-avg_time
    t.append(avg_time)
    b.append(best[0])
        
                
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
            
        