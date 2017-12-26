
import random

def rand():
    return random.randint(0,20)

def get_initial_population(size=7):
    l=[rand() for i in range(size)]
    return l

def get_fitness(l):
    ret=[(-1*(i-10)**2) for i in l]
    return ret

def get_bin(l):
    ret=[bin(i)[2:] for i in l]
    ret=[(5-len(i))*'0'+i for i in ret]
    return ret

def get_dec(s):
    n=len(s)
    sm=0
    for i in range(n):
        sm+=int(s[i])
        sm=sm*2
    return sm//2

def get_dec_list(l):
    ret=[get_dec(i) for i in l]
    return ret

def apply_selection_operator(population,fitness,binary):
    l=[i for i in fitness]
    l.sort(reverse=True)
    n=len(fitness)
    idx=3*n//4
    val=l[idx]
    p=[]
    f=[]
    b=[]
    for i in range(n):
        if(fitness[i]>=val):
            p.append(population[i])
            f.append(fitness[i])
            b.append(binary[i])
    return(p,f,b)

def perform_crossover(s1,s2):
    n=len(s1)
    assert(n==5)
    assert(len(s2)==5)
    crossover_point=random.randint(1,n-1)
    ret=s1[0:crossover_point]+s2[crossover_point:]
    assert(len(ret)==5)
    return ret

def apply_crossover_operator(population,fitness,binary,num_crossovers):
    l=[]
    n=len(population)
    for i in range(num_crossovers):
        #print("n-1 =",n-1)
        z=[population[random.randint(0,n-1)],population[random.randint(0,n-1)]]
        z=get_bin(z)
        l.append(z)
    offsprings_bin=[perform_crossover(i[0],i[1]) for i in l]
    offsprings_dec=get_dec_list(offsprings_bin)
    for i in offsprings_dec:
        assert(i<32)
    offsprings_fitness=get_fitness(offsprings_dec)
    population+=offsprings_dec
    fitness+=offsprings_fitness
    binary+=offsprings_bin
    return (population,fitness,binary)

def apply_mutation_operator(population,fitness,binary):
    if(random.random()>0.4):
        idx=random.randint(0,len(population)-1)
        bit=random.randint(0,len(binary[0])-1)
        binary[idx]=binary[idx][0:bit]+str(random.randint(0,1))+binary[idx][bit+1:]
        population[idx]=get_dec(binary[idx])
        fitness=get_fitness(population)
    return (population,fitness,binary)

def avg(l):
    return sum(l)/len(l)

def hash1(l):
    h=[0]*33
    for i in l:
        h[i]+=1
    return h

# Find argmin (x-10)**2, 0<=x<=20

num_gens=20
ans=[]
mx=-10**100
population = get_initial_population(size=100000)
for i in range(num_gens):
    n=len(population)
    #random.shuffle(population)
    fitness=get_fitness(population)
    avg_fitness=avg(fitness)
    binary=get_bin(population)
    if(mx<avg_fitness):
        mx=avg_fitness
        ans=[j for j in population]
    population,fitness,binary=apply_selection_operator(population,fitness,binary)
    num_crossovers=n-len(population)
    population,fitness,binary=apply_crossover_operator(population,fitness,binary,num_crossovers)
    #print("generation = "+str(i+1)+" avg_fitness = "+str(avg_fitness)+" n = "+str(n)+" population =",population)
    print("generation = "+str(i+1)+" avg_fitness = "+str(avg_fitness)+" n = "+str(n))
    assert(len(binary[0])==5 and max(population)<=32)
    population,fitness,binary=apply_mutation_operator(population,fitness,binary)
print("###########################")
print("Max fitness =",mx)
#print("Fittest Population =",ans)
