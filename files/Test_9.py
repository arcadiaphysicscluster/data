from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

if rank == 0:
	data_chunks = np.arange(100)
		
	print('we will be scattering:', data_chunks , 'into', size, 'chunks')
	
else:
	data_chunks = None

data_chunks = comm.scatter(data_chunks, root = 0)
print(name, 'original data:', data_chunks)


data_chunks = data_chunks + 1

data_chunks = comm.gather(data_chunks, root = 0)

if rank == 0:
	print('master collected:', data_chunks)