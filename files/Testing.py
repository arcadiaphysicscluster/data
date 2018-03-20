from mpi4py import MPI
from numpy import arange, errstate, seterr
from math import sin

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.size
name = MPI.Get_processor_name()

def f(x,t):
	return -x**3 + sin(t)

a = 1
b = 10
N = 1000
h = (b - a)/N
x = 0

if rank == 0:
	seterr(divide='ignore')
	with errstate(divide='ignore'):
		tpoints = arange(a,b,h)

	xpoints = []
	print 'Initial array:', tpoints

else:
	tpoints = None
	xpoints = None

print 'test', tpoints

tpoints = comm.scatter(tpoints, root = 0)
print 'Processor', name, 'has data:', tpoints, xpoints

for t in tpoints:
	xpoints.append(x)
	k1 = h*f(x,t)
	k2 = h*f(x + .5 * k1, t + .5 * h)
	x += k2

newTpoints = comm.gather(tpoints, root = 0)
newXpoints = comm.gather(xpoints, root = 0)

if rank == 0:
	print name, 'Tpoints:', newTpoints
	print name, 'Xpoints:', newXpoints

