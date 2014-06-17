import operator
import math
a={"cake":3,"bad":1,"china":5}
b={"bag":2,"Japan":18,"usa":2}
c={"mn":1,"cat":1,"usa":9}
lis=[]
lis.append(["songyu",a]);lis.append(["zhangyuan",b]);lis.append(["shijian",c])

def construct_vector(result):
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
    for i in result:
        print i
def calculate_distance(a,b):
    #this will adopt the cosine algorithm
    vector_product=0
    a_mod=0;b_mod=0
    key_a=a[1].keys();key_a=key_a.sort()
    key_b=b[1].keys();key_b=key_b.sort()
    for k,v in a[1].items():
        vector_product+=float(a[1][k]*b[1][k])
        a_mod+=pow(a[1][k],2)
        b_mod+=pow(b[1][k],2)
    return vector_product/(math.sqrt(a_mod)*math.sqrt(b_mod))
#construct_vector(lis)