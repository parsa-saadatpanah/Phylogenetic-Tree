def compare(s1, s2):
	d = 0
	for i in range(len(s1)):
		if s1[i]==s2[i] or s1[i]=='?' or s2[i]=='?':
			continue
		d = d+1
	return d
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

count = len(name)

valid = [True for i in range(count)]

while count>1:
	best_i = -1
	best_j = -1
	NJD = [ [0 for i in range(len(name))] for j in range(len(name)) ]
	valids= [x for x in range(len(name)) if valid[x]]
	sm=[0 for i in range(len(name))]
	for i in valids:
		for j in valids:
			if j != i:
				sm[i]+=d[i][j]
	for i in valids:
		for j in valids:
			if j==i: 
				continue
			NJD[i][j] = d[i][j]
			sub = sm[i]+sm[j]-d[i][j]*2
			sub/= float(max(count-2,1))
			NJD[i][j] = NJD[i][j] - sub
			if best_i == -1 or NJD[i][j]<NJD[best_i][best_j]:
				best_i = i
				best_j = j
	bn=NJD[best_i][best_j]
	print ("F: ",NJD[best_i][best_j])
	b1=-1
	b2=-1
	b3=-1
	NJD = [ [ [0 for i in range(len(name))] for j in range(len(name)) ] for k in range(len(name))]

	for i in valids:
		for j in valids:
			for k in valids:
				if i==j or i==k or j==k:
					continue
				NJD[i][j][k] = (d[i][j]+d[j][k]+d[j][k])/3.
				sub = sm[i]+sm[j]+sm[k] - d[i][j]*2 - d[i][k]*2 - d[j][k]*2
				sub/= float(max(3./2*(count-3),1))
				NJD[i][j][k] = NJD[i][j][k] - sub
				if b1 == -1 or NJD[i][j][k]<NJD[b1][b2][b3]:
					b1 = i
					b2 = j
					b3 = k
	print ("S: ",NJD[b1][b2][b3])
	if count<=2 or bn < NJD[b1][b2][b3]:	
		valid[best_j] = False
		name[best_i] = '('+name[best_i]+','+name[best_j]+')'
		for k in range(len(name)):
			if not valid[k]:
				continue
			if k==best_i or k==best_j:
				continue
			d_new = d[best_i][k] + d[best_j][k] - d[best_i][best_j]
			d_new = float(d_new)/2.0
			d[best_i][k] = d_new
			d[k][best_i] = d_new
		count = count - 1
	else:
		valid[b2] = False
		valid[b3]= False
		name[b1] = '('+name[b1]+','+name[b2]+','+name[b3]+')'
		for k in valids:
			if k==b1 or k==b2 or k==b3:
				continue
			d_new = d[b1][k] + d[b2][k] + d[b3][k] - (d[b1][b2] + d[b1][b3] + d[b2][b3])/2.*3
			d_new = float(d_new)/3.0
			d[b1][k] = d_new
			d[k][b1] = d_new
		count = count - 2	

o = open('ConstructedTree', 'w')
for i in range(len(name)):
	if valid[i]:
		o.write(name[i]+'\n')






