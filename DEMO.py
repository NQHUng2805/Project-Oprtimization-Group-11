from ortools.sat.python import cp_model
import random
def cvrp_model(N, K, M, r, c, d):
    model = cp_model.CpModel()
    B = [i for i in range(1, N+M + 2*K + 1)]
    vehicles = [i for i in range(1, K + 1)]
    F1 = [(i, k + M + N) for i in B for k in vehicles]
    F2 = [(k + M + K + N, i) for i in B for k in vehicles]
    F3 = [(i, i) for i in B]
    #F4 = [(N+m, i) for m in range(1, M+1) for i in range(1, N+1)]
    #F5 = [(k+N+M, N+m) for k in vehicles for m in range(1, M+1)]
    B2 = [(i, j) for i in B for j in B]
    A = list(set(B2) - set(F1) - set(F2) - set(F3))
    print(A)
    A_plus = dict()
    A_minus = dict()
    
    for e in A:
        A_plus[e[0]] = list()
        A_minus[e[1]] = list()
    for e in A:
        A_plus[e[0]].append(e[1])
        A_minus[e[1]].append(e[0])
    # print(A_plus)
    # print(A_minus)
    
    # define variables
    x = {}
    y = {}
    z = {}
    
    for k in vehicles:
        for i, j in A:
            x[k, i, j] = model.NewIntVar(0, 1, 'x[%d,%d,%d]' % (k, i, j))
            
    for k in vehicles:
        for i in B:
            y[k, i] =model.NewIntVar(0, sum(r), 'y[%d, %d]' % (k, i))
    for i in B:
        z[i] = model.NewIntVar(1, K, 'z[%d]' % i)
    
        
        
    # add constraints
    for i in range(1, N+M+1):
        model.Add(sum(x[k, i, j] for j in A_plus[i] for k in vehicles) == 1)
        model.Add(sum(x[k, j, i] for j in A_minus[i] for k in vehicles) == 1)
        
    for i in range(1, N+M+1):
        for k in vehicles:
            model.Add((sum(x[k, i, j] for j in A_plus[i]) - sum(x[k, j, i] for j in A_minus[i])) == 0)
            
    for k in vehicles:
        model.Add(sum(x[k,k+N+M,j] for j in range(1, N+M+1)) == 1)
        model.Add(sum(x[k,j,k+K+N+M] for j in range(1, N+M+1)) == 1)  
        
    E = 1000000
    
    for k in vehicles:
        for i, j in A:
            model.Add(E*(1-x[k, i, j])+z[i] >= z[j])
            model.Add(E*(1-x[k, i, j])+z[j] >= z[i])
            
            model.Add(E*(1-x[k, i, j])+y[k, j] >= y[k, i] + r[j])
            model.Add(E*(1-x[k, i, j])+y[k, i] + r[j] >= y[k, j])
                
    for k in vehicles:
        model.Add(y[k, k+K+M+N] <= c[k])
        model.Add(y[k, k+N+M] == 0)
        model.Add(z[k+M+N] == k)
        model.Add(z[k+K+M+N] == k)
    
    # a = [(z[7] - z[1]), (z[6]-z[1])]
    # model.AddMultiplicationEquality(0, a)
    model.Add(z[1] == z[5])
    model.Add(z[2] == z[6])
    
    
    # objective function
    obj = sum(x[k, i, j] * d[i-1][j-1] for (i,j) in A for k in vehicles)
    model.Minimize(obj)
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        print("Optimal Value:", int(solver.ObjectiveValue()))
        
    for k in vehicles:
        for i, j in A:
            if k == 1 and solver.Value(x[k, i, j]) == 1:
                print('x[%d, %d, %d]' % (k, i, j))
    for k in vehicles:
        for i, j in A:
            if k == 2 and solver.Value(x[k, i, j]) == 1:
                print('x[%d, %d, %d]' % (k, i, j))
    
    
    
N = 4
K = 2
M = 4 
I = 100000
r = [0, 4, 3, 2, 5, 0, 0, 0, 0, 0, 0, 0, 0]
c = [0, 10, 10]
d = [[0, 2, 1, 2, 3, 4, 2, 5, 3, 3, I, I],
     [2, 0, 4, 2 ,2, 6, 2, 5, 1, 1, I, I],
     [2 ,4, 0, 4, 0, 2, 2, 5, 1, 1, I, I],
     [4 ,3, 5, 0, 7, 0, 2, 5, 4, 4, I, I],
     [3 ,5, 3, 1, 0, 2, 2, 5, 1, 2, 3, 4],
     [1 ,6, 3, 1, 3, 0, 2, 5, 5, 6, 7, 6],
     [2 ,7, 3, 1, 5, 7, 0, 5, 1, 2, 3, 4],
     [5 ,8, 3, 1, 5, 7, 2, 0, 5, 4, 6, 5],
     [2 ,7, 3, 1, I, I, I, I, 0, 0, 0, 0],
     [2 ,7, 3, 1, I, I, I, I, 0, 0, 0, 0],
     [2 ,7, 3, 1, 5, 7, 2, 5, 0, 0, 0, 0],
     [2 ,7, 3, 1, 5, 7, 2, 5, 0, 0, 0, 0]]

def generate_data(N, K, M):
    d = [[0] * (N+M+2*K) for i in range((N+M+2*K))]
    for i in range(1, len(d)+1):
        for j in range(1, len(d)+1):
            if i == j:
                d[i-1][j-1] = 0
            elif i <= N and N+M+K+1 <=j <= N+M+K+K:
                d[i-1][j-1] = 1000000
            elif N+M+1 <= i <= N+M+K and N+1 <= j <= N+M:
                d[i-1][j-1] = 1000000
            elif N+M+1 <= i <= N+M+K and N+M+1 <= j <= N+M+K+K:
                d[i-1][j-1] = 0
            else:
                d[i-1][j-1] = random.randint(1, 9)
        
        c = [0] + [random.randint(1, 9) for _ in range(K)]
        r = [0] * (N+M+K+K)
        for i in range(1, N+1):
            r[i] = random.randint(1, 9)
    return d, c, r
    
generate_data(4, 2, 4)
    

cvrp_model(N, K, M, r, c, d)

            

        