#!/usr/bin/env python2
# coding: utf-8

# In[ ]:


import numpy as np
import sys
from matplotlib import pyplot as plt


# ##### Use the files generated by lattice creation code, i.e. shape, neighborlist, and label of each site

# In[ ]:


posarr = []
shape = np.load(sys.argv[1]+'_shape.npy')
nlist = np.memmap(sys.argv[1]+'_neighbors.npy',mode='r',dtype=int,shape=(shape[0],shape[1]))
label = np.load(sys.argv[1]+'_label.npy',allow_pickle='True',mmap_mode='r')
ndiff = 1


# ##### If a zeolite lattice intersection site has a neighbor site in zeolite-gas interface, add it to the posarr array

# In[ ]:


i = 0
while i < nlist.shape[0]:
	if (label[nlist[i,0]-1]=='ZI'):
		flag = 0
		for j in nlist[i]:
			if (label[j-1]=='ZGI'):
				flag = 1
		if (flag == 1):
			posarr += [int(nlist[i,0])]
	i+=1


# In[ ]:


posarr = np.unique(np.asarray(posarr))


# In[ ]:


print "# of potential sites found = ",len(posarr)
del nlist
dist = np.load(sys.argv[1]+'_coordinates.npy',allow_pickle='True',mmap_mode='r')


# ##### Choose number of simulations you want run = nsim sites from the posarr array by random

# In[ ]:


np.random.shuffle(posarr)
nsim = len(posarr)
site = posarr.reshape(nsim,ndiff)
del posarr
dtraj_0 = np.zeros((nsim,ndiff,3))
dtraj_k = np.zeros((nsim,ndiff,3))


# ##### Decorate the hopping molecule on the selected sites by saving the starting position of kMCs as the position of these sites

# In[ ]:


for k in range(nsim):
	for j in range(ndiff):
		dtraj_0[k,j,:] = dist[:,site[k,j]-1]
		dtraj_k[k,j,:] = dist[:,site[k,j]-1]
del dist
for i in site:
	print i,label[i-1]


# ##### Save the 
# ##### 1. ID of initial site occupied by the molecule, 
# ##### 2. Coordinate position of this initial site which is at step = 0, 
# ##### 3. Coordinate position of the molecule at step = k

# In[ ]:


np.save('site_nsim',site)
np.save('dtraj_0_nsim',dtraj_0)
np.save('dtraj_k_nsim',dtraj_k)

