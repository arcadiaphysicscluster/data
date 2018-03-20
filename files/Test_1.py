from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.rank

print "My name is: ", comm.rank


os.system("sudo apt-get install docker; curl -fsSL https://yum.dockerproject.org/gpg | sudo apt-")

