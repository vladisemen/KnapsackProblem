import numpy as np
# Начальное население
def init(popsize,n):
    population=[]
    for i in range(popsize):
        pop=''
        for j in range(n):
            pop=pop+str(np.random.randint(0,2))
        population.append(pop)
    return population

# декодированного1
def decode1(x,n,w,c,W):
    s=[]# Сохранить коллекцию нижних индексов выбранного объекта
    g=0
    f=0
    for i in range(n):
        if (x[i] == '1'):
            if g+w[i] <= W:
                g = g+w[i]
                f = f+c[i]
                s.append(i)
            else:
                break
    return f,s

 #Фитнес-функция1
def fitnessfun1(population,n,w,c,W):
    value=[]
    ss=[]
    for i in range(len(population)):
        [f,s]= decode1(population[i],n,w,c,W)
        value.append(f)
        ss.append(s)
    return value,ss


    # декодированного2
def decode2(x,n,w,c):
    s=[]# Сохранить коллекцию нижних индексов выбранного объекта
    g=0
    f=0
    for i in range(n):
        if (x[i] == '1'):
            g = g+w[i]
            f = f+c[i]
            s.append(i)
    return g,f,s

 #Фитнес-функция2
def fitnessfun2(population,n,w,c,W,M):
    value=[]
    ss=[]
    for i in range(len(population)):
        [g,f,s]= decode2(population[i],n,w,c)
        if g>W:
            f = -M # наказание
        value.append(f)
        ss.append(s)
    minvalue=min(value)
    value=[(i-minvalue+1) for i in value]
    return value,ss


    # Выбор рулетки
def roulettewheel(population,value,pop_num):
    fitness_sum=[]
    value_sum=sum(value)
    fitness=[i/value_sum for i in value]
    for i in range(len(population)):##
        if i==0:
            fitness_sum.append(fitness[i])
        else:
            fitness_sum.append(fitness_sum[i-1]+fitness[i])
    population_new=[]
    for j in range(pop_num):###
        r=np.random.uniform(0,1)
        for i in range(len(fitness_sum)):###
            if i==0:
                if r>=0 and r<=fitness_sum[i]:
                    population_new.append(population[i])
            else:
                if r>=fitness_sum[i-1] and r<=fitness_sum[i]:
                    population_new.append(population[i])
    return population_new


    # Две точки пересечения
def crossover(population_new,pc,ncross):
    a=int(len(population_new)/2)
    parents_one=population_new[:a]
    parents_two=population_new[a:]
    np.random.shuffle(parents_one)
    np.random.shuffle(parents_two)
    offspring=[]
    for i in range(a):
        r=np.random.uniform(0,1)
        if r<=pc:
            point1=np.random.randint(0,(len(parents_one[i])-1))
            point2=np.random.randint(point1,len(parents_one[i]))
            off_one=parents_one[i][:point1]+parents_two[i][point1:point2]+parents_one[i][point2:]
            off_two=parents_two[i][:point1]+parents_one[i][point1:point2]+parents_two[i][point2:]
            ncross = ncross+1
        else:
            off_one=parents_one[i]
            off_two=parents_two[i]
        offspring.append(off_one)
        offspring.append(off_two)
    return offspring


    # Единственная точечная мутация1
def mutation1(offspring,pm,nmut):
    for i in range(len(offspring)):
        r=np.random.uniform(0,1)
        if r<=pm:
            point=np.random.randint(0,len(offspring[i]))
            if point==0:
                if offspring[i][point]=='1':
                    offspring[i]='0'+offspring[i][1:]
                else:
                    offspring[i]='1'+offspring[i][1:]
            else:
                if offspring[i][point]=='1':
                    offspring[i]=offspring[i][:(point-1)]+'0'+offspring[i][point:]
                else:
                    offspring[i]=offspring[i][:(point-1)]+'1'+offspring[i][point:]
            nmut = nmut+1
    return offspring


    # Единственная точечная мутация2
def mutation2(offspring,pm,nmut):
    for i in range(len(offspring)):
        for j in range(len(offspring[i])):
            r=np.random.uniform(0,1)
            if r<=pm:
                if j==0:
                    if offspring[i][j]=='1':
                        offspring[i]='0'+offspring[i][1:]
                    else:
                        offspring[i]='1'+offspring[i][1:]
                else:
                    if offspring[i][j]=='1':
                        offspring[i]=offspring[i][:(j-1)]+'0'+offspring[i][j:]
                    else:
                        offspring[i]=offspring[i][:(j-1)]+'1'+offspring[i][j:]
                nmut = nmut+1
    return offspring