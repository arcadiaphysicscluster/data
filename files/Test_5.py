from mpi4py import MPI

comm = MPI.COMM_WORLD
rank = comm.rank
size = comm.size
name = MPI.Get_processor_name()

shared = (rank + 1) * 7
newRank = (rank - 1) % size
comm.send(shared, dest = (rank + 1) % size)
data = comm.recv(source = newRank)

print name
print 'Rank', rank
print 'Received:', data, 'which came from rank', newRank