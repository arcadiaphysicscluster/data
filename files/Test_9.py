from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

data_chunks = None
if rank == 0:
	data = np.arange(100)
	data_chunks = np.split(data,size)
		
	print('we will be scattering:', data , 'into', size, 'chunks')
	
recvbuf = np.empty(100, dtype='i')
comm.Scatter(data_chunks,recvbuf,root = 0)

print(name, 'original data:', data_chunks)

for i in range(len(data_chunks)):
	data_chunks[i] = data_chunks[i] + 1

comm.Gather(data_chunks,recvbuf,root = 0)

if rank == 0:
	print('master collected:', data_chunks)