
### Beagle Landing ###
solar = Solar_system(path)

# Create planets
mars = Planet_with_atmosphere(6.4e23, 3400e3, "mars", solar,  11000e3, 1.6e-4)
mars.set_initial_condition([0, 0], [0, 0])
beagle2 = Planet(100, 10, "Beagle2", solar)
beagle2.set_initial_condition([(-298-3400)*1e3, 0], [0, -4000])

# Add planets to solar system: solar.add(planet)
solar.add(mars) 
solar.add(beagle2)

# Choose timing options
t_max = 100000 # seconds
dt = 1 # seconds

solar.solve(t_max, dt)
