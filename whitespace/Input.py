import Program
A = " "
B = "\t"
C = "\n"
"""
   Input to the whitespace VM.
   For convenience, three input characters 
       A => space, B => tab, C => either of CR/LF

Numbers are binary sign-and-modulus (A=0, B=1, C=terminator)
Strings are sequences of binary characters, terminated by C.

We have:

* Stack instructions (Preceded by A)
     Push (Integer)    A
     Dup           CA
     Swap          CB
     Discard       CC

* Arithmetic (Preceded by BA)
     Plus          AA
     Minus         AB
     Times         AC
     Divide        BA
     Modulo        BB

* Heap access (Preceded by BB)
     Store         A
     Retrieve      B

* Control     (Preceded by C)
     Label String  AA
     Call Label    AB
     Jump Label    AC
     If Zero Label BA
     If Neg Label  BB
     Return        BC
     End           CC

* IO instructions (Preceded by BC)
     OutputChar    AA
     OutputNum     AB
     ReadChar      BA
     ReadNum       BB
"""

def load(fname):
	fp = open(fname,"r")
	src = fp.read()
	fp.close()
	execute(src)

def execute(src):
	prog = parse(src)
	if prog != None:
		#print repr(prog) # uncomment to dump the contents of the program to stdout
		Program.vm (prog)

# DFA for the opcode tree
# format: DFA[(state,letter)] = state or (opcodeclass, None|int|str) or "tokenlist for error msg"
DFA = {(0,A): 1, (0,B): 4, (0,C): 12,
       (1,A): (Program.Push, int), (1,B): 2, (1,C): 3,
       (2,A): (Program.Ref, int), (2,B): "[SP][TB][TB]", (2,C): (Program.Slide, int),
       (3,A): (Program.Dup, None), (3,B): (Program.Swap, None), (3,C): (Program.Discard, None),
       (4,A): 5, (4,B): 8, (4,C): 9,
       (5,A): 6, (5,B): 7, (5,C): "[TB][SP][LF]",
       (6,A): (Program.Plus, None), (6,B): (Program.Minus, None), (6,C): (Program.Times, None),
       (7,A): (Program.Divide, None), (7,B): (Program.Modulo, None), (7,C): "[TB][SP][TB][LF]",
       (8,A): (Program.Store, None), (8,B): (Program.Retrieve, None), (8,C): "[TB][TB][LF]",
       (9,A): 10, (9,B): 11, (9,C): "[TB][LF][LF]",
       (10,A): (Program.OutputChar, None), (10,B): (Program.OutputNum, None), (10,C): "[TB][LF][SP][LF]",
       (11,A): (Program.InputChar, None), (11,B): (Program.InputNum, None), (11,C): "[TB][LF][TB][LF]",
       (12,A): 13, (12,B): 14, (12,C): 15,
       (13,A): (Program.Label, str), (13,B): (Program.Call, str), (13,C): (Program.Jump, str),
       (14,A): (Program.JumpZero, str), (14,B): (Program.JumpNeg, str), (14,C): (Program.Return, None),
       (15,A): "[LF][LF][SP]", (15,B): (Program.Trace, None), (15,C): (Program.End, None)}

def parse(src):
	i = 0;
	prog = Program.Program();
	lines,lastnewline = 1,-1 # so can give error locations as line:char
	tokenstart = 0,1,1 # byte, line, char
	state = 0
	while i < len(src):
		while src[i] not in (A,B,C):
			i += 1
		if state == 0:
			tokenstart = (i,lines,i-lastnewline)
		if src[i] == "\n":
			lines += 1
			lastnewline = i
		next = DFA[(state,src[i])]
		action = type(next)
		if action is int: # next state in tree
			state = next
		elif action is tuple: # next opcode
			state = 0
			opcode,parameter = next
			if parameter is int:
				(x,i) = parseNumber(src, i+1)
				lines += 1 # parseNumber will end on a \n
				lastnewline = i
				prog.programdata.append(opcode(tokenstart, x))
			elif parameter is str:
				(x,i) = parseString(src, i+1)
				lines += 1
				lastnewline = i
				prog.programdata.append(opcode(tokenstart, x))
			else:
				prog.programdata.append(opcode(tokenstart))
		else: # invalid state
			print "Error parsing script: %s is not a valid command at byte 0x%X (line %d char %d)\n" % ((next,) + tokenstart)
			print "Program so far: ", repr(prog);
			return None
		i += 1
	# find all the labels
	for i in range(len(prog.programdata)):
		if prog.programdata[i].opcode == Program.Opcodes.Label:
			prog.labels[prog.programdata[i].label] = i;
	return prog;

def parseNumber(string, index):
	a = 0L;
	neg = None
	while neg == None:
		if string[index] == A:
			neg = False
		elif string[index] == B:
			neg = True
		elif string[index] == C:
			return (0,index)
		index += 1
	while string[index] != C:
		if string[index] == A:
			a <<= 1
		elif string[index] == B:
			a <<= 1
			a += 1
		index += 1
	if neg:
		return (-a,index)
	else:
		return (a,index)

# storing a string (only used for labels) as eg "100101001" or "\t  \t \t  \t" would take up a lot
# of pointless space, but storing it as a number like parseNumber would mean 001 and 0001 wouldn't
# be unique - so store as a tuple of length and value, so they'd be (3,1) and (4,1) and hence unique
def parseString(string, index):
	a = 0L;
	length = 0;
	while string[index] != '\n':
		if string[index] == " ":
			a <<= 1
			length += 1
		elif string[index] == "\t":
			a <<= 1
			a += 1
			length += 1
		index += 1
	return ((length,a),index)
