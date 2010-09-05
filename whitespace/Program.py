import sys

class Program:
	def __init__(self):
		# static data
		self.programdata = []
		self.labels = {}
		# dynamic data
		self.stack = []
		self.heap = {}
		self.programcounter = 0
		self.pcstack = []
	def __str__(self):
		return "<Program, %d opcodes (incl %d labels) - at %d, %d stack length, %d call depth, %d heap size>" % (len(self.programdata), len(self.labels), self.programcounter, len(self.stack), len(self.pcstack), len(self.heap))
	def __repr__(self):
		return "%s\nProgram Data: %s\nLabels: %s\nData Stack: %s\nHeap: %s\nProgram counter: %d\nPC Stack: %s" % (str(self),self.programdata,self.labels,self.stack,self.heap,self.programcounter,self.pcstack)

class Opcodes: # the numbers themselves are meaningless - they just have to be unique
	# Axx - stack ops
	Push = 0            # AA num    - push num to stack
	Dup = 1             # ACA       - push copy of TOS (top of stack)
	Swap = 2            # ACB       - swap TOS and TOS-1
	Discard = 3         # ACC       - pop and discard TOS
	Ref = 4             # ABA num   - push copy of TOS-num
	Slide = 5           # ABC num   - pop and discard TOS-1 through TOS-num - keep TOS
	                    #           - equiv to "ACB ACC" num times

	# BAxx - math ops
	Plus = 6            # BAAA      - push TOS-1 + TOS
	Minus = 7           # BAAB      - push TOS-1 - TOS
	Times = 8           # BAAC      - push TOS-1 * TOS
	Divide = 9          # BABA      - push TOS-1 / TOS (floored)
	Modulo = 10         # BABB      - push TOS-1 % TOS

	# BBx - heap ops
	Store = 11          # BBA       - write TOS to address TOS-1
	Retrieve = 12       # BBB       - read from address TOS

	# Cxx - flow ops
	Label = 13          # CAA label - mark a label
	Call = 14           # CAB label - call a subroutine
	Jump = 15           # CAC label - jump to a label
	JumpZero = 16       # CBA label - jump if TOS is zero
	JumpNeg = 17        # CBB label - jump if TOS is <0
	Return = 18         # CBC       - return from subroutine
	Trace = 24          # CCB       - print core dump
	End = 19            # CCC       - stop executing program

	# BCxx - I/O ops
	OutputChar = 20     # BCAA      - output char from TOS
	OutputNum = 21      # BCAB      - output int from TOS
	InputChar = 22      # BCBA      - input char to address at TOS
	InputNum = 23       # BCBB      - input int to address at TOS

class Instruction:
	opcode = -1
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		raise "Hmm, calling a non-opcode? Strange tastes..."

class Push(Instruction):
	opcode = Opcodes.Push
	def __init__(self, codeloc, value):
		self.codeloc = codeloc
		self.value = value
	def __call__(self, program):
		program.stack.append(self.value)
	def __str__(self):
		return "<Push %d>" % self.value
	__repr__ = __str__
class Dup(Instruction):
	opcode = Opcodes.Dup
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			program.stack.append(program.stack[-1])
		except IndexError:
			print "Error: Dup in empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Dup>"
	__repr__ = __str__
class Swap(Instruction):
	opcode = Opcodes.Swap
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			program.stack[-1],program.stack[-2] = program.stack[-2],program.stack[-1]
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Swap in stack with only one element at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Swap in empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Swap>"
	__repr__ = __str__
class Discard(Instruction):
	opcode = Opcodes.Discard
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			program.stack.pop()
		except IndexError:
			print "Error: Discard from empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Discard>"
	__repr__ = __str__
class Ref(Instruction):
	opcode = Opcodes.Ref
	def __init__(self, codeloc, location):
		self.codeloc = codeloc
		self.location = -location - 1
	def __call__(self, program):
		try:
			program.stack.append(program.stack[self.location])
		except IndexError:
			print "Error: Ref value larger than stack size at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Ref %d>" % -self.location
	__repr__ = __str__
class Slide(Instruction):
	opcode = Opcodes.Slide
	def __init__(self, codeloc, quantity):
		self.codeloc = codeloc
		self.quantity = -quantity - 1
	def __call__(self, program):
		try:
			program.stack = program.stack[0:self.quantity] + [program.stack[-1]]
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Slide from empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Slide value larger than stack size at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Slide %d>" % (-self.quantity + 1)
	__repr__ = __str__

class Plus(Instruction):
	opcode = Opcodes.Plus
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			y = program.stack.pop()
			x = program.stack.pop()
			program.stack.append(x + y)
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Plus with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Plus with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Plus>"
	__repr__ = __str__
class Minus(Instruction):
	opcode = Opcodes.Minus
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			y = program.stack.pop()
			x = program.stack.pop()
			program.stack.append(x - y)
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Minus with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Minus with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Minus>"
	__repr__ = __str__
class Times(Instruction):
	opcode = Opcodes.Times
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			y = program.stack.pop()
			x = program.stack.pop()
			program.stack.append(x * y)
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Times with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Times with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Times>"
	__repr__ = __str__
