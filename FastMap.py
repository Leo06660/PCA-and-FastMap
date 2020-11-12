#!/usr/bin/env python
# coding: utf-8

# In[1]:


class FastMap():
    
    def __init__(self, fastmap_wordlist):
#         self.k = k
#         self.fastmap_data = fastmap_data
        self.fastmap_wordlist = fastmap_wordlist
#         self.coordinate_idx = -1
        self.output_k_coordinate = 0 #np.zeros((len(fastmap_wordlist),k))
        
    def find_farthest_obj(self, obj1_idx, fastmap_data):
        # The row related to obj1_idx
        obj1_distances = np.concatenate((fastmap_data[fastmap_data[:,0]==obj1_idx], 
                                         fastmap_data[fastmap_data[:,1]==obj1_idx]))
        # Find out Oa in the above rows with max distance
        max_dist_idx = np.argmax(obj1_distances[:,2])
        obj2 = list(obj1_distances[max_dist_idx][0:2])
        obj2.remove(obj1_idx)
        obj2_idx = int(obj2[0])
        return obj2_idx
    
    def find_farthest_pair(self, fastmap_wordlist, fastmap_data):
        Ob = random.sample(fastmap_wordlist,1)[0]
        Ob_idx = fastmap_wordlist.index(Ob)+1
        old_ob_idx = Ob_idx
        while 1:
            Oa_idx = self.find_farthest_obj(Ob_idx, fastmap_data)
            Ob_idx = self.find_farthest_obj(Oa_idx, fastmap_data)
            if old_ob_idx == Ob_idx:
                return Oa_idx, Ob_idx
            else:
                old_ob_idx = Ob_idx
                
    def distance_function(self, obj1_idx, obj2_idx, fastmap_data):
        idx = []
        idx.append(obj1_idx)
        idx.append(obj2_idx)
        idx.sort()
        for idx_objs in range(len(fastmap_data)):
            if fastmap_data[:,0][idx_objs]==idx[0] and fastmap_data[:,1][idx_objs]==idx[1]:
                d = fastmap_data[:,2][idx_objs]
                return d
            else:
                d = 0
        return d
    
    def result(self, k, fastmap_data, coordinate_idx):
        # Stopping criteria
        if k<=0:
            return self.output_k_coordinate
        else:
            coordinate_idx+=1
        # Find each farthest pair of fastmap_data
        Oa_idx, Ob_idx = self.find_farthest_pair(self.fastmap_wordlist, fastmap_data)
        # Calculate the coordinate for each iteration
        for obj_idx in range(1,len(self.fastmap_wordlist)+1):
            d_ai = self.distance_function(Oa_idx, obj_idx, fastmap_data)
            d_ab = self.distance_function(Oa_idx, Ob_idx, fastmap_data)
            d_ib = self.distance_function(Ob_idx, obj_idx, fastmap_data)
            x = (d_ai**2+d_ab**2-d_ib**2)/(2*d_ab)
            self.output_k_coordinate[obj_idx-1][coordinate_idx]=x
        # Create new distance function which is new fastmap data
        new_fastmap_data = fastmap_data.copy() 
        for row in range(len(new_fastmap_data)):
            D_old = self.distance_function(new_fastmap_data[row][0],
                                      new_fastmap_data[row][1], 
                                      fastmap_data)
            xi = self.output_k_coordinate[int(new_fastmap_data[row][0]-1)][coordinate_idx]
            xj = self.output_k_coordinate[int(new_fastmap_data[row][1]-1)][coordinate_idx]
            new_fastmap_data[row][2] = (D_old**2-(xi-xj)**2)**0.5
        # Call FastMap function again with the input of new fastmap 
        self.result(k-1, new_fastmap_data, coordinate_idx)
        return self.output_k_coordinate

