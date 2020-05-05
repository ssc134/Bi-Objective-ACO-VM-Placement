import numpy as np
import random
import Formulae
import Pheromone


def canFit(VMcpu_Util, VMmem_Util, ServerList, ServerPtr):
    '''
    VMcpu_Util = utilization of VM CPU
    VMmem_Util = utilization of VM Memeory
    ServerList = list [CPU_Utilization%, MemUtilization%, Server index]
    ServerPtr = Index of ServerList
    '''
    if VMcpu_Util <= ServerList[ServerPtr][0] and VMmem_Util <= ServerList[ServerPtr][1]:
        return(True)
    return(False)


def heuristic1(ServerList, ServerPtr, const=0.0001):
    # initialising normalised power consumption to 0
    ncp = 0
    for i in range(ServerPtr+1):
        ncp += Formulae.powerConsumption(ServerList[i][0])
    ncp /= 100
    return(1/(const+ncp))


def heuristic2(ServerList, ServerPtr, const=0.0001):
    # initialising wastage to 0
    w = 0
    for i in range(ServerPtr+1):
        w += Formulae.wastage(ServerList[i][0]/100, ServerList[i][1]/100)
    return(1/(const+w))


def heuristic(ServerList, ServerPtr):
    '''
    Returns combined heuristic (h1 + h2)
    '''
    return(heuristic1(ServerList, ServerPtr) + heuristic2(ServerList, ServerPtr))


def probability(ServerList, ServerPtr):
    '''
    returns probability of movement into the selected VM based on free resource available
    '''
    return(2-(ServerList[ServerPtr][0]+ServerList[ServerPtr][1])/100)


def ACO(evapL, evapG, alpha, tau0, q0, NA, M, n, VM):
    '''
    evapL = local evaporation rate
    evapG = global evaporation rate
    alpha = parameter that controls the weight between pheromone and heuristic
    tau0 = initial pheromone
    NA = number of ants
    M = number of iterations
    n = number of VMs
    VM = list of VMs. Each element is a list of 2 elements. VM[0] = CPU requirement, VM[1] = Mem requirement
    '''

    # assign indices to all VMs
    for i in range(len(VM)):
        VM[i].append(i)

    # creating an empty ParetoSet
    ParetoSet = []
    # Solution is a 2 element list [i, j] with i = VM index and j = Server index
    Sol = []
    # List of wastages of each Solution in ParetoSet
    Wastage = []
    # List of Power Consumptions in each ParetoSet
    PowerConsumption = []
    # Pheremone Matrix list for each Sol in ParetoSet
    PheromoneMatList = []
    # list containing a list of 2 elements donoting no of times/iterations a solution has existed in ParetoSet.
    SolAge = []

    # creating Pheromone and Heuristic matrices
    PheromoneMat = np.empty([n, n], dtype=float)
    Heuristic = np.empty([n, n], dtype=float)

    # initialising PheromoneMat matrix
    for i in range(n):
        for j in range(n):
            PheromoneMat[i, j] = tau0

    for i in range(int(M)):
        for j in range(NA):

            # creation of server list
            ServerList = []
            for k in range(n):
                # [0, 0, k] = 0% utilization of CPU, 0% utilization of Mem, k is the index of server
                x = [95, 95, k]
                ServerList.append(x)

            # randomising server list
            random.shuffle(ServerList)

            # creating a set of unplaced VMs to be used to placed them into servers
            # initially all VMs are unplaced
            UnplacedVMs = set()
            for k in range(n):
                UnplacedVMs.add(k)

            randomServerList = []
            for x in range(n):
                randomServerList.append(x)
            ServerPtr = 0
            while(len(UnplacedVMs) != 0):
                for k in range(len(VM)):
                    if(canFit(VM[k][0], VM[k][1], ServerList, ServerPtr)):
                        h = heuristic(ServerList, ServerPtr)
                        p = probability(ServerList, ServerPtr)
                        q = random.random()
                        if q <= q0:
                            # if q<=q0 use the selected server else choose a random server
                            Sol.append([VM[k][2], ServerPtr])
                            ServerList[ServerPtr][0] += VM[k][0]
                            ServerList[ServerPtr][1] += VM[k][1]
                        else:
                            # selection of a random server
                            randomServerList= []

                            lastIndex= n-1
                            randomServerPtr= random.randint(0, lastIndex)
                            Sol.append([VM[k][2], randomServerPtr])
                            while(canFit(VM[k][0], VM[k][1], ServerList, randomServerPtr) == False):
                                Sol.pop()
                                temp= randomServerList[randomServerPtr]
                                randomServerList[randomServerPtr]= randomServerList[lastIndex]
                                randomServerList[lastIndex]= temp
                                lastIndex -= 1
                                randomServerPtr= random.randint(0, lastIndex)
                                Sol.append(VM[k][2], randomServerPtr)

                    # applying local pheromone updating rule
                    PheromoneMat= Pheromone.localUpdate(PheromoneMat, n, evapL, tau0)

        # evaluation
        # print(Sol)
        # Calculating the objective function for each solution
        CurrentWastage= Formulae.totalWastage(Sol, VM)
        CurrentPowerConsumption= Formulae.totalPowerConsumption(Sol, VM)
        # comparing dominance of the solution with that of solutions in the ParetoSet
        # and adding dominated solution's index in the dominatedSolutions list
        dominatedSolutions= []
        for j in range(len(ParetoSet)):
            if((CurrentWastage < Wastage[j] and CurrentPowerConsumption <= PowerConsumption[j]) or (CurrentWastage <= Wastage[j] and CurrentPowerConsumption < PowerConsumption[j])):
                dominatedSolutions.append(j)
        # if the current Sol dominates atleast 1 solution in ParetoSet, add this sol to ParetoSet
        if(len(dominatedSolutions) > 0):
            ParetoSet.append(Sol)
            PheromoneMatList.append(PheromoneMat)
        # removing dominated solutions from ParetoSet in reverse order so that the list indexing doesn't get changed
        sorted(dominatedSolutions, reverse=True)
        for j in range(len(dominatedSolutions)):
            ParetoSet.pop(dominatedSolutions[j])
            Wastage.pop(dominatedSolutions[j])
            PowerConsumption.pop(dominatedSolutions[j])
            PheromoneMatList.pop(dominatedSolutions[j])

        # adding current Pheromone matrix to the Pheromone Matrix List
        PheromoneMatList.append(PheromoneMat)
        # global updation on Pheromone matrix
        for mat in PheromoneMatList:
            Pheromone.globalUpdate(mat, n, evapG, tau0, NA, i, i, ServerList)

    return(ParetoSet)
