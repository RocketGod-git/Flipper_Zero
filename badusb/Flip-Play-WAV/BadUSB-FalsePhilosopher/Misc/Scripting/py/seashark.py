#!/usr/bin/python

# seashark
#
# This is the authoritative implementation of the C^ programming language. C^ is
# 100% syntax-agnostic and it doesn't care about what your code is trying to do.
# All code executes 100% error- and bug-free because C^ doesn't distinguish
# between success and failure. In fact, C^ cares so little about... anything
# that it will bite big chunks out of your source code every time you run it.
# If you agree with ancient wisdom such as "can't have bugs if you don't have
# code", C^ is the language for you.
#
# The C^ interpreter was coded in Python because it's slow and that doesn't
# matter.
#
################################################################################
# WARNING ~~~~\O/~~~~~~^~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
#                                                                              #
# C^ will destroy your source code or whatever file you pass to it.            #
# I'm not kidding.                                                             #
# Seriously.                                                                   #
################################################################################

import sys
import random
from os.path import exists

shark = "[C^]"

if len(sys.argv) < 2:
	print(shark, "Usage: seashark [filename]")
	quit()

filename = sys.argv[1]

if not exists(filename):
	print(shark, "Cannot find", filename)
	quit()

with open(filename) as file:
	lines = file.readlines()
	lines = [line.rstrip() for line in lines]
	lines = [line[:random.randint(0, 80)] for line in lines]

with open(filename, 'w') as file:
	for line in lines:
		file.write("%s\n" % line)

print(shark, filename, "executed successfully. EXECUTED.")
