from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

if rank == 0:
	data = [x for x in range(size * 10)]
	data_chunks = np.split(data,size)
		
	print('we will be scattering:', data , 'into', size, 'chunks')
	
else:
	data_chunks = None

comm.scatter(data_chunks, root = 0)
print(name, 'original data:', data_chunks)

if data_chunks:
	for i in range(len(data_chunks)):
		data_chunks[i] = data_chunks[i] + 1
		
print(name, 'altered data:', data_chunks)

comm.gather(data_chunks, root = 0)

if rank == 0:
	print('master collected:', data_chunks)