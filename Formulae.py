def wastage(utilisedCPU, utilisedMem, const=0.0001):
    '''
    Returns fractional value
    utilisedCPU = normalised utilisated CPU
    utilisedMem = normalised utilisated Memory
    const = correction factor
    '''
    utilisedCPU /= 100
    utilisedMem /= 100
    if(utilisedMem+utilisedCPU == 0):
        return(0)
    return((abs((1-utilisedCPU)-(1-utilisedMem)+const)/(utilisedCPU+utilisedMem)))


def powerConsumption(utilisation, powerMax=1, powerIdle=0):
    '''
    Returns fractional power consumption value
    utilisation = % CPU utilisation
    powerMax = max power server can consume
    powerIdle = server's power consumption at idle
    '''
    if(utilisation == 0):
        return(0)
    else:
        return((powerMax-powerIdle)*(utilisation/100) + powerIdle)


def totalWastage(Sol, VM):
    Server = []
    for i in range(len(VM)):
        Server.append([0, 0])
    for i in range(len(VM)):
        Server[Sol[i][1]][0] += VM[Sol[i][0]][0]
        Server[Sol[i][1]][1] += VM[Sol[i][0]][1]
    # total wastage
    tw = 0
    for i in range(len(Server)):
        tw += wastage(Server[i][0]/100, Server[i][1]/100)
    return(tw)


def totalPowerConsumption(Sol, VM):
    Server = []
    for i in range(len(VM)):
        Server.append([0, 0])
    for i in range(len(VM)):
        Server[Sol[i][1]][0] += VM[Sol[i][0]][0]
        Server[Sol[i][1]][1] += VM[Sol[i][0]][1]
    # power consumption
    tpc = 0
    for i in range(len(Server)):
        tpc += powerConsumption(Server[i][0])
    return(tpc)
