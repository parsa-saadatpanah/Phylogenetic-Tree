from copy import *
from TreeScore import Node
import math
import random
def compare(s1, s2):
	d = 0
	for i in range(len(s1)):
		if s1[i]==s2[i] or s1[i]=='?' or s2[i]=='?':
			continue
		d = d+1
	return d

def score(name):
	seq = {}
	s = open('Alignment', 'r')
	for line in s:
		seq[line.split()[0]] = line.split()[1] 

	root = Node(name, seq)
	scores = [ min([root.score[i][j] for j in range(len(root.score[0]))]) for i in range(len(root.score))]
	return sum(scores)

def doYourWork(isRandom,d,name,factor):
	count = len(name)
	valid = [True for i in range(count)]
	while count>1:
		all=[]
		valids= [x for x in range(len(name)) if valid[x]]
		sm=[0 for i in range(len(name))]
		for i in valids:
			for j in valids:
				if j != i:
					sm[i]+=d[i][j]
		for i in valids:
			for j in valids:
				if j<=i: 
					continue
				NJD = d[i][j]
				sub = sm[i]+sm[j]-d[i][j]*2
				sub/= float(max(count-2,1))
				NJD = NJD - sub
				all.append((i,j,NJD))
		all=sorted(all, key= lambda x:x[2])
		if len(all)<=1 or isRandom==False:
			best_i=all[0][0]
			best_j=all[0][1]
		else:
			diff=(all[1][2]-all[0][2])/factor
			p=math.exp(-diff)/2
			if random.random()<=p:
				best_i=all[1][0]
				best_j=all[1][1]
			else:
				best_i=all[0][0]
				best_j=all[0][1]			
		valid[best_j] = False
		name[best_i] = '('+name[best_i]+','+name[best_j]+')'
		for k in valids:
			if k==best_i or k==best_j:
				continue
			d_new = d[best_i][k] + d[best_j][k] - d[best_i][best_j]
			d_new = float(d_new)/2.0
			d[best_i][k] = d_new
			d[k][best_i] = d_new
		count = count - 1
	for i in range(len(name)):
		if valid[i]:
			s=score(name[i])
			return (name[i],s)

f = open('Alignment', 'r')
name = []
seq = []
for line in f:
	l = line.split()
	name.append(l[0])
	seq.append(l[1])

d = [[0 for i in range(len(name))] for j in range(len(name))]

for i in range(len(name)):
	for j in range(len(name)):
		d[i][j] = compare(seq[i], seq[j])
res=[]
res.append( doYourWork(False,deepcopy(d),deepcopy(name),1))
for i in range(100):
	res.append(doYourWork(True,deepcopy(d),deepcopy(name),1+i/10.))
#	print(res[-1][1])
res=sorted(res,key=lambda x: x[1])

o = open('ConstructedTree', 'w')
o.write(res[0][0]+'\n')
o.close()






