import Formulae


def initial(n, HostUtilisation):
    '''
     n = number of VMs
     HostUtilisation = list of hosts such that HostUtiliztion[0] = CPU consumption, HostUtilization[1] = Mem consumption
    '''

    # Normalised Power Consumption
    npc = 0
    # powerMax is assumed to be 100%
    for i in range(len(HostUtilisation)):
        npc += Formulae.powerConsumption(HostUtilisation[i][0])/100

    # wastage
    w = 0
    for i in range(len(HostUtilisation)):
        w += Formulae.wastage(HostUtilisation[i]
                              [0]/100, HostUtilisation[i][1]/100)

    return(1/(n*(npc+w)))


def localUpdate(PheromoneMatrix, n, evapL, tau0):
    for y in range(n):
        for x in range(n):
            PheromoneMatrix[y, x] = (
                1-evapL)*PheromoneMatrix[y, x] + evapL*tau0
    return(PheromoneMatrix)


def globalUpdate(PheromoneMatrix, n, evapG, tau0, NA, currentIteration, age, serverList):
    npc = 0
    for i in range(len(serverList)):
        npc += Formulae.powerConsumption(serverList[i][0])

    w = 0
    for i in range(len(serverList)):
        w += Formulae.wastage(serverList[i][0], serverList[i][1])

    # calculating value of lambda
    adaptiveCoefficient = NA/(currentIteration-age+1)

    for i in range(n):
        for j in range(n):
            PheromoneMatrix[i, j] *= (1-evapG)
            PheromoneMatrix[i, j] += (evapG*adaptiveCoefficient)/(npc+w)

    return(PheromoneMatrix)
