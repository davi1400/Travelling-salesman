# -*- coding: utf-8 -*-
"""
Created on Mon Mar 8 17:46:17 2019

@author: vitor
"""
import numpy as np

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
            self.world[i].state=i
            
    def vec(self):
        aux=[]
        for i in range(self.len):
            aux.append=self.world[i].state
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
        
        new_pop=[]
        for i in range(len(indices)):
            aux_world=np.copy(self.population[indices[i]])
            change=np.arange(self.len)
            np.random.shuffle(change)
            aux_world.change(change[0],change[1])
            new_pop.append(aux_world)
        return new_pop
    
    def reproduction(self,p1,p2):
        child1=Problem(self.len)
        child2=Problem(self.len)
        
        cut=[int(self.len/3),2*int(self.len/3)]
        
        for i in range(cut[1]-cut[0]):
            child1.world[cut[0]+i].state=p1.world[cut[0]+i].state
            child2.world[cut[0]+i].state=p2.world[cut[0]+i].state
            
        i=cut[1]
        while(i!=cut[0]):
            j=i
            while(True):
                if(len(np.where(child1.vec()==p2.world[j].state)[0])==0):
                    child1.world[i].state=p2.world[j].state
                    break
                else:
                    j=(j+1)%self.len
            i=(i+1)%self.len
        
        i=cut[1]
        while(i!=cut[0]):
            j=i
            while(True):
                if(len(np.where(child2.vec()==p1.world[j].state)[0])==0):
                    child2.world[i].state=p1.world[j].state
                    break
                else:
                    j=(j+1)%self.len
            i=(i+1)%self.len                    
                
            
        return child1,child2
    
    def selection(self):
        pop_cost=[]
        for i in range(self.len_popu):
            pop_cost.append(self.population[i].cost())
        pop_cost=np.asanyarray(pop_cost)
        return np.copy(self.population[pop_cost.argsort[-int(0.1*self.len):]])
    
    def new_population(self):
        
        
        
        
        
        
        
        
        
        
        
        
        
        
            
        
            
        