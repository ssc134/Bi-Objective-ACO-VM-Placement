
def mean(l):
    sum = 0
    for i in range(len(l)-1):
        sum += l[i]
    return(sum/(len(l)-1))  # because index is also appended at the end


def FFD_Sol(VM, maxCpuLimit=95, MaxMemLimit=95):

    i = 0
    for vm in VM:
        vm.append(i)
        i += 1

    # reverse sorted VM list
    rVM = sorted(VM, key=mean, reverse=True)

    HostUtilization = []
    for i in range(len(VM)):
        HostUtilization.append([0, 0])

    # Sol is a list of list. Sol[i] has value [p,q]. It denotes VM p is assigned to host q.
    Sol = []

    # ptr points to hosts in list
    ptr = 0
    for i in range(len(rVM)):
        if(rVM[i][0] <= maxCpuLimit-HostUtilization[ptr][0] and rVM[i][1] <= MaxMemLimit-HostUtilization[ptr][1]):
            HostUtilization[ptr][0] += rVM[i][0]
            HostUtilization[ptr][1] += rVM[i][1]
            Sol.append([rVM[i][2], ptr])
        else:
            ptr += 1
            HostUtilization[ptr][0] -= rVM[i][0]
            HostUtilization[ptr][1] -= rVM[i][1]
            Sol.append([rVM[i][2], ptr])

    Sol.sort()
    return(Sol, HostUtilization)
