from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()
'''
def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq
'''
if rank == 0:
	data = np.arange(100)
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