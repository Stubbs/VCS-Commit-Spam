#!/usr/bin/env python
# encoding: utf-8
"""
checkin-filter.py

Created by Stuart Grimshaw on 2009-05-25.
Copyright (c) 2009 Stuart Grimshaw. All rights reserved.
"""

import sys
import getopt
import re
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
			opts, args = getopt.getopt(argv[1:], "tgho:vps", ["help", "output=", "train=", "guess="])
		except getopt.error, msg:
			raise Usage(msg)

		filter =  CommitFilter()
		verbose = False
		pretend = False
		
		# option processing
		for option, value in opts:
			if option == "-v":
				verbose = True
			elif option == "-p":
				pretend = True
			elif option in ("-h", "--help"):
				raise Usage(help_message)
			elif option in ("-o", "--output"):
				output = value
			elif option in("-t", "--train"):
				filter.train('fail', value.lower())
				filter.save(fname=filter.fname)
			elif option in("-g", "--guess"):
				# Check for a comment that's just punctuation
				if re.match('$\p+^', value) or len(value) == 1:
					return 1
				
				# Loop throught the results of the guess and see if any fail
				for group, percentage in filter.guess(value.lower()):
					if group == 'fail' and percentage > 0.90:
						if verbose:
							print percentage

						if pretend:
							print "That looks like spam to me"
						else:
							return 1
			elif option in("-s", "--stats"):
				print filter.poolTokens('fail')
			else:
				raise Usage()
	
	except Usage, err:
		print >> sys.stderr, sys.argv[0].split("/")[-1] + ": " + str(err.msg)
		return 2


if __name__ == "__main__":
	sys.exit(main())
