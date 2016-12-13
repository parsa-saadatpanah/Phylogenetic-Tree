import sys
import re
def RemoveBrace(s):
	ans = ''
	i = 0
	while i<len(s):
		if s[i]!='{':
			ans = ans + s[i]
		else:
			ans = ans + s[i+1]
			i = i+3
		i = i+1
	return ans

def parse(s):
	if s[0]!='(':
		return []
	inside = []
	balance = 0
	start = 0
	for i in range(len(s)):
		if i==0:
			start = 1
			continue
		if i==len(s)-1 and s[i]=='\n':
			inside.append(s[start:i-1])
			continue
		if i==len(s)-1:
			inside.append(s[start:i])
			continue
		if s[i]==')' :
			balance = balance-1
		if s[i]=='(':
			balance = balance+1
		if s[i] ==',':
			if balance==0:
				inside.append(s[start:i])
				start = i+1

	return inside

class Node(object):

	def __init__(self, s, seq,length):
		self.name = s
		inside = parse(s)
		self.children = [Node(i, seq,length) for i in inside]
		self.score = [ [1 for i in range(4)] for i in range(length)]
		if len(self.children) == 0:
			sequence = seq[self.name]
			for i in range(length):
				if sequence[i] == 'A':
					self.score[i][0] = 0
				elif sequence[i] == 'T':
					self.score[i][1] = 0
				elif sequence[i] == 'C':
					self.score[i][2] = 0
				elif sequence[i] == 'G':
					self.score[i][3] = 0
				elif sequence[i] == '?':
					self.score[i][0] = 0
					self.score[i][1] = 0
					self.score[i][2] = 0
					self.score[i][3] = 0
		else:
			for i in range(length):
				for j in range(4):
					self.score[i][j] = 0
					for child in self.children:
						a = min([child.score[i][k] if k==j else child.score[i][k]+1 for k in range(4)])
						self.score[i][j] = self.score[i][j]+a

	def size(self):
		c = 1
		for child in self.children:
			c = c + child.size()
		return c



if __name__ == "__main__":
	seq = {}
	s = open('Alignment2', 'r')
	for line in s:
		seq[line.split()[0]] = RemoveBrace(line.split()[1])
		l=len(seq[line.split()[0]])

	if len(sys.argv) == 2:
		t= open(sys.argv[1],'r')
	else:
		t = open('RealTree', 'r')
	root = Node(t.readline(), seq,l)

	scores = [ min([root.score[i][j] for j in range(len(root.score[0]))]) for i in range(len(root.score))]
	print(sum(scores))

