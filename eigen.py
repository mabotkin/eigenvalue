import random
import time
import sys

E_MAX = 10
E_MIN = -10
BIG = 12

# currently only supports 2x2
def factors(n):
	if n == 0:
		return 0
	return list(reduce(list.__add__,([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0)))

def genMat(e1, e2):
	while True:
		trace = e1 + e2
		det = e1*e2
		a = random.randint(-BIG, BIG)
		d = trace-a
		tot = (a*d) - det
		neg = 1
		if tot < 0:
			neg = -1
			tot = abs(tot)
		f = factors(tot)
		b = random.choice(f)
		if b == 0:
			c = random.randint(E_MIN, E_MAX)
		else:
			c = tot/b
		if random.random() < 0.5:
			b *= neg
		else:
			c *= neg
		if abs(a) < BIG and abs(b) < BIG and abs(c) < BIG and abs(d) < BIG:
			break
	return [[a, b],[c, d]]

def printMat(mat):
	for i in mat:
		for j in i: 
			sys.stdout.write(str(j) + " ")
		sys.stdout.write("\n")

scores = []

print "Welcome to the Eigenvalue Game!"
while True:
	try:
		sys.stdout.write("Press Enter when ready.")
		ea = random.randint(E_MIN, E_MAX)
		eb = random.randint(E_MIN, E_MAX)
		mat = genMat(ea, eb)
		raw_input()
		printMat(mat)
		tic = time.time()
		while True:
			try:
				print "Answer:"
				ans = raw_input().split()
				if len(ans) != 2:
					print "Invalid Answer"
				a = int(ans[0])
				b = int(ans[1])
				if (a == ea and b == eb) or (a == eb and b ==  ea):
					break
				else:
					print "Wrong."
			except ValueError, IndexError:
				print "Input Error"
		print "Correct!"
		toc = time.time()
		print "Time Elapsed: " + str(toc-tic) + " seconds."
		scores.append(toc-tic)
	except KeyboardInterrupt:
		print "Number Correct: " + str(len(scores))
		if len(scores) != 0:
			print "Average Time: " + str(sum(scores)/float(len(scores))) + " seconds."
		sys.exit(0)
