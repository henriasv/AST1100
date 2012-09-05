import numpy as np
import copy
import sys

class Planet:
	def __init__(self, mass, radius, name, system):
		self.mass = float(mass)
		self.radius = float(radius)
		self.F = np.asarray([0.0, 0.0])
		self.system = system
		self.G = 6.67e-11
		self.name = name
		self.outfile = open(system.path + self.name + ".bin", 'wb')
		self.outfile.write(np.float64(self.radius));
		self.outfileradius = open(system.path + self.name + ".radius", 'wb')
		self.outfileradius.write(np.float64(self.radius))
		
	def set(self, mass, r, v, name):
		self.mass = float(mass)
		self.r = np.asarray(r)
		self.v = np.asarray(v)
		self.name = name

	def set_initial_condition(self, r0, v0):
		self.v = np.asarray(v0)
		self.r = np.asarray(r0)

	def get_radius(self):
		return self.radius

	def getForce(self, planet2):
		r_tmp = (planet2.r-self.r)
		force = -self.G*(self.mass*planet2.mass)*r_tmp/(np.linalg.norm(r_tmp)**3)
		return force

	def calculateForce(self):
		self.F = np.asarray([0.0, 0.0])
		for j in range(len(self.system.content)):
			if not (self.system.content[j] is self):
				#print "calculating force between % s and %s" % (self.system.content[j].name, self.name)
				self.F += self.system.content[j].getForce(self)
	
	def output(self):
		for i in range(len(self.r)):
			self.outfile.write(self.r[i])

	def getDistance(self, other):
		return np.linalg.norm(self.r+other.r)
	

class Planet_with_atmosphere(Planet):
	def __init__(self, mass, radius, name, system, atmosphere_radius, atmosphere_friction):
		Planet.__init__(self, mass, radius, name, system)
		self.atmosphere_radius = atmosphere_radius+radius
		self.atmosphere_friction = atmosphere_friction

	def getForce(self, planet2):
		r_tmp = (planet2.r-self.r)
		force = Planet.getForce(self, planet2);
		if (np.linalg.norm(r_tmp) < self.atmosphere_radius):
			force -= (planet2.v-self.v)*self.atmosphere_friction
		return force
		

class Solar_system:
	def __init__(self, outPath):
		self.content = [];
		self.old_content = [];
		self.path = outPath;

	def add(self, new_object):
		self.content.append(new_object);

	def solve(self, t_max, dt):
		t = 0;
		while t<t_max:
			self.output()
			self.calculateAllForces()
			self.integrate(dt)
			self.checkCollisions()
			t += dt

	def checkCollisions(self):
		i = 0;
		while i<len(self.content):
			j = i+1
			while j <len(self.content):
				minimum_distance = self.content[i].radius + self.content[j].radius
				if self.content[i].getDistance(self.content[j])< minimum_distance:
					self.collide(i, j)
				j+=1
			i+=1

	def calculateAllForces(self):
		for planet in self.content:
			planet.calculateForce()

	def integrate(self, dt):
		for planet in self.content:
			planet.v = planet.v + planet.F/planet.mass*dt
			planet.r = planet.r + planet.v*dt

	def output(self):
		for planet in self.content:
			planet.output()

	def collide(self, i1, i2):
		if (i1>i2):
			planet1 = self.content.pop(i1)
			planet2 = self.content.pop(i2)
			print "%s collided with %s" % (planet1.name, planet2.name)

		elif (i1<i2):
			planet2 = self.content.pop(i2)
			planet1 = self.content.pop(i1)
			print "%s collided with %s" % (planet1.name, planet2.name)

		else:
			# creating variables for the interpreter not to fail. No use..
			planet1 = 0
			planet2 = 0
			print "Error, object colliding itself!, exiting"
			sys.exit(1)

		if planet1.mass >= planet2.mass: # Keep properties from planet1
			new_planet = copy.deepcopy(planet1)
			new_v = (planet1.mass*planet1.v+planet2.mass*planet2.v)/(planet1.mass+planet2.mass)
			new_r = planet1.r
			new_planet.set(planet1.mass+planet2.mass, new_r, new_v, new_planet.name+"_collided")
			new_planet.outfile = planet1.outfile;
			
		elif planet1.mass < planet2.mass: # Keep properties from planet2
			new_planet = copy.deepcopy(planet2)
			new_v = (planet1.mass*planet1.v+planet2.mass*planet2.v)/(planet1.mass+planet2.mass)
			new_r = planet2.r
			new_planet.set(planet1.mass+planet2.mass, new_r, new_v, new_planet.name+"_collided")
			new_planet.outfile = planet2.outfile;
	
		else:
			print "Error in creating new planet"
			new_planet = 0;
			sys.exit(1)

		self.add(new_planet)
	
