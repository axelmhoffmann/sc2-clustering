import sc2reader
from tabulate import tabulate
import os

#######################################################################################################
# Takes all the abc.SC2Replay files in the current directory and outputs a time-series vector abc.txt #
#######################################################################################################

# The time between each sample in the time series (in SC2 gameticks, 20t = 1s)
resolution = 600
# Maximum amount of samples in the time series
limit = 30


path = os.getcwd()
os.mkdir(path + '/vectors')

# Each unit type recording is seperately hardcoded, because unfortunately some units have different behaviour and corresponding events
players = list()
p1zlings = list()
p1drones = list()
p1roaches = list()
p1hydras = list()
p1mutas = list()
p1banes = list()

def resetLists():
	global p1zlings, p1drones, p1roaches, p1hydras, p1mutas, p1banes
	players = list()
	p1zlings = [0]
	p1drones = [0]
	p1roaches = [0]
	p1hydras = [0]
	p1mutas = [0]
	p1banes = [0]

def appendAll(last):
	global p1zlings, p1drones, p1roaches, p1hydras, p1mutas, p1banes
	p1zlings.append(p1zlings[last])
	p1drones.append(p1drones[last])
	p1roaches.append(p1roaches[last])
	p1hydras.append(p1hydras[last])
	p1mutas.append(p1mutas[last])
	p1banes.append(p1banes[last])

def computeReplay(replay):
	global p1zlings, p1drones, p1roaches, p1hydras, p1mutas, p1banes
	replay = sc2reader.load_replay(replay)

	resetLists()
	# Get each team from the game summary
	for team in replay.teams:
		# Use to find each player in order to sort the events by player
		players.append(team.players[0].pid)

	playerOfInterest = players[0]

	for event in replay.events:
		# Things such as minerals are spawned in frame 0. Ignore them as they are irrelevant
		if event.frame == 0:
			continue

		# Units that are born mainly include troops and workers.
		if type(event) is sc2reader.events.tracker.UnitBornEvent:
			if event.control_pid != playerOfInterest:
				continue
			index = int(event.frame / resolution)
			last = len(p1zlings) - 1
			if index >= limit:
				break
			if index > last & last >= 0:
				appendAll(last)

			if event.unit.name == "Zergling":
				p1zlings[index] += 1
			if event.unit.name == "Roach":
				p1roaches[index] += 1
			if event.unit.name == "Drone":
				p1drones[index] += 1
			if event.unit.name == "Hydralisk":
				p1hydras[index] += 1
			if event.unit.name == "Mutalisk":
				p1mutas[index] += 1
			if event.unit.name == "Baneling":
				p1banes[index] += 1

		if type(event) is sc2reader.events.tracker.UnitDiedEvent:
			if event.killing_player_id != players[1]:
				continue
			index = int(event.frame / resolution)
			last = len(p1zlings) - 1
			if index > last & last >= 0:
				appendAll(last)
			
			if event.unit.name == "Zergling":
				p1zlings[index] -= 1
			if event.unit.name == "Roach":
				p1roaches[index] -= 1
			if event.unit.name == "Drone":
				p1drones[index] -= 1
			if event.unit.name == "Hydralisk":
				p1hydras[index] -= 1
			if event.unit.name == "Mutalisk":
				p1mutas[index] -= 1
			# For some reason, baneling spawning can't be properly tracked by any event. So we count their deaths (uses) instead
			if event.unit.name == "Baneling":
				p1banes[index] += 1

	data = [p1drones, p1zlings, p1roaches, p1hydras, p1mutas, p1banes]
	return data


replays = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) & f.endswith('.SC2Replay'))]
print('Vectorising {0} replays...'.format(len(replays)))

for r in replays:
	rPath = path + "/" + r

	vect = computeReplay(rPath)
	dataStr = str(vect)

	name = r.split('.', 1)[0]
	saveFile = open('vectors/' + name + '.txt', 'w+')
	saveFile.write(dataStr)
	saveFile.close()
