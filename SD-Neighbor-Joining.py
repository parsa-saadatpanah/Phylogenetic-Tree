import re
def compare(s1, s2):
	d = 0
	for i in range(len(s1)):
		if s1[i]==s2[i] or s1[i]=='?' or s2[i]=='?':
			continue
		d = d+1
	return d
f = open('Alignment2', 'r')
name = []
seq = []
for line in f:
	l = line.split()
	name.append(l[0])
	seq.append(re.sub('\\{[^\\}]*\\}',
			'?',l[1]))

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
	ssm=sum(sm)
	for i in valids:
		for j in valids:
			if j==i: 
				continue
			NJD[i][j] = d[i][j]
			sub = sm[i]+sm[j]-d[i][j]*2
			sub/= float(max(count-2,1))
			NJD[i][j] = NJD[i][j] - sub
			add=ssm-2*sm[i]-2*sm[j]+2*d[i][j]
			add/=float(max((count-2)*(count-3),1))
			NJD[i][j]+=add
			if best_i == -1 or NJD[i][j]<NJD[best_i][best_j]:
				best_i = i
				best_j = j
	NJD[best_i][best_j]	
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

o = open('ConstructedTree', 'w')
for i in range(len(name)):
	if valid[i]:
		o.write(name[i]+'\n')






