from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

if rank == 0:
	data = [ x for x in range(size * 10)]
	chunks = [[] for _ in range(size)]
    for i, chunk in enumerate(data):
		chunks[ i % size].append(chunk)
		
	print 'we will be scattering:', data , 'into', size, 'chunks'
	
else:
	data = None
	data_chunks = None
	
data = comm.scatter(data_chunks, root = 0)
print 'rank', rank, 'has data:', data_chunks
for i in range(len(data_chunks)):
	data_chunks[i] = data_chunks[i] + 1

newData = comm.gather(data_chunks, root = 0)

if rank == 0:
	print 'master collected:', newData
