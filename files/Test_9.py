from mpi4py import MPI
import numpy as np

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

def split_seq(seq, size):
        newseq = []
        splitsize = 1.0/size*len(seq)
        for i in range(size):
                newseq.append(seq[int(round(i*splitsize)):int(round((i+1)*splitsize))])
        return newseq

if rank == 0:
	data = [ x for x in range(size * 10)]
	data_chunks = split_seq(data,size)
		
	print 'we will be scattering:', data , 'into', size, 'chunks'
	
else:
	data = None
	data_chunks = None
	
recvbuf = [100]
data = comm.Scatter(data_chunks, recvbuf, dtype='i')

print 'rank', rank, 'has data:', data_chunks

for i in range(len(data_chunks)):
	data_chunks[i] = data_chunks[i] + 1

newData = comm.Gather(data_chunks, recvbuf, dtype='i')

if rank == 0:
	print 'master collected:', newData