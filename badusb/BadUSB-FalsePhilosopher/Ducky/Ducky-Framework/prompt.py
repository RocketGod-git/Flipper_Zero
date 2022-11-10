#!/bin/python3

import os
import time

def prompt():

	print('Choose platform...' )
	print('\t1. Windows ')
	print('\t2. Linux ')
	print('\t3. Os X')
	print('\t99. Exit')

	while(True):
		try:
			ch = input('\n[Quack]>	')

			if ((int(ch) < 1 or int(ch) > 3) and int(ch) != 99):
				print('You need to supply a number between 1 and 3!! ')
			else:
				break
		except:
			print('Please give a number between 1 and 3')

	#line25
	defaultPath = '/home/ghost/scripts/python/duckyFramework/git'



	if (int(ch) == 1):
		p = '/payloads/win'

	elif (int(ch) == 2):
		p = '/payloads/lin'

	elif (int(ch) == 3):
		p = '/payloads/osx'

	else:
		print('Bye\t\tQuack!')
		exit()

	#store payloads
	path = defaultPath + p + '/'
	path = path.replace('\n', '')
	payloads = os.listdir(path)
	options = []
	for dir in payloads:
		options.append(path+'/'+dir)

	#print payloads
	num = 0
	for o in options:
		print(num,o.replace(path+'/',''))
		num +=1
	print('\n99 Exit')

	while(True):
		try:
			ch = input('\n[Quack]>  ')
			if ((int(ch) < 0 or int(ch) >= len(options))and int(ch) != 99):
				print('plase supply a number available')
			else:
				break

		except:
			print('Please supply a number')

	if (int(ch) == 99):
		print('Bye\t\tQuack!')
		exit()

	os.system('/usr/bin/cp '+options[int(ch)]+'/*.txt ./payload.txt')
	print('A payload.txt has been created...')
	time.sleep(1)

	print('\nHere comes a short description...\n')
	os.system('/usr/bin/cat '+options[int(ch)]+'/readme.md')
	print("\n\n\nI recomend that if you don't need to change anything, you should read it too\n")


if __name__ == '__main__':
	prompt()
