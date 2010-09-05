
#! /usr/bin/python
#
"""LOLCODE to Python translator

A quick hack to translate LOLCODE to Python. OH NOES!
"""
__author__ = "David Basden "
__copyright__ = "GNU Public Licence v2.0"
__version__ = "0.2"

import re
import sys

class State(object):
	def __init__(self): self.level = 0
	def indent(self): return "\t"*self.level

class Keyword(object):
	format = ""
	match = None
	indent = True
	subparse = ()
	def __init__(self, match):
		self.match = match
		self.args = list( match.groups() )
	def on_match_start(self, state): pass
	def on_match_end(self, state): pass
	def on_recurse_start(self, state): pass
	def on_recurse_end(self, state): pass
	def render(self, state):
		if self.indent: out = state.indent()
		else: out = ""
		out += self.format % tuple(self.args)
		return out
	def __str__(self): return str(type(self))+str(self.args)

class Hai(Keyword):
	matchon = "HAI"
	format = "for __HAI in ('l0l',):\n"
	def on_match_end(self, state): state.level += 1
class KThxBye(Keyword):
	matchon = "KTHXBYE"
	format = "break\n"
class CanHas(Keyword):	# TODO: make this ! noop
	matchon = "CAN HAS (.+)\?"
	format = "# import %s\n"
class Visible(Keyword):
	matchon = "VISIBLE (.+)$"
	subparse = (0,)
	format = "print %s\n"
class Gimmeh(Keyword):
	matchon = "GIMMEH (.+)"
	format = "%s = raw_input()\n"
class IHasA(Keyword):
	matchon = "I HAS A (.+)"
	format = "%s = 0\n"
class ImInUrLoop(Keyword):
	matchon = "IM IN YR LOOP"
	format = "while True:\n"
	def on_match_end(self, state): state.level += 1
class ImOuttaUrLoop(Keyword):
	matchon = "IM OUTTA YR LOOP"
	format = "pass\n"
	def on_match_end(self, state): state.level -= 1
class BiggerThan(Keyword):
	matchon = """IZ (.+) BIGGER THAN (.+)\?(.+)$"""
	format = "if %s > %s:\n%s"
	subparse = (2,)
	def on_recurse_start(self, state): state.level += 1
	def on_recurse_end(self, state): state.level -= 1
class Up(Keyword):
	matchon = "UP (.+)!!(\d+)"
	format = "%s += %s\n"
class NN(Keyword):
	matchon = """^(.+?)\ N\ (.+)$"""
	subparse = (0,1)
	indent = False
	format = "%s + %s"
	
	
# This also defines precedence in descending order
keywords = (Hai,KThxBye,CanHas,Visible,Gimmeh,IHasA,ImInUrLoop,ImOuttaUrLoop,BiggerThan,Up,NN)

class LolLex(object):
	def __init__(self, keywords):
		self.keywords = keywords
		self.patternmap = [(re.compile(c.matchon,re.MULTILINE & re.DOTALL),c) for c in keywords] 
	def getkw(self,cs):
		for pattern,c in self.patternmap:
			m = pattern.match(cs.strip())
			if m != None: return c(m)
		return None
	def parse(self,cs):
		kw = self.getkw(cs)
		if kw == None: return kw
		for sp in kw.subparse:
			# Iff recursed keyword is empty, we should leave the input in place
			# because it probably contains a variable name -- Base case
			recursekw = self.parse(kw.args[sp])
			if recursekw != None: kw.args[sp]= recursekw
		return kw
class Lol2Py(object):
	def get_code_str(self, kws, s=None):
		out = ""
		if s == None: s = State()
		for kw in kws:
			if not isinstance(kw,Keyword): ## Leave non-keywords in-place
				out = out + str(kw)
				continue
			kw.on_match_start(s)
			for sp in kw.subparse: # recursive render - tres evil
				kw.on_recurse_start(s)
				token = self.get_code_str((kw.args[sp],), s=s)
				kw.args[sp] = token
				kw.on_recurse_end(s)
			out = out + kw.render(s)
			kw.on_match_end(s)
		return out

def usage():
	print >> sys.stderr, "%s < [-h|--help] | [-c|--show-code] | [-r|--run-code] > [filename]" % (sys.argv[0],)
	sys.exit()

if __name__ == "__main__":
	filename,runcode,showcode = None,False,False
	for arg in sys.argv[1:]:
		if arg == '-r' or arg == '--run': runcode = True
		elif arg == '-c' or arg == '--show-code': showcode = True
		elif filename != None or arg == '-h' or arg == '--help': usage()
		else: filename = arg
	if not (runcode or showcode): showcode = True
	if filename == None: codefile = sys.stdin
	else: codefile = open(filename,'r')

	ll = LolLex(keywords)
	kws,buf = [], ""
	while True:
		line = codefile.readline()
		if line == "": break
		buf = buf+" "+line.strip()
		kw = ll.parse(buf)
		if kw != None:
			kws.append(kw)
			buf = buf[kw.match.end()+1:]
		else:
			print "### DO NOT WANT!!! : [%s]" % (buf,)
			buf = ""
	l2p = Lol2Py()
	codez = l2p.get_code_str(kws)
	if showcode:
		if runcode: print "# Start lolpy code output"
		print codez
		if runcode: print "# End lolpy code output\n\n# RUNZ0RZ!"
	if runcode: exec codez in {}


