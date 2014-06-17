from numpy import vstack,array
from scipy.cluster.vq import kmeans,whiten,vq
from scipy.cluster.vq import kmeans2,whiten
from pylab import plot,show
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
from Config import DB
import pymysql
import re
from ScrawlData import tf_idf
ruler={}
def construct_ruler_and_vectors(result,ruler):
    #first construct the ruler
    for tuple in result[0][1]:
        if ruler.get(tuple[0],None)==None: ruler[tuple[0]]=0
        else: ruler[tuple[0]]+=1
    ruler=sorted(ruler.items(),key=lambda e:e[0],reverse=False) #make sure that the hash is sorted again
    #then construct the vectors for kmeans to use it!
    vectors_list=[]
    points=[]
    for fans in result:
        tmp_list=[]
        for tuple in fans[1]:
            tmp_list.append(tuple[1])
        #vectors_list.append(tmp_list)
        points.append(Point(fans[0],tmp_list,fans[2]))
    return points

#v=construct_ruler_and_vectors(a,ruler)
#whitened=whiten(v)
#print kmeans2(whitened,3)

import sys, math, random

class Point:
    def __init__(self,fans_name,coords,actor_fullname=None, reference=None):
        self.coords = coords
        self.n = len(coords)
        self.reference = reference
        self.fans_name=fans_name
        self.ruler={}
        self.cluster_num=-1
        self.actor_fullname=actor_fullname
        self.keywords_that_to_be_stored_in_DB=""
    def __repr__(self):
        return str(self.fans_name)+"--"+str(self.coords)
    def back_list_to_origin_hash(self):
        index=0
        new_coords={}
        for k,v in self.ruler.items():
            if self.coords[index]!=0:
                new_coords[k]=self.coords[index]
                self.keywords_that_to_be_stored_in_DB+=str(k)+","
            index+=1
       # self.coords=new_coords

class Cluster:
    def __init__(self, points):
        if len(points) == 0: raise Exception("ILLEGAL: empty cluster")
        self.points = points
        self.n = points[0].n
        for p in points:
            if p.n != self.n: raise Exception("ILLEGAL: wrong dimensions")
        self.centroid = self.calculateCentroid()
    def __repr__(self):
        return str(self.points)
    def update(self, points):
        old_centroid = self.centroid
        self.points = points
        self.centroid = self.calculateCentroid()
        return getDistance(old_centroid, self.centroid)
    def calculateCentroid(self):
        reduce_coord = lambda i:reduce(lambda x,p : float(x) + float(p.coords[i]),self.points,0.0)
        # if len(self.points)==0:
        #     centroid_coords=[0.00001 for i in range()]
        centroid_coords = [reduce_coord(i)/len(self.points) for i in range(self.n)]
        return Point("centroid",centroid_coords)

def kmeans(points, k, cutoff):
    initial = random.sample(points, k)
    clusters = [Cluster([p]) for p in initial]
    while True:
        lists = [ [] for c in clusters]
        for p in points:
            smallest_distance = getDistance(p,clusters[0].centroid)
            index = 0
            for i in range(len(clusters[1:])):
                distance = getDistance(p, clusters[i+1].centroid)
                if distance < smallest_distance:
                    smallest_distance = distance
                    index = i+1
            lists[index].append(p)
        biggest_shift = 0.0
        for i in range(len(clusters)):
            shift = clusters[i].update(lists[i])
            biggest_shift = max(biggest_shift, shift)
        if biggest_shift < cutoff:
            break
    return clusters

def getDistance(a, b):
    if a.n != b.n: raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)

def getDistance_for_eval(a, b):
    if len(a) != len(b): raise Exception("ILLEGAL: non comparable points")
    ret = reduce(lambda x,y: x + pow((a.coords[y]-b.coords[y]), 2),range(a.n),0.0)
    return math.sqrt(ret)

def makeRandomPoint(n, lower, upper):
    return Point([random.uniform(lower, upper) for i in range(n)])


def insert_into_database(cluster_num,keywords,fan_fullname,actor_fullname):
    conn=DB.get_dbconn_obj()
    cursor=DB.get_dbcur(conn)
    sql="insert into mining_results (cluster_num,keywords,fan_fullname,actor_fullname) values ('"+str(cluster_num)+"','"+str(keywords)+"','"+str(fan_fullname)+"','"+str(actor_fullname)+"')"
    count=cursor.execute(sql)
    conn.commit()
    print sql

result=tf_idf.prepare_for_kmeans()
result=tf_idf.construct_vector_old(result) #all rows has the same vector features
num_points, k, cutoff = len(result[0][1]), 3, 0.5
points = construct_ruler_and_vectors(result,ruler)

clusters = kmeans(points, k, cutoff)
def write_file(text,fp):
    fp.write(str(text))
# def ICS(centroid_coords,coords):
#     print centroid_coords
#     print coords
#     if len(centroid_coords)!=len(coords):
#         return -1
#     else:
#         dot_mul=0
#         mod1=0;mod2=0
#         for index in range(len(centroid_coords)):
#             dot_mul+=(centroid_coords[index]*coords[index])
#             mod1+=math.pow(centroid_coords[index],2)
#             mod2+=math.pow(coords[index],2)
#         mod=math.sqrt(mod1)*math.sqrt(mod2)
#         cosine=float(dot_mul)/float(mod)
#         return cosine
sim_sum=0

fp=open("keq3.txt","a+")
row_tobe_writed=""
for i,c in enumerate(clusters):
    count=0
    tmp_count=0
    tmp_sim_sum=0

    for p in c.points:
        tmp_count+=1
        print " Cluster: ",i
        p.ruler=ruler
        p.cluster_num=i
        p.back_list_to_origin_hash()
       # val=getDistance_for_eval(c.centroid.coords,p.coords)
        val=getDistance(c.centroid,p)
        count+=1
        row_tobe_writed+="Cluster number: "+str(i)+"   "+p.keywords_that_to_be_stored_in_DB+"   "+p.fans_name+"   "+p.actor_fullname+"\n"
        if val==-1: continue
        else: tmp_sim_sum+=val
    row_tobe_writed+="\n"
    row_tobe_writed+="-------The total number for this cluster is:"+str(count)+"-------\n"
    sim_sum+=float(tmp_sim_sum)/float(tmp_count)
write_file(row_tobe_writed+"\n    ICS:",fp)
write_file(float(sim_sum)/float(k),fp)
print float(sim_sum)/float(k)


       # p.keywords_that_to_be_stored_in_DB=re.sub('\'',"\\'",p.keywords_that_to_be_stored_in_DB)
       # p.keywords_that_to_be_stored_in_DB=re.sub("\"",'\\"',p.keywords_that_to_be_stored_in_DB)
     #   print p.coords
     #    try:
     #        print p.centroid
     #        insert_into_database(p.cluster_num,p.keywords_that_to_be_stored_in_DB,p.fans_name,p.actor_fullname)
     #    except:
     #        continue

