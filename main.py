import FFD
import Pheromone
import ACO2


# getting VM input
n = int(input("Enter no of VMs: "))
print("Enter their CPU and memory utilizations respectively: ")
VM = []
for i in range(n):
    x = list(map(int, input().split()))
    VM.append(x)


Sol, HostUtilisation = FFD.FFD_Sol(VM)

print(Sol)
print(HostUtilisation)
print(Pheromone.initial(n, HostUtilisation))

# getting parameters input
inp = list(map(float, input(
    "Enter local pheromone evaporation rate, global pheromone evaporation rate, alpha, q0, No of ants and no of iterations:").split()))
evapL = inp[0]
evapG = inp[1]
alpha = inp[2]
q0 = inp[3]
NA = int(inp[4])
M = int(inp[5])
tau0 = Pheromone.initial(n, HostUtilisation)
print(evapL, evapG, alpha, tau0, q0, int(NA), int(M))


ParetoSet = ACO2.ACO(evapL, evapG, alpha, tau0, q0, NA, M, n, VM)

print(VM)
