"""
Original software copyright 2010 Mark Holmquist and Logan May.

Some recent modifications copyright 2012 Mark Holmquist.

This file is part of redlandside.

redlandside is licensed under the GNU GPLv3 or later, please see the
COPYING file in this directory or http://www.gnu.org/licenses/gpl-3.0.html for
more information.
"""

from PyQt4 import QtGui, QtCore

def format(color, style='', bgcolor=''):
	"""Return a QTextCharFormat with the given attributes.
	"""
	_color = QtGui.QColor()
	_color.setNamedColor(color)
	_format = QtGui.QTextCharFormat()
	_format.setForeground(_color)
	if 'bold' in style:
		_format.setFontWeight(QtGui.QFont.Bold)
	if 'italic' in style:
		_format.setFontItalic(True)
	if bgcolor != '':
		_color.setNamedColor(bgcolor)
		_format.setBackground(_color)

	return _format

class SyntaxHighlighter (QtGui.QSyntaxHighlighter):

	def __init__(self, fileobj):
		QtGui.QSyntaxHighlighter.__init__(self, fileobj.parent.textedit.document())

		self.styles = {
			'keyword': format('red'),
			'preproc': format('green'),
			'brace': format('darkBlue'),
			'defclass': format('black', 'bold'),
			'literal': format('magenta'),
			'comment': format('darkGreen', 'italic'),
			'wsspace': format('black', bgcolor='blue'),
			'wstab': format('black', bgcolor='red')
		}
		self.rules = []
		rules = []


# C++ ______________________________________________________________________________________________________________________

		if fileobj.language == "C++":
			keywords = ['and','and_eq','asm','auto','bitand','bitor','bool','break','case','catch','char','class','compl','const','const_cast','continue','default','delete','do','double','dynamic_cast','else','enum','explicit','export','extern','false','float','for','friend','goto','if','inline','int','long','mutable','namespace','new','not','not_eq','operator','or','or_eq','private','protected','public','register','reinterpret_cast','return','short','signed','sizeof','static','static_cast','struct','switch','template','this','throw','true','try','typedef','typeid','typename','union','unsigned','using','virtual','void','volatile','wchar_t','while','xor','xor_eq']
			rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in keywords]

			preprocs = ['#define','#error','#include','#line','#pragma','#undef','#if','#ifdef','#ifndef','#else','#elif','#endif']
			rules += [(r'%s' % w, 0, self.styles['preproc']) for w in preprocs]


			braces = ['\{','\}','\(','\)','\[','\]']
			rules += [(r'%s' % w, 0, self.styles['brace']) for w in braces]

			rules += [
					(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['literal']), # Double-quote strings
					(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['literal']), # Single-quote strings
					(r'\b\d+\b', 0, self.styles['literal']), # Numbers
					(r'\/\/[^\n]*', 0, self.styles['comment'])
			]

# PYTHON ______________________________________________________________________________________________________________________



		elif fileobj.language == "Python":
			keywords = ['and', 'del', 'for', 'is', 'raise', 'assert', 'elif', 'from', 'lambda', 'return', 'break', 'else', 'global', 'not', 'try', 'class', 'except', 'if', 'or', 'while', 'continue', 'exec', 'import', 'pass', 'yield', 'def', 'finally', 'in', 'print']
			rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in keywords]

			preprocs = ['import', 'from' ]
			
			rules += [(r'%s' % w, 0, self.styles['preproc']) for w in preprocs]
			
			rules += [(r'def\:', 0, self.styles['defclass'])]
	

			braces = ['\{','\}','\(','\)','\[','\]']
			rules += [(r'%s' % w, 0, self.styles['brace']) for w in braces]

			rules += [
					(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['literal']), # Double-quote strings
					(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['literal']), # Single-quote strings
					(r'\b\d+\b', 0, self.styles['literal']), #Numbers
					(r'\#[^\n]*', 0, self.styles['comment'])
			]


# LOLCODE ______________________________________________________________________________________________________________________



		elif fileobj.language == "LOLCODE":
			keywords = ['HAI', 'KTHXBYE', 'VISIBLE', 'GIMMEH', 'I HAS A', 'IM IN YR LOOP', 'IM OUTTA YR LOOP', 'IZ', 'BIGGER THAN', 'UP' ]
			rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in keywords]

			preprocs = ['CAN HAS']
			
			rules += [(r'%s' % w, 0, self.styles['preproc']) for w in preprocs]
			
			rules += [(r'def\:', 0, self.styles['defclass'])]


			braces = ['\{','\}','\(','\)','\[','\]']
			rules += [(r'%s' % w, 0, self.styles['brace']) for w in braces]

			rules += [
					(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['literal']), # Double-quote strings
					(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['literal']), # Single-quote strings
					(r'\b\d+\b', 0, self.styles['literal']), #Numbers
					(r'BTW[^\n]*', 0, self.styles['comment'])
			]

# PROLOG ______________________________________________________________________________________________________________________




		elif fileobj.language == "Prolog":
			keywords = ['block', 'dynamic', 'mode', 'module', 'multifile', 'meta_predicate', 'parallel', 'sequential', 'volatile' ]
			rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in keywords]

			# in the case of prolog i've used the preproc style to highlight capitals for variables.
			preprocs = [(r'\b[A-Z]+[a-zA-Z]*\b')]
			
			rules += [(r'%s' % w, 0, self.styles['preproc']) for w in preprocs]
			
			rules += [(r'def\:', 0, self.styles['defclass'])]


			braces = ['\{','\}','\(','\)','\[','\]']
			rules += [(r'%s' % w, 0, self.styles['brace']) for w in braces]

			rules += [
					(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['literal']), # Double-quote strings
					(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['literal']), # Single-quote strings
					(r'\b\d+\b', 0, self.styles['literal']), #Numbers
					(r'\%[^\n]*', 0, self.styles['comment'])
			]


# LISP _______________________________________________________________________________________________________________________



		elif fileobj.language == "Lisp":
			keywords = ['car','cdr','setq','quote','eval','append','list','cons','atom','listp','null','memberp','nil','t','defun','abs','expt','sqrt','max','min','cond']
			rules += [(r'\b%s\b' % w, 0, self.styles['keyword']) for w in keywords]

			braces = ['\(','\)']
			rules += [(r'%s' % w, 0, self.styles['brace']) for w in braces]

			rules += [
					(r'"[^"\\]*(\\.[^"\\]*)*"', 0, self.styles['literal']), # Double-quote strings
					(r"'[^'\\]*(\\.[^'\\]*)*'", 0, self.styles['literal']), # Single-quote strings
					(r'\b\d+\b', 0, self.styles['literal']), #Numbers
					(r'\;[^\n]*', 0, self.styles['comment'])
			]


# WHITESPACE ____________________________________________________________________________________________________________________



		elif fileobj.language == "Whitespace":
			# OK, we're gonna do some crazy stuff with this one. Most of it needs to be defined by hand.
			rules += [
					(r' ', 0, self.styles['wsspace']),
					(r'\t', 0, self.styles['wstab'])
			]

		self.rules = [(QtCore.QRegExp(pattern), index, formatz) for (pattern, index, formatz) in rules]

	def highlightBlock(self, text):
		# Do other syntax formatting
		for expression, nth, format in self.rules:
			index = expression.indexIn(text, 0)

			while index >= 0:
				# We actually want the index of the nth match
				index = expression.pos(nth)
				length = expression.cap(nth).length()
				self.setFormat(index, length, format)
				index = expression.indexIn(text, index + length)
		self.setCurrentBlockState(0)
