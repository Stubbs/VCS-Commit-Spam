#!/usr/bin/env python
# encoding: utf-8
"""
checkin-filter.py

Created by Stuart Grimshaw on 2009-05-25.
Copyright (c) 2009 Stuart Grimshaw. All rights reserved.
"""

import sys
import getopt
from reverend.thomas import Bayes


help_message = '''
Bayesian filters for any CVS that provides pre-commit hooks.

	-t "message"		Train the comment filter, this should be a copy of  
	--train "message"	the kind of commit message you consider bad.

	-g "message"		Guess if this commit message is good or bad. Returns 1
	--guess "message"	if it's bad, 0 if it's good
'''


class Usage(Exception):
	def __init__(self, msg):
		self.msg = msg
		
class CommitFilter(Bayes):
	def __init__(self, fileName='commitfilter.bayes'):
		super(CommitFilter, self).__init__()
		
		self.fname = fileName
		
		try:
			self.load(fname=self.fname)
		except IOError, msg:
			print "Unable to open filter file, will create a new one after training."

	def filterMessage(self, msg):
		self.guess

def main(argv=None):
	if argv is None:
		argv = sys.argv
	try:
		try:
			opts, args = getopt.getopt(argv[1:], "tgho:vs", ["help", "output=", "train=", "guess="])
		except getopt.error, msg:
			raise Usage(msg)

		filter =  CommitFilter()

		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			elif option in ("-h", "--help"):
				raise Usage(help_message)
			elif option in ("-o", "--output"):
				output = value
			elif option in("-t", "--train"):
				filter.train('fail', value)
				filter.save(fname=filter.fname)
			elif option in("-g", "--guess"):
				print filter.guess(value)
			elif option in("-s", "--stats"):
				print filter.poolTokens('fail')
			else:
				raise Usage()
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		return 2


if __name__ == "__main__":
	sys.exit(main())
