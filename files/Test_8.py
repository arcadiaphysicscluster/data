from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

if rank == 0:
	data = [ (x + 1)** x for x in range(size)]
	print('we will be scattering:', data)
	
else:
	data = None
	
data = comm.scatter(data, root = 0)
print('rank', rank, 'has data:', data)

for i in range(len(data)):
		data[i] = data[i] + 1
		
data = comm.gather(data, root = 0)
print('master collected', data)
