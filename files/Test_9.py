from mpi4py import MPI
import numpy as np
from csv import reader
import time

startTime = time.time()

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

if rank == 0:
	data_chunks = np.arange(100,200) #number of nodes to perform operation on, so 10 nodes will get 10 operations
		
	print('we will be scattering:', data_chunks , 'into', size, 'chunks')
	
else:
	data_chunks = None

data_chunks = comm.scatter(data_chunks, root = 0)

#--------------------------------------------------------------------------------------------------------
bitPrice = []
data_chunks = data_chunks + 1

with open(r'/home/pi/cloud/data/files/allData.csv', newline = '', mode = 'r+') as csvFile:
    reader = reader(csvFile, delimiter = ',')
	
    for i in range(983):
        next(reader)
    for row in reader:
        bitPrice.append(row[1])
'''
#This shows the graph for the current market price of Bitcoin       
time = numpy.linspace(1, len(bitPrice), len(bitPrice))
plt.plot(time, bitPrice)
'''

#Since we are using the stochastic differential equation:  dS = −μS dt + σ dW_t
#we want to calculate μ and σ
def daily_return(bitPrice):
    returns = []
    for i in range(0, len(bitPrice) - 1):
        today = float(bitPrice[i+1])
        yesterday = float(bitPrice[i])
        daily_return = (today - yesterday) / today
        returns.append(daily_return)
    return returns

returns = daily_return(bitPrice)

mu = np.mean(returns) * (1310/4) #working days from 1/1/2011 to 3/30/2018
sigma = np.std(returns) * np.sqrt(1310/4) 

#print(mu, sigma)

#Brownian function describes the random motion of stock values

def Brownian(seed, N):
    np.random.seed(seed)
    dt = 1./N
    b = np.random.normal(0.,1.,int(N)) * np.sqrt(dt)
    W = np.cumsum(b)
    return W, b

def GBM(So, mu, sigma, W, T, N):
    t = np.linspace(0,1,N+1)
    S = []
    S.append(So)
    for i in range(1, int(N+1)):
        drift = mu - .5 * sigma**2
        diffusion = sigma * W[i-1]
        S_temp = float(So) * np.exp(drift + diffusion)
        S.append(S_temp)
    return S, t

seed = data_chunks
N = len(bitPrice) - 1
So = bitPrice[0]
W = Brownian(seed,N)[0]
T = 1


soln = GBM(So, mu, sigma, W, T, N)[0]
t = GBM(So, mu, sigma, W, T, N)[1]
#plt.plot(t, soln)

#print(len(bitPrice), len(soln))

sumation = 0

for i in range(len(bitPrice)):
    bitFloat = float(bitPrice[i])
    solnFloat = float(soln[i])
    sumation = sumation + (bitFloat - solnFloat)

#print(sumation)


data_chunks = abs(sumation)

#--------------------------------------------------------------------------------------------------------
data_chunks = comm.gather(data_chunks, root = 0)

if rank == 0:
    print('min value:', np.amin(data_chunks), 'with seed :', np.argmin(data_chunks) + 1)
    print('TIme it took:', time.time() - startTime, 'seconds')