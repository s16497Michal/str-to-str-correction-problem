# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 16:21:04 2020

@author: michal
"""

import json
import string
import random
import time

def random_strings_genereator(length):
    letters = string.ascii_lowercase
    s1 = ''.join(random.choice(letters) for i in range(length))
    return s1
    
def write_strings_to_file():
    strings = random_strings_genereator(2, 2)
    data = {'S1': strings[0], 'S2': strings[1]}
    with open('jsons/problem.json', 'w') as outfile:
        json.dump(data, outfile)

def reading_problem_from_file():
    with open('jsons/problem.json') as problem_set:
        problem = json.load(problem_set)
        
    problem_list = [problem['S1'], problem['S2']]
    return problem_list

        
def goal(insert, update, delete):
   return map(lambda e:e+1, [insert, update, delete])


def brute_force(stringA, stringB, goal, lengthA, lengthB): 

    if lengthA == 0:
         return lengthB 
  
    if lengthB == 0:
        return lengthA 
  

    if stringA[lengthA-1]==stringB[lengthB-1]:
        return brute_force(stringA, stringB, goal, lengthA-1, lengthB-1)
  
     
    return min(goal(brute_force(stringA, stringB, goal, lengthA, lengthB-1),   #insercja
                   brute_force(stringA, stringB, goal, lengthA-1, lengthB),    #usuwanie 
                   brute_force(stringA, stringB, goal, lengthA-1, lengthB-1))) #zamiana  
    
    
def climbing(stringA, stringB): 
    
    tablica = [[0 for x in range(len(stringB) + 1)] for x in range(len(stringA) + 1)] 
  
    for i in range(len(stringA)+1): 
        for j in range(len(stringB)+1): 
            
            if i == 0:  
                tablica[i][j] = j  
     
            elif j == 0: 
                tablica[i][j] = i
            else:
                if stringA[i-1] != stringB[j-1]:
                    
                    tablica[i][j] = min(goal(tablica[i][j-1],  
                                   tablica[i-1][j],        
                                   tablica[i-1][j-1])) 
                else: tablica[i][j]=tablica[i-1][j-1] 
                                   
    return tablica[len(stringA)][len(stringB)]

lista_tabu=[] #lista punktow zakazanych
def tabu(stringA, stringBB): 
    
    tab = [[0 for x in range(len(stringB) + 1)] for x in range(len(stringA) + 1)] 
   
    for i in range(len(stringA)+1): 
        for j in range(len(stringB)+1):		
            if (i,j) not in lista_tabu:

             if i == 0:  
                tab[i][j] = j  
                 
             elif j == 0: 
                tab[i][j] = i
             else:
                if stringA[i-1] != stringBB[j-1]: 
                    tab[i][j] = min(goal(tab[i][j-1],  
                                         tab[i-1][j],        
                                         tab[i-1][j-1]))
                else: tab[i][j]=tab[i-1][j-1]  
                lista_tabu.append((i,j-1))
                lista_tabu.append((i-1,j))
                lista_tabu.append((i-1,j-1))
                lista_tabu.append((i,j))
    return tab[len(stringA)][len(stringB)]  


def G(T):
  return T-1

def sa(stringA, stringB, Tmin): 
   
 T=10000
 i = 0

 A=max(len(stringA),len(stringB))
 
 while T > Tmin:

  
   B=0
   new_stringA=stringA
   new_stringB=stringB
   while len(new_stringA) != 0 and len(new_stringB) !=0:
    
    if new_stringA[-1]!=new_stringB[-1]:
   
     s=random.randint(1,3)
     
     if s==1:
       new_stringB=new_stringB[:-1]

     elif s==2:
       new_stringA=new_stringA[:-1]
    
     elif s==3:
       new_stringA=new_stringA[:-1]
       new_stringB=new_stringB[:-1]
    
     B+=1

	
	    
    else: 
      new_stringA=new_stringA[:-1]
      new_stringB=new_stringB[:-1]     	
   newB=B
   if (len(new_stringA)==0 and len(new_stringB)!=0) or (len(new_stringB)==0 and len(new_stringA)!=0): newB+=1
     
   
   if A > newB: A = newB
	   
   elif random.uniform(0, 1) < 1/(i+1): A = B


   T = G(T)
   i = i+1

 return A    

#generujemy 2 randomowe ciągi znakow
stringA = random_strings_genereator(8)
stringB = random_strings_genereator(10)
    

print("stringA: " + stringA)
print("stringB: " + stringB)

start = time.time()
bruteforce_result = brute_force(stringA, stringB, goal, len(stringA), len(stringB))
end = time.time()
brutforce_time = (end - start)
print("metoda brutforce znalazła rozwiazanie = " + str(bruteforce_result))
print("czas wykonania metody brute force dla stringA o długosci " + str(len(stringA)) + " i stringB o długosci: " + str(len(stringB)) + ": " + str(brutforce_time)) 


start = time.time()
climbing_result = climbing(stringA, stringB)
end = time.time()
climbing_time = (end - start)
print("metoda wspinaczkowa znalazła rozwiazanie = " + str(climbing_result))
print("czas wykonania metody climbing dla stringA o długosci " + str(len(stringA)) + " i stringB o długosci: " + str(len(stringB)) + ": " + str(climbing_time)) 


start = time.time()
tabu_result = tabu(stringA, stringB)
end = time.time()
tabu_time = (end - start)
print("metoda tabu znalazła rozwiazanie = " + str(tabu_result))
print("czas wykonania metody tabu dla stringA o długosci " + str(len(stringA)) + " i stringB o długosci: " + str(len(stringB)) + ": " + str(tabu_time))

start = time.time()
sa_result = sa(stringA, stringB, 1)
end = time.time()
sa_time = (end - start)
print("metoda tabu znalazła rozwiazanie = " + str(sa_result))
print("czas wykonania metody tabu dla stringA o długosci " + str(len(stringA)) + " i stringB o długosci: " + str(len(stringB)) + ": " + str(sa_time))  