class Divide(Instruction):
	opcode = Opcodes.Divide
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			y = program.stack.pop()
			x = program.stack.pop()
			program.stack.append(x / y)
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Divide with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Divide with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Divide>"
	__repr__ = __str__
class Modulo(Instruction):
	opcode = Opcodes.Modulo
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			y = program.stack.pop()
			x = program.stack.pop()
			program.stack.append(x % y)
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Modulo with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Modulo with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Modulo>"
	__repr__ = __str__

class Store(Instruction):
	opcode = Opcodes.Store
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			val = program.stack.pop()
			addr = program.stack.pop()
			program.heap[addr] = val
		except IndexError:
			if len(program.stack) == 0:
				print "Error: Store with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			else:
				print "Error: Store with only one stack entry at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Store>"
	__repr__ = __str__
class Retrieve(Instruction):
	opcode = Opcodes.Retrieve
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			addr = program.stack.pop()
			program.stack.append(program.heap[addr])
		except IndexError:
			print "Error: Retrieve with empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
		except KeyError:
			print "Error: Retrieve from an address not stored to yet at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Retrieve>"
	__repr__ = __str__

class Label(Instruction):
	opcode = Opcodes.Label
	def __init__(self, codeloc, label):
		self.codeloc = codeloc
		self.label = label
	def __call__(self, program):
		pass # a label is a no-op
	def __str__(self):
		return "<Label %s>" % repr(self.label)
	__repr__ = __str__
class Call(Instruction):
	opcode = Opcodes.Call
	def __init__(self, codeloc, label):
		self.codeloc = codeloc
		self.label = label
	def __call__(self, program):
		try:
			program.pcstack.append(program.programcounter)
			program.programcounter = program.labels[self.label]
		except KeyError:
			print "Error: Call to undefined label at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Call %s>" % repr(self.label)
	__repr__ = __str__
class Jump(Instruction):
	opcode = Opcodes.Jump
	def __init__(self, codeloc, label):
		self.codeloc = codeloc
		self.label = label
	def __call__(self, program):
		try:
			program.programcounter = program.labels[self.label]
		except KeyError:
			print "Error: Jump to undefined label at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Jump %s>" % repr(self.label)
	__repr__ = __str__
class JumpZero(Instruction):
	opcode = Opcodes.JumpZero
	def __init__(self, codeloc, label):
		self.codeloc = codeloc
		self.label = label
	def __call__(self, program):
		try:
			if program.stack.pop() == 0:
				program.programcounter = program.labels[self.label]
		except KeyError:
			print "Error: JumpZero to undefined label at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<JumpZero %s>" % repr(self.label)
	__repr__ = __str__
class JumpNeg(Instruction):
	opcode = Opcodes.JumpNeg
	def __init__(self, codeloc, label):
		self.codeloc = codeloc
		self.label = label
	def __call__(self, program):
		try:
			if program.stack.pop() < 0:
				program.programcounter = program.labels[self.label]
		except KeyError:
			print "Error: JumpNeg to undefined label at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<JumpNeg %s>" % repr(self.label)
	__repr__ = __str__
class Return(Instruction):
	opcode = Opcodes.Return
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			program.programcounter = program.pcstack.pop()
		except IndexError:
			print "Error: Return without Call at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<Return>"
	__repr__ = __str__
class End(Instruction):
	opcode = Opcodes.End
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		program.programcounter = None
	def __str__(self):
		return "<End>"
	__repr__ = __str__

class OutputChar(Instruction):
	opcode = Opcodes.OutputChar
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			sys.stdout.write(chr(program.stack.pop()))
		except ValueError:
			print "Error: OutputChar value not in range 0-255 at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
		except IndexError:
			print "Error: OutputChar on empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<OutputChar>"
	__repr__ = __str__
class OutputNum(Instruction):
	opcode = Opcodes.OutputNum
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			sys.stdout.write(str(program.stack.pop()))
		except IndexError:
			print "Error: OutputNum on empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<OutputNum>"
	__repr__ = __str__
class InputChar(Instruction):
	opcode = Opcodes.InputChar
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			a = sys.stdin.read(1)
			if (a == ''):
				program.heap[program.stack.pop()] = -1
			else:
				program.heap[program.stack.pop()] = ord(a)
		except IndexError:
			print "Error: InputChar on empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<InputChar>"
	__repr__ = __str__
class InputNum(Instruction):
	opcode = Opcodes.InputNum
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		try:
			program.heap[program.stack.pop()] = int(sys.stdin.readline())
		except IndexError:
			print "Error: InputNum on empty stack at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
		except ValueError:
			print "Error: Entered value not a number for InputNum at byte 0x%X (line %d char %d)" % self.codeloc
			program.programcounter = None
	def __str__(self):
		return "<InputNum>"
	__repr__ = __str__
class Trace(Instruction):
	opcode = Opcodes.Trace
	def __init__(self, codeloc):
		self.codeloc = codeloc
	def __call__(self, program):
		print repr(program)
	def __str__(self):
		return "<Trace>"
	__repr__ = __str__

def vm(prog):
	while prog.programcounter >= 0:
		a = prog.programdata[prog.programcounter]
		prog.programcounter += 1
		#sys.stdout.write(str(a)) # uncomment to perform trace
		a(prog)
