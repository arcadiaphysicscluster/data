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
#	data_chunks = split_seq(data,size)
		
	print 'we will be scattering:', data , 'into', size, 'chunks'
	
else:
	data = None
#	data_chunks = None

recvbuf = np.empty(100, dtype='i')
comm.Scatter(data, recvbuf, root = 0)

print 'rank', rank, 'has data:', data

for i in range(len(data_chunks)):
	data[i] = data[i] + 1

comm.Gather(data, recvbuf, root = 0)

if rank == 0:
	print 'master collected:', data