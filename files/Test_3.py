from mpi4py import MPI

comm = COMM.MPI_WORLD
rank = comm.rank
size = comm.size
 
print 'rank', rank
print 'size', size
print 9**(rank + 3)