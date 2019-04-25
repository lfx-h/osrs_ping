import subprocess, re, requests
from bs4 import BeautifulSoup as bs
bestping = []

def ping(world):
	result = subprocess.check_output(('ping oldschool%d.runescape.com -n 1 | find "time="' % world), shell=True)
	split_res = result.split(' ')
	locator = 'time='
	global bestping

	for x in split_res:
		if locator in x:
			ms = re.findall('\d+', x).pop()
			if int(ms) < 60:
				ms = ms, 'ms - good'
			elif int(ms) < 160:
				ms = ms, 'ms - ok ping'
			else:
				ms = ms, 'ms'
		
			if len(bestping) == 0:
				bestping.append((world, ms[0]))
			if int(ms[0]) < int(bestping[0][1]):
				del bestping[:]
				bestping.append((world, ms[0]))
			elif int(ms[0]) == int(bestping[0][1]):
				bestping.append((world, ms[0]))
			
	return ms
	
def number_worlds():
	content = requests.get('http://oldschool.runescape.com/slu').text
	soup = bs(content, "html.parser")
	data = 'class="server-list__world-link"'
	locator = 'chool'
	world_list = []
	
	for a in soup.find_all('a', {'class' : 'server-list__world-link'}):
		for x in a:
			if locator in x:
				world = re.findall('\d+', x)
				world_list.extend(world)
		
	number_of_worlds = len(soup.find_all('a', {'class' : 'server-list__world-link'}))
	world_list = [int(s) for s in world_list]
	world_list.sort()
	
	return world_list
	
def printed():
	for world in number_worlds():
		while True:
			try:
				print 'World ', world, ': ', ' '.join(map(str, (ping(world))))
			except subprocess.CalledProcessError:
				print 'Error, retrying...\n'
				continue
			break
	
print 'Welcome to OSRS World Ping Checker!'
print ' ====    ====    ====     ====       ====    ==   =     =    ===='
print '||   |  ||      ||   |   ||         ||   |   ||   |\    |   ||'
print '||   |   ====   |====     ====      |====    ||   ||\   |   ||  _' 
print '||   |      ||  ||  \        ||     ||       ||   || \  |   ||   |'
print ' ====    ====   ||   \    ====      ||       ||   ||  \ |    ===='
print 'This ping checker is scripted to update even when new worlds are released because it takes the server list directly from http://oldschool.runescape.com/slu\nType everything without " "\nNote that the program is simple for the sake of SPEED, adding various filters greatly slowed down the program\n\nPing Thresholds:\nok ping   < 160ms\ngood ping < 50ms\n\n'
while True:
	print 'Specific world:  type # of world'
	print 'All worlds:      press enter (recommended)'
	var = raw_input()
	if var == "":
		printed()
	else:
		try:
			world = int(var)
			if world in number_worlds():
				print 'World ', world, ':', ' '.join(map(str, (ping(world)))), '\n\n'
			else:
				print "\n\n\nValue Error: Wrong parameters entered, selected world doesn't exist\n"
				continue
		except ValueError:
			print "\n\n\nValue Error: Wrong parameters entered, selected world doesn't exist\n"
			continue
	
	print '\n\nBest ping worlds: '
	print 'World     ping\n----------------'
	for p in bestping:
		print '#', p[0], '  - ', p[1], 'ms'
	print '----------------'
	print 'To test again press enter'
	print 'To close press ctrl + c'
	raw_input()	
