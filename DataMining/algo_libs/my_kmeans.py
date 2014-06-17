import sys,random,math
class User:
    def __init__(self,name,coords,reference=None):
        self.name=name
        self.coords=coords
        self.n=len(coords)
        self.reference=reference

class Cluster:
    def __init__(self,users):
        if len(users)==0: raise Exception("zero dimesion exception happended!")
        self.users=users
        self.n=len(users[0].coords)
        for user in users:
            if user.n!=self.n:raise Exception("ILLEGAL: wrong dimensions")
        self.centroid=self.calculateCentroid()

    def calculateCentroid(self):
        centroid={}
        #this is another method hasn't been completed yet
        # for user in self.users:
        #     for k,v in user[1].items():
        #         if centroid.get(k,None)==None: centroid[k]=v
        #         else: centroid[k]+=v
      #  print self.users[0].coords
        for k,v in self.users[0].coords.items():
            sum=0
            for user in self.users:
                sum+=user.coords[k]
            centroid[k]=float(float(sum)/float(self.n))
        return User("centroid_user",centroid)

    def update(self,users):
        old_centroid=self.centroid
        self.users=users
        if len(users)==0: return
        self.centroid=self.calculateCentroid()
        return getDistance(old_centroid,self.centroid)

def getDistance(a,b):
    #this will adopt the cosine algorithm
    vector_product=0
    a_mod=0;b_mod=0
    key_a=a.coords.keys()
    key_b=b.coords.keys()
    key_a.sort()
    key_b.sort()
   # for k,v in a.coords.items():
    for k in key_a:
        vector_product+=float(a.coords[k]*b.coords[k])
        a_mod+=pow(a.coords[k],2)
        b_mod+=pow(b.coords[k],2)
    return vector_product/(math.sqrt(a_mod)*math.sqrt(b_mod))

def construct_vector(result):
    sample_hash={}
    for single_list in result:
        for k,v in single_list.coords.items():
            if sample_hash.get(k,None)==None:
                sample_hash[k]=1
    keys_list=sample_hash.keys()
    #rehandle the result set again
    for single_list in result:
        #find the difference between 2 lists
        diff=[i for i in keys_list if i not in single_list.coords]
        #make them all have the same dimension
        for d in diff:
            single_list.coords[d]=0
    return result
    # for i in result:
    #     print i.coords

def construct_vector_old(result):
    sample_hash={}
    for single_list in result:
        for k,v in single_list[1].items():
            if sample_hash.get(k,None)==None:
                sample_hash[k]=1
    keys_list=sample_hash.keys()
    #rehandle the result set again
    for single_list in result:
        #find the difference between 2 lists
        diff=[i for i in keys_list if i not in single_list[1]]
        #make them all have the same dimension
        for d in diff:
            single_list[1][d]=0
    return result

def kmeans(users,k,cutoff):
    initial=random.sample(users,k)
    clusters=[Cluster([u]) for u in initial]

    while True:
        lists=[[] for c in clusters]
        print lists
        for u in users:
            smallest_distance=getDistance(u,clusters[0].centroid)
            index=0
            for i in range(len(clusters[1:])):
                distance=getDistance(u,clusters[i+1].centroid)
                if distance<smallest_distance:
                    smallest_distance=distance
                    index=i+1
            lists[index].append(u)
        biggest_shift=0.0
        for i in range(len(clusters)):
            shift=clusters[i].update(lists[i])
            biggest_shift=max(shift,biggest_shift)
        if biggest_shift<cutoff:
            break
    return clusters

def main():
    k,cutoff=3,10
    a={"cake":3,"bad":1,"china":5}
    b={"bag":2,"Japan":18,"usa":2}
    c={"mn":1,"cat":1,"usa":9}
    d={"fuck":3,"ruby":18,"china":12}
    e={"letsgo":2,"template":8,"ecommerce":4}
    f={"ca":5,"saltlake":3,"chicago":7}
    lis=[]
    lis.append(["songyu",a])
    lis.append(["zhangyuan",b])
    lis.append(["shijian",c])
    lis.append(["zhangziyi",d])
    lis.append(["jackchen",e])
    lis.append(["kelly",f])
    lis=construct_vector_old(lis)
    users=[]
    for user in lis:
        u=User(user[0],user[1])
        users.append(u)
    clusters=kmeans(users,k,cutoff)

if __name__=="__main__":
    main()