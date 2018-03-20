from mpi4py import MPI
import os

comm = MPI.COMM_WORLD
rank = comm.rank



if rank != 0:
	print "My name is: ", comm.rank
	os.system("curl -sSL https://get.docker.com | sh")
	
'''
sudo docker swarm leave; sudo docker swarm join --token SWMTKN-1-5sjbfzctsjmf0osxqwijks43xvly4resj3kslh7gs5kxnnu0ci-er6dbk8m3hyngoa4ny194vyd6 192.168.10.1:2377
'''

