
# coding: utf-8

# In[1]:

get_ipython().magic(u'load ItembasedCF.py')


# In[ ]:



# In[10]:


"""
Created on Mon Dec  1 18:29:09 2014

@author: Divya
"""

import numpy as np
from copy import deepcopy

data=np.genfromtxt("full_training.txt",delimiter=' ',dtype=int)
#data=data[range(50000),:]

testdata=np.genfromtxt("test_5000.txt",delimiter=' ',dtype=int)
#testdata=testdata[range(5000),:]

item_adj_list=dict.fromkeys(data[:,1],None)


for i in item_adj_list.keys():
    item_adj_list[i]=[]

for i in range(data.shape[0]):
    item_adj_list[data[i][1]].append((data[i][0],data[i][2]))
    

    
user_adj_list=dict.fromkeys(data[:,0],None)

for i in user_adj_list.keys():
    user_adj_list[i]=[]

for i in range(data.shape[0]):
    user_adj_list[data[i][0]].append((data[i][1],data[i][2]))
    

item_averages=dict.fromkeys(data[:,1],0)

for i in item_averages.keys():
   item_averages[i]=np.average(list(zip(*item_adj_list[i]))[1])


# In[11]:

no_of_Test= testdata.shape[0]
item_adj_list_test=dict.fromkeys(testdata[0:no_of_Test,1],None)

for i in item_adj_list_test.keys():
   item_adj_list_test[i]=[]

for i in range(no_of_Test):
   item_adj_list_test[testdata[i][1]].append((testdata[i][0],testdata[i][2])) 

user_adj_list_test=dict.fromkeys(testdata[0:no_of_Test,0],None)

for i in user_adj_list_test.keys():
    user_adj_list_test[i]=[]

for i in range(no_of_Test):
    user_adj_list_test[testdata[i][0]].append((testdata[i][1],testdata[i][2]))    


# In[12]:

import math


def pearson_corr(i,j):
    if not(i in item_adj_list) or not(j in item_adj_list):  
        return -2
    commonusers=[]
    userini= list(zip(*item_adj_list[i]))[0]
    userinj= list(zip(*item_adj_list[j]))[0]
    for l in range(len(userini)):
        if(userini[l] in userinj):
            commonusers.append(userini[l])
    #print(commonusers)   
    useriratings=[]
    userjratings=[]
    cusers = len(commonusers)
    if (cusers == 0):
        return -2
    for l in range(len(commonusers)):
       useriratings.append(item_adj_list[i][userini.index(commonusers[l])][1]-user_averages[commonusers[l]])
       userjratings.append(item_adj_list[j][userinj.index(commonusers[l])][1]-user_averages[commonusers[l]])
    #print(useriratings)
    #print(userjratings)
    num=np.dot(useriratings,userjratings)
    deno1=np.sqrt(np.dot(useriratings,useriratings))
    deno2=np.sqrt(np.dot(userjratings,userjratings))
    deno = deno1*deno2 *(1+math.exp(-((cusers*1.0)/2)))
    if (deno !=0):
        #print( num*1.0/deno)
        return ( num*1.0/deno) 
    else:
        return -2
      


# In[13]:

def predictrating(user,item):
    itemrated=list(zip(*user_adj_list[user]))[0]
    ratings=list(zip(*user_adj_list[user]))[1]
    sumrating=0
    sumsim=0
    simitems=0
    for i in range(len(itemrated)):
        sim=pearson_corr(itemrated[i],item)
        if(sim>0):
            sumrating=sumrating+sim*(ratings[i]-item_averages[itemrated[i]])
            sumsim=sumsim+sim
            simitems=simitems+1
    if(simitems>5):
        return (item_averages[item]+(sumrating*1.0/sumsim))
    else:
        return -1
        

#print(predictrating(1,61))


# In[14]:

# RMSE calculation
numpreds=0
sumerr=0
for user in user_adj_list_test.keys():
    if (user_adj_list.has_key(user)):
        for j in range(len(user_adj_list_test[user])):
            item=user_adj_list_test[user][j][0]
            if item_adj_list.has_key(item):
                pr=predictrating(user,item)
                if(pr!=-1):
                    temp = (pr-user_adj_list_test[user][j][1])
                    sumerr=sumerr+(temp * temp)
                    numpreds=numpreds+1
            else:
                continue
    else:
        continue
        
            
RMSE=np.sqrt(sumerr/numpreds) 


print RMSE
print numpreds/7500.0


# In[9]:

numpreds/7500.0


# In[ ]:





# In[ ]:



