import os
import sys
import glob
import numpy as np
import time
from scitools.easyviz.matplotlib_ import plot, hold, figure, axis
from matplotlib.pylab import ion, draw

class Support:
	@staticmethod
	def listdir_str(path, marker):
   		return glob.glob(os.path.join(path, '*'+marker))

path = os.getcwd() + "/" + sys.argv[1] + "/"

infiles = []

listing = Support.listdir_str(path, ".bin")
for infile in listing:
	infiles.append(infile)
	print infile

planets = []
planets_resh = []
radii = []

i = 0;
for instance in infiles:
	planets.append(np.fromfile(instance))
	radii.append(planets[i][0])
	planets[i] = np.delete(planets[i], 0)
	i+=1

for i in range(len(planets)):
	planets_resh.append(planets[i].reshape(len(planets[i])/2, 2))

try:
	plotOption = sys.argv[2]
except IndexError:
	print "No plot option provided. Options are: plot and movie"
	sys.exit(1)

if plotOption == "plot":
	for instance in planets_resh:
		try:
			plot(instance[:, 0], instance[:, 1], '*')
			hold('on')
		except:
			print "ValueError!"

# movie:
if plotOption == "movie":
	ion()
	figure()
	colors = ['*r', '*b', '*m']
	min_length = 0;
	min_x = 0; max_x = 0; min_y = 0; max_y = 0;
	for i in range(len(planets_resh)):
		max_x_tmp = planets_resh[i].max();
		if max_x_tmp>max_x:
			max_x = max_x_tmp
		min_x_tmp = planets_resh[i].min();
		if min_x_tmp<min_x:
			min_x = min_x_tmp
		max_y_tmp = planets_resh[i].max();
		if max_y_tmp>max_y:
			max_y = max_y_tmp
		min_y_tmp = planets_resh[i].min();
		if min_y_tmp<min_y:
			min_y = min_y_tmp
	axis_choice = [min_x, max_x, min_y, max_y]
	print axis_choice
	for i in range(len(planets_resh)):
		if len(planets[i])>min_length:
			min_length = len(planets[i])

	for i in range(0, min_length, 100):
		for j in range(len(planets)):
			try:
				point = (planets_resh[j][i])
				plot_array = []
				for theta in np.linspace(0, 2*np.pi, 100):
					plot_array.append([point[0] + radii[j]*np.sin(theta), point[1] + radii[j]*np.cos(theta)])
				plot_array = np.asarray(plot_array)
				plot(plot_array[:, 0], plot_array[:, 1], colors[j], axis=axis_choice)
				#plot(planets_resh[j][i:i+1, 0], planets_resh[j][i:i+1, 1],colors[j])
				hold('on')
				#time.sleep(0.1)
			except:
				print "Could not plot something"
		draw()
		hold('off')
raw_input("press enter")

