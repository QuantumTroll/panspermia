import sys
import pygame as pg
import random
import copy
import math

import traits

### 
# to do list
# 
#  honestly, I should revisit traits and include pheno and biome prereqs and requirements
#   prereqs and reqs are checked when looking for available traits
#   only reqs are checked when looking at biome availability and redundant traits
#
#  soil: biome and traits (for plants, animals, and microbes)
#  toxic: traits
#  more traits: plant stuff
#  more traits: camouflage and looks, e.g. mandibles
#  citybuilder ecological disaster and special evolution rules
#  interplanetary asteroid defense
#  interplanetary/interstellar migration
#    - select a set of useful/supporting species in the biome(s)
#   traits: stuff in caverns
#  warmblooded: requires propel (actually circulatory)

# simulation has stars, planets, age, etc
class Simulation:
	def __init__(self,num_stars,num_planets_per_star):
		print("Initialising simulation")
		if len(sys.argv) > 1:
			random.seed(sys.argv[1])
			print("Seed:",sys.argv[1])
		else:
			random.seed()
			seed = random.randint(0,10000000)
			random.seed(seed)
			print("Random seed:",seed)
		
		self.age = 0
		self.running = False
		self.stars = []
		# load up all the traits
		self.traits = self.loadTraits()
		
		print("Creating stars & planets")
		# create stars with planets
		for i in range(0,num_stars):
			r = i*20/num_stars + random.randint(1,6)
			position = (r*math.sin(i*.5),r*math.cos(i*.5))
			num = num_planets_per_star + random.randint(-2,2)
			self.stars.append( Star(num, position,(r,i), self.traits ))
		
		# spawn life on a planet
		planet0 = self.findPlanet('ocean')
			
		planet0.abiogenesis()
		
	def findPlanet(self,type):
		for s in self.stars:
			for p in s.planets:
				if p.type == type:
					return p
	
	def drawAllLifeforms(self):
		print("Draw all lifeforms")
		
	def loadTraits(self):
		print("Loading all possible traits")
		list = []
		lib = traits.getTraits()
		id = 0
		for t in lib:
			trait = Trait(t['name'],t['pheno_prereqs'],t['pheno_nopes'],t['pheno_tags'],t['biome_reqs'],t['biome_tols'],t['biome_impacts'],t['eco_impacts'],t['num_per_planet'], t['description'], t['stage'], t['org_type'], id)
			list.append(trait)
			id += 1
		print(id,"traits loaded")
		return list
		
		
	def iterate(self):
		self.age += 1
		print("Taking a simulation step:",self.age)
		# handle evolution for each star system
		for star in self.stars:
			star.updatePos(self.age)
			star.evolve()
		# handle interstellar events
		print("Step complete")
		
	def asteroid(self,planet):
		print("ASTEROID ON PLANET",planet.name)
		forms = planet.asteroid()
		print(len(forms),"lifeforms floating through space")
		if len(forms) < 1:
			return
		for p in planet.star.planets:
			if len(p.lifeforms)>0 or random.random() > 0.5 or p == planet: # 50% chance of a neighboring planet to be seeded if planet is empty
				continue
				
			# add a lifeform to p
			for f in forms:
				form = f.makeCopyForPlanet(p)				
				p.addLifeform(form)
		# find nearby stars and seed life
		starPos  = planet.star.position
		spread_radius = 5
		for s in self.stars:
			if math.dist(starPos,s.position) < spread_radius:
				s.seedForms(forms)
		
# stars just have a list of planets
class Star:

	def __init__(self,num_planets,pos,params,traits):
		self.position = pos
		self.params = params
		self.planets = []
		# populate planets
		r_mid = 1 + random.random()*0.25 - 0.125
		r_per_planet = 1.0/num_planets
		r = r_mid - (num_planets-1)*r_per_planet/2
		for i in range(0,num_planets):			
			self.planets.append( Planet(self,traits[:],r) ) # pass a copy of all traits to the planet					
			r += r_per_planet
	
	def updatePos(self,age):	 # rotate about centre of galaxy
		r = self.params[0]
		i = self.params[1]
		mul = age*.1
		v = 1.0/r
		rotphase = v*mul
		self.position = (r*math.sin(i*.5+rotphase),r*math.cos(i*.5+rotphase))

	
	def hasLife(self):
		for planet in self.planets:
			if len(planet.lifeforms) > 0:
				return True
		return False	
	
	def evolve(self):
		for p in self.planets:
			p.evolve()
			p.cull()

	def seedForms(self, forms):
		print("star in",self.position,"seeded")
		for p in self.planets:
			if len(p.lifeforms) == 0 and random.random() < 0.5:
				print("seeding life on",p.name)
				# try to add a lifeform to p
				for f in forms:
					form = f.makeCopyForPlanet(p)				
					p.addLifeform(form)
		
		
# planets are more interesting   
class Planet:
	def __init__(self,star, traits, distance):
		self.max_lifeforms = 1800
		self.id = random.randint(0,1000000)
		self.type = ''
		self.star = star
		self.distance = distance # distance to star

		self.biomes = []
		self.setBiomes()
		self.generateName()	
		self.lifeforms = []		
		#self.addTagToAtmo('Sulfur')
		self.has_builder = False
		self.has_interplanetary = False				
		self.has_interstellar = False
		self.traits = traits
		
	def setBiomes(self):
		
		is_radioactive = False
		if random.random() < 0.3:
			is_radioactive = True
			self.max_lifeforms *= 1.2
		
		if self.distance < 0.65:
			self.max_lifeforms *= 0.3
			# burned world
			self.type = 'burned'
			self.biomes.append( Biome(self,'mudpit',True,['light','sand','sludge'], [],[]) )
			self.biomes.append( Biome(self,'land',True,['light','sand','rock','dry'], [],['dry']) )
			self.biomes.append( Biome(self,'desert',True,['light','sand','rock','dry','arid'], [],['dry','arid']) )		
			if is_radioactive:
				self.biomes.append( Biome(self,'plutonium fields', True, ['sand','dry', 'radiation'], [],['radiation','dry']) )
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')

		elif self.distance < 0.85:
			self.max_lifeforms *= 0.5
			# hot world		
			self.type = 'hot'			
			self.biomes.append( Biome(self,'shallow sea',True,['water','light','sludge'], [],[]) )
			self.biomes.append( Biome(self,'beach',True,['light','sand'], [],[]) )
			self.biomes.append( Biome(self,'land',True,['light','sand','rock','dry'], [],['dry']) )
			self.biomes.append( Biome(self,'desert',True,['light','sand','rock','dry','arid'], [],['dry','arid']) )
			
			if is_radioactive:
				self.biomes.append( Biome(self,'radon caverns', True, ['sand','rock','dry','radiation'], [],['dry','radiation']) )
			else:
				self.biomes.append( Biome(self,'caverns',True,['sand','rock','dry'], [],['dry']) )
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')
		elif self.distance < 1.15:
			self.max_lifeforms *= 1
			if random.random() < 0.2:
				# ocean
				self.type = 'ocean'
				self.max_lifeforms *= 0.5
				self.biomes.append( Biome(self,'shallow sea',True,['water','light','sludge'], [],[]) )
				self.biomes.append( Biome(self,'deep sea',False,['water','sludge'], [],[]) )
				if is_radioactive:
					self.biomes.append( Biome(self,'uranium trench', False, ['water', 'sludge', 'radiation'], [],['radiation']) )
				self.biomes.append( Biome(self,'cold sea',True,['light','water','cold'], [],['cold']) )
				self.biomes.append( Biome(self,'icecap',True,['light','water','frozen'], [],['frozen']) )		
			else:
				# temperate
				self.type = 'temperate'
				self.biomes.append( Biome(self,'shallow sea',True,['water','light','sludge'], [],[]) )
				self.biomes.append( Biome(self,'deep sea',False,['water','sludge'], [],[]) )
				if is_radioactive:
					self.biomes.append( Biome(self,'uranium trench', False, ['water', 'sludge', 'radiation'], [],['radiation']) )
				self.biomes.append( Biome(self,'beach',True,['light','sand'], [],[]) )
				self.biomes.append( Biome(self,'land',True,['light','sand','rock','dry'], [],['dry']) )
				if random.random() < 0.5:
					self.biomes.append( Biome(self,'desert', True, ['light', 'sand', 'rock','dry', 'arid'], [],['dry','arid']) )
				else:
					self.biomes.append( Biome(self,'cold sea',True,['light','water','cold'], [],['cold']) )
				self.biomes.append( Biome(self,'tundra',True,['light','sand','rock','dry','cold'], [],['dry','cold']) )
				if random.random() < 0.5:
					self.biomes.append( Biome(self,'icecap',True,['light','sand','rock','cold','frozen'], [],['cold','frozen']) )		
			
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')
		elif self.distance < 1.35:
			self.max_lifeforms *= 0.4
			# cold	
			self.type = 'cold'
			self.biomes.append( Biome(self,'shallow sea',True,['water','light','sludge'], [],[]) )
			self.biomes.append( Biome(self,'deep cold sea',False,['water','sludge','cold'], [],['cold']) )
			if is_radioactive:
				self.biomes.append( Biome(self,'radium sea', True, ['water','light', 'sludge', 'radiation'], [],['radiation']) )
			self.biomes.append( Biome(self,'beach',True,['light','sand','cold'], [],['cold']) )
			self.biomes.append( Biome(self,'land',True,['light','sand','rock','dry','cold'], [],['dry','cold']) )
			if random.random() < 0.5:
				self.biomes.append( Biome(self,'frozen desert', True, ['light', 'sand', 'rock', 'dry','arid','frozen'], [],['dry','arid','frozen']) )
			else:
				self.biomes.append( Biome(self,'frozen ocean',False,['water','sand','rock','frozen'], [],['frozen']) )		
			self.biomes.append( Biome(self,'tundra',True,['light','sand','rock','dry','cold'], [],['dry','cold']) )
			self.biomes.append( Biome(self,'icecap',True,['light','sand','rock','dry','cold','frozen'], [],['dry','cold','frozen']) )		
			
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')
		else:
			self.max_lifeforms *= 0.3
			# frozen
			self.type = 'frozen'
			self.biomes.append( Biome(self,'frozen ocean',False,['water','sand','rock','frozen'], [],['frozen']) )	
			self.biomes.append( Biome(self,'icecap',True,['light','sand','rock','frozen'], [],['frozen']) )
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')
		
		self.max_lifeforms = int(self.max_lifeforms)
	
	def cull(self):
		num_to_die = len(self.lifeforms) - self.max_lifeforms 
		if num_to_die < 0:
			return
		#print(len(self.lifeforms),'-',self.max_lifeforms,'=',num_to_die )
		chance = num_to_die / self.max_lifeforms
		if random.random() > chance:
			return

		asteroid_chance = chance * 0.05
		if random.random() < asteroid_chance:
			sim.asteroid(self)
			num_to_die = len(self.lifeforms) - self.max_lifeforms 
			if num_to_die < 0:
				return			
		
		# identify biomes with less than 10% of total population	
		threshold = len(self.lifeforms) / 10.0
		protected_biomes = []
		for b in self.biomes:
			if len(b.lifeforms) < threshold:
				protected_biomes.append(b)
			
		kill_list = []
		while num_to_die > 0:
			f = random.choice(self.lifeforms)
			# randomly exempt microbiome
#			if not f.is_multicellular and random.random() < .25:
#				continue
			# exempt younger species
			if random.random() < 1-(f.age)*0.8:
				continue
			# exempt species with a presence in a low-pop biome	
			exempt = False
			for b in protected_biomes:
				if f in b.lifeforms:
					exempt = True
					break
			for b in f.biomes:
				if not f.description in b.lifelist:
					continue
				if b.lifelist[f.description] < 2:
					exempt = True
					break
			if exempt:
				continue
			num_to_die -= 1 # may double-count, but this is intentional	
			if not f in kill_list:
				kill_list.append(f)
	#	print(len(kill_list))		
		for f in kill_list:
			f.kill()	
	#	print(len(self.lifeforms))
		
	def asteroid(self):
		print("Asteroid on planet",self.id)
		spread = []
		death_rate_sea = random.random()*0.2 + 0.8		
		death_rate_land = random.random()*0.3 + 0.7	
		print("death rate",death_rate_sea,"and",death_rate_land,"on sea and land")
		spread_rate_sea = random.random()*0.1
		spread_rate_land = random.random()*0.01
		kill_list = []
		for f in self.lifeforms:
			deathrate = death_rate_sea
			spreadrate = spread_rate_land
			for b in f.biomes:
				if not 'water' in b.geo_tags:
					deathrate = death_rate_land
				else:
					spreadrate = spread_rate_sea
			
			if random.random() < spreadrate and not f.is_multicellular:
				spread.append(f)
			if random.random() < deathrate:
				kill_list.append(f)
		
		for f in kill_list:
			f.kill()							
		
		print(len(self.lifeforms),"lifeforms survived")
		
		return spread	
	
	def abiogenesis(self):
		print("Performing abiogenesis on planet",self.id)
		if False:
			print("  Forcing biomes")
			self.max_lifeforms = 1500
			# populate biomes 	
			self.biomes = []
			self.biomes.append( Biome(self,'shallow sea',True,['water','light','sludge'], [],[]) )
			self.biomes.append( Biome(self,'deep sea',False,['water','sludge'], [],[]) )
			self.biomes.append( Biome(self,'uranium trench', False, ['water', 'sludge', 'radiation'], [],['radiation']) )
			self.biomes.append( Biome(self,'beach',True,['light','sand','rock'], [],[]) )
			self.biomes.append( Biome(self,'land',True,['light','sand','rock','dry'], [],['dry']) )
			self.biomes.append( Biome(self,'desert',True,['light','sand','rock','dry','arid'], [],['dry','arid']) )		
			self.biomes.append( Biome(self,'tundra',True,['light','sand','rock','dry','cold'], [],['dry','cold']) )
			self.biomes.append( Biome(self,'icecap',True,['light','sand','rock','frozen'], [],['frozen']) )	
			self.atmosphere = []
			self.addTagToAtmo('CO2')
			self.addTagToAtmo('Nitrogen')
		
		print("  Picking initial trait")
		for t in self.traits:
			if 'micro_eat_sludge' in t.name:			
				traits = [copy.deepcopy(t)]
		print("  Generating genome")
		traits[0].genGenome()		
		self.addLifeform( Lifeform( None, self, traits ) )
		print("  First organism created: ",traits[0].genome)
	
	def addLifeform(self, form):						
		self.lifeforms.append(form)
		for t in form.traits:
			for pt in self.traits:
				if t.name == pt.name:
					pt.num_per_planet += 1
		
	def removeLifeform(self, form):
		if not form in self.lifeforms:
			return
		self.lifeforms.remove(form)
		for t in form.traits:
			for pt in self.traits:
				if t.name == pt.name:
					pt.num_per_planet -= 1
	
	def evolve(self):
#		print("Evolving planet geologies")		# nothing for now	
		# Todo: clear out e.g. oxygen if no oxygen-producing species
		# for each lifeform, evolve it according to its current biomes
		
		new_forms = []
		for form in self.lifeforms: 		
			new = form.evolve(self.traits)										
			if new: 
				new_forms.append(new)
		if len(self.lifeforms) > 0:
			print("Planet",self.name,":",len(self.lifeforms),"plus",len(new_forms),'new')
		for new in new_forms:
			self.addLifeform(new)
		
# for each lifeform, find biomes that fit, killing the ones that have no biome	
		for b in self.biomes:
			b.lifeforms = []
			b.lifelist = {}
			
		#kill = []
		#for form in self.lifeforms:
		# kill older species, not younger species
		#	killchance = form.age/20.0
		#	if random.random() < killchance and len(self.lifeforms) > 1:
				# kill off species
		#		kill.append(form)
					
		#for k in kill:
		#	k.kill()
			
		for form in self.lifeforms:
			form.findBiomes()
		
# for each lifeform, call addImpactsToBiomes	
		for b in self.biomes:
			b.clearEcoTags()
		for form in self.lifeforms:
			form.addImpactsToBiomes()
	
	def addTagToAtmo(self, tag):
		if not tag in self.atmosphere:
			self.atmosphere.append(tag)
			for b in self.biomes:
				if b.atmo and not tag in b.geo_tags:					
					b.geo_tags.append(tag)					
	
	def generateName(self):	
		if self.type == 'burned':
			self.name = random.choice(['Char','Pyro','Mag','Surt'])
		elif self.type == 'hot':
			self.name = random.choice(['Tropo','Sved','Sole','Nova'])
		elif self.type == 'temperate':
			self.name = random.choice(['Terra','Geo','Meso','Neo'])
		elif self.type == 'ocean':
			self.name = random.choice(['Hydro','Mar','Aqu'])
		elif self.type == 'cold':
			self.name = random.choice(['Nor','Fin','Jar','Ir'])						
		else:
			self.name = random.choice(['Ice','Nep','Plut','Kuip'])
		
		self.name += random.choice(['oid', 'erra', 'ozone', 'loth', 'sphere', 'une', 'us', 'iter','etus','rus','irun','eron','ron','ter','ius'])			
		
	def cityBuilder(self, lifeform):

		if self.has_builder:			
			return
			
		print("CITY BUILDER:",lifeform.id)	
		print("city builder on planet",self.name)
		self.has_builder = True
		
		# TODO: rethink this a bit. Also, add the "city" tag. And then when this species dies, remove "city" and replace with "ruin" instead.
		# create new biomes
		for b in lifeform.biomes:
			self.biomes.append( Biome(self,b.type+' city',b.atmo,b.geo_tags,[],b.hazards) )
			
		# add toxic to random biome
		biome = random.choice(self.biomes)
		biome.hazards.append('toxic')
		biome.geo_tags.append('toxic')
		biome.type = 'toxic ' + biome.type
		# do mass extinction
		
		sim.running = False
		
	def interplanetary(self, lifeform):

		if self.has_interplanetary:			
			return
			
		print("INTERPLANETARY:",lifeform.id)	
		print("interplanetary on planet",self.name)
		self.has_interplanetary = True
		
		# do migration to in-system planets
		
		sim.running = False
		
	def interstellar(self, lifeform):

		if self.has_interplanetary:			
			return
			
		print("INTERSTELLAR:",lifeform.id)	
		print("interstellar on planet",self.name)
		self.has_interstellar = True
		
		# do migration to in-system planets
		
		sim.running = False
			
# biome
class Biome:
	def __init__(self,planet,type,atmo,geo_tags,eco_tags,hazards):
		self.planet = planet
		self.type = type
		self.atmo = atmo
		self.geo_tags = geo_tags
		self.eco_tags = eco_tags	
		self.hazards = hazards
		self.lifeforms = []
		self.lifelist = {}
	def addLifeform(self, form):		
		#for l in self.lifeforms:
		#	if form.size > l.size:
		#		self.lifeforms.insert(self.lifeforms.index(l)+1,form)
		#		break					
		#if not form in self.lifeforms:
		self.lifeforms.append(form)
		if form.description in self.lifelist:
			self.lifelist[form.description] += 1
		else:
			self.lifelist[form.description] = 1
	def removeLifeform(self, form):
		if not form in self.lifeforms:
			print("WARNING: tried to remove missing lifeform from",self.type,self.planet.name)
			return
		self.lifeforms.remove(form)	
		if form.description in self.lifelist:
			self.lifelist[form.description] -= 1
	def addHazard(self,tag):
		if not tag in self.hazards:		
			self.hazards.append(tag)	
	def addGeoTag(self,tag):
		if not tag in self.geo_tags:		
			self.geo_tags.append(tag)
			# check if geo_tag is a hazard property	
			if tag in ['radiation','toxic','dry','arid']:
				self.hazards.append(tag)
			# check if geo_tag is an atmospheric property
			if self.atmo:
				if  tag in ['O2','methane','CO2']:
					self.planet.addTagToAtmo(tag)
	def addEcoTag(self,tag):
		self.eco_tags.append(tag)		
	def clearEcoTags(self):
		self.eco_tags = []
	def removeGeoTag(self,tag):
		print("removing tag %s not implemented"%tag)
	def removeEcoTag(self,tag):
		print("removing tag %s not implemented"%tag)


# lifeform has phenotype traits and a genome		
class Lifeform:
	
	def __init__(self,parent,planet,traits):
		self.parent = parent
		self.id = ''
		if self.parent:
			self.id = self.parent.id + str(len(self.parent.children))
		self.planet = planet
		self.children = []		
		self.traits = traits
		self.genome = ''		
		self.genGenome()
		self.is_alive = True
		self.age = 0
		self.size = 0
		self.description = ''
		self.name = ''
		self.is_multicellular = False
		self.pheno_needs = {}
		self.pheno_supply = {}
		self.biome_reqs = []
		self.biome_tols = []
		self.eco_tags = []
		self.eco_niches = []
		self.biomes = []
		self.sumBiomeRequirements()
		self.findBiomes()
		self.sumEcoBiomeImpacts()	
		self.pheno_needs = self.sumPhenoNeeds(self.traits)
		self.pheno_supply = self.sumPhenoSupply(self.traits)
		self.genDescription()	
	
	def refresh(self):
		self.genGenome()
		self.pheno_needs = {}
		self.pheno_supply = {}
		self.biome_reqs = []
		self.biome_tols = []
		self.eco_tags = []
		self.eco_niches = []
		self.sumBiomeRequirements()
		self.findBiomes()
		self.sumEcoBiomeImpacts()	
		self.pheno_needs = self.sumPhenoNeeds(self.traits)
		self.pheno_supply = self.sumPhenoSupply(self.traits)
		self.genDescription()	
	
	def makeCopyForPlanet(self, planet):
		form = Lifeform(self,planet,self.traits)
		self.children.append(form)
		return form
		
	def kill(self):
		self.is_alive = False
		self.planet.removeLifeform(self)
		for b in self.biomes:
			b.removeLifeform(self)
	
	def genDescription(self):
		maxTraits = []
		maxStage = -1
		for t in self.traits:
			if t.org_type == '':
				continue
			if t.stage > maxStage:
				maxTraits = [t]
				maxStage = t.stage
			elif t.stage == maxStage:
				maxTraits.append(t)
		if len(maxTraits) == 0:
			self.description = 'organic detritus'	
			return
			
		self.description = random.choice(maxTraits).org_type
	
	
	def genGenome(self):
		for t in self.traits:
			self.genome += t.genome
	
	def sumBiomeRequirements(self):
	#	print("Establishing requirements for lifeform", self.genome)
		# for each trait in lifeform, check tags
		for trait in self.traits:
			# check if something in reqs is not in self.biome_reqs
			for b_req in trait.biome_reqs:
				if not b_req in self.biome_reqs:
					self.biome_reqs.append(b_req)
			for b_tol in trait.biome_tols:
				if not b_tol in self.biome_tols:
					self.biome_tols.append(b_tol)				
	
	def findBiomes(self):
	#	print("Finding biomes for lifeform",self.genome)
		# clear biomes list
		self.biomes = []		
		# iterate through self.planet.biomes
		for b in self.planet.biomes:
			# evaluate if b has the stuff in reqs_tags
			all_sat = True
			for req in self.biome_reqs:
				# check if req is in b.geo_tags or b.eco_tags 				
				if not (req in b.geo_tags or req in b.eco_tags):
		#			print(b.type,"fails requirement",req)
					all_sat = False
			if not all_sat:
				continue

			for h in b.hazards:
				if not h in self.biome_tols:
					all_sat = False									
			
			if all_sat:
				self.biomes.append(b) 
				b.addLifeform(self)
			#	print("Found biome:",b.type)
		if len(self.biomes) < 1:
		#	print("No biomes found. Killing lifeform",self.genome)
			self.planet.removeLifeform(self)
			self.is_alive = False
	
	def sumEcoBiomeImpacts(self):
		if not self.is_alive:
			return
		#print("Going through traits and decide on tags to add to biome")
		biome_tags = []
		eco_tags = []
		microsize = 0
		macrosize = 0
		for trait in self.traits:
		
			if 'multicellular' in trait.pheno_tags:
				self.is_multicellular = True

			if 'micro_size' in trait.pheno_tags:
				microsize += trait.pheno_tags['micro_size'] 	

			if 'size' in trait.pheno_tags:
				macrosize += trait.pheno_tags['size']
				
			for bt in trait.biome_impacts:
				if not bt in biome_tags:
					biome_tags.append(bt)
			for et in trait.eco_impacts:
				if not et in eco_tags:
					eco_tags.append(et)
		
		if self.is_multicellular:
			self.size = macrosize+100 
		else:
			self.size = microsize
		
		self.bio_impacts = biome_tags

		self.eco_niches = []
		# need some logic to derive ecosystem stuff
		if 'primary' in eco_tags:
			if not self.is_multicellular:
				self.eco_niches.append('micro_producer')
			else: # use logic about size here
				self.eco_niches.append('macro_producer')			
		
		if 'predator' in eco_tags:
			if not self.is_multicellular:
				self.eco_niches.append('micro_predator')
			else:
				self.eco_niches.append('macro_predator')		
		
		if 'grazer' in eco_tags:
			self.eco_niches.append('grazer')
			
		#TODO: need to add the new eco_niche stuff from traits
		# mushroom
		if 'mushroom' in eco_tags:
			self.eco_niches.append('mushroom')
		# motile
		if 'motile' in eco_tags and not self.is_multicellular:
			self.eco_niches.append('motile')		
		# root_symbiont
		if 'root_symbiont' in eco_tags:
			self.eco_niches.append('root_symbiont')		
		# sky_food
		if 'sky_food' in eco_tags:
			self.eco_niches.append('sky_food')
		# animal
		if 'animal' in eco_tags:
			self.eco_niches.append('animal')		
		# pollinator
		if 'pollinator' in eco_tags and self.size < 101:
			self.eco_niches.append('pollinator')		
		# leaves
		if 'leaves' in eco_tags and not 'needles' in eco_tags:
			self.eco_niches.append('leaves')		
		# seeds
		if 'seeds' in eco_tags:
			self.eco_niches.append('seeds')				
		# lignin
		if 'lignin' in eco_tags:
			self.eco_niches.append('lignin')				
		# tree
		if 'tree' in eco_tags:
			self.eco_niches.append('tree')				
		# endosperm
		if 'endosperm' in eco_tags:
			self.eco_niches.append('endosperm')				
		# flower
		if 'flower' in eco_tags:
			self.eco_niches.append('flower')	
		
		if 'citybuilder' in eco_tags:
			self.eco_niches.append('builder')
			self.planet.cityBuilder(self)
		
		if 'interplanetary' in eco_tags:
			self.eco_niches.append('interplanetary')
			self.planet.interplanetary(self)

		if 'interstellar' in eco_tags:
			self.eco_niches.append('interstellar')
			self.planet.interstellar(self)

		
	def addImpactsToBiomes(self):	
		if not self.is_alive:
			return		
	#	print("Adding eco and biome impact to biomes")	
		for b in self.biomes:
			for e in self.bio_impacts:
				if not e in b.geo_tags:
					b.addGeoTag(e)
			for e in self.eco_niches:
				if not e in b.eco_tags:
					b.addEcoTag(e)		
	
	def evolve(self, traits):
		self.age += 1
		if not self.is_alive:
			return False				
		
		if len(self.children) > 2 or random.random() > 2.0/(self.age+2):					
			return False						
			
		#print("Evolving ",self.genome)
		new_traits = copy.copy(self.traits)
		
		# 40%: go through traits list, make list of unnecessary ones
			# remove the trait, updating genome
		if random.random() < 0.4 and len(self.traits) > 2:
			red = self.findRedundantTrait(new_traits)
			if red:
				new_traits.remove(red)
			
			
		# go through traits list, make list of accessible ones
		# add trait, updating genome
		
		else:
			evolved_trait = self.selectAvailableTrait()
			
			if not evolved_trait:
	#		print("Evolution stalled")
				return False
				
			loc = random.randint(0,len(new_traits))	
			new_traits.insert(loc,evolved_trait)
				
		form = Lifeform(self,self.planet,new_traits) 		
		self.children.append( form )
		return form
	
	def sumPhenoSupply(self,traits):		
		pheno_supply = {}
		for t in traits:		
			for sup in t.pheno_tags:
				if sup not in pheno_supply:
					pheno_supply[sup] = t.pheno_tags[sup]
				else:
					if t.pheno_tags[sup] > 0:
						pheno_supply[sup] += t.pheno_tags[sup]
		return pheno_supply
	
	def sumPhenoNeeds(self,traits):
		pheno_needs = {'carbon':1,'energy':1}	
		for t in traits:	
			for dem in t.pheno_prereqs:
				if dem not in pheno_needs:
					pheno_needs[dem] = t.pheno_prereqs[dem]
				else:
					if t.pheno_prereqs[dem] > 0:
						pheno_needs[dem] += t.pheno_prereqs[dem]	
		return pheno_needs		
	
	def findAvailableTraits(self):
		candidates = []
						
		# go through all traits, get ones with pheno_prereq + pheno_demand satisfied
		for t in self.planet.traits:										
			already_has = False
			for has in self.traits:
				if t.name == has.name:
					already_has = True
			if already_has:
				continue
			all_sat = True
			for prereq in t.pheno_prereqs:
				if prereq not in self.pheno_supply:
					if not t.pheno_prereqs[prereq] == 0:
						all_sat = False
				elif prereq in self.pheno_needs:
					if t.pheno_prereqs[prereq] > 0 and t.pheno_prereqs[prereq]+self.pheno_needs[prereq] > self.pheno_supply[prereq]:
						all_sat = False
				else:
					if t.pheno_prereqs[prereq] > 0 and t.pheno_prereqs[prereq] > self.pheno_supply[prereq]:
						all_sat = False
					
			
			for nope in t.pheno_nopes:
				if nope in self.pheno_supply and not self.pheno_supply[nope] == 0:
					all_sat = False
			
			if all_sat:		
				candidates.append(t)

		isRV = False
		for t in self.traits:
			if t.name == 'radiovore':
				isRV = True
				break
		
						
		candidates2 = []
		# for each biome, get biome supply and check if candidates are happy	
		for b in self.biomes:
			for c in candidates:
				if c in candidates2:
					continue				
				#print("biome reqs for",c.name)
				if len(c.biome_reqs) == 0 :
					candidates2.append(c)
					continue
				all_sat = True	
				for req in c.biome_reqs:
					if not req in b.geo_tags and not req in b.eco_tags :
						all_sat = False
				if all_sat:
					candidates2.append(c)
		return candidates2
	
	def selectAvailableTrait(self):
		#print("Finding available traits")	
		
		candidates = self.findAvailableTraits()
		if len(candidates) > 0:
			minUsedTraits = []
			minUsed = 1000000
			for t in candidates:
				if t.num_per_planet < minUsed:
					minUsed = t.num_per_planet
					minUsedTraits = [t]
				elif t.num_per_planet == minUsed:
					minUsedTraits.append(t)
								
			trait = random.choice(minUsedTraits)
			#trait.num_per_planet += 1 # done more generally in planet.addLifeform()
			trait = copy.copy(trait)
			trait.genGenome()
			#print("new trait:",trait.name,trait.genome)
			return trait	
		
	def findRedundantTrait(self, traits):
		# collect the sum of the phenotypic supply/demand of the organism
		needs = self.sumPhenoNeeds(traits)
		supply = self.sumPhenoSupply(traits)
					
		# go through the traits again, selecting ones that don't contribute to a critical supply
		redundants = []	
		for t in traits:			
			r = True
			for pt in t.pheno_tags: 
				if pt in needs:
					if needs[pt] > -1 and supply[pt]-t.pheno_tags[pt] < needs[pt]:
						r = False
					elif needs[pt] < 0 and supply[pt] == -1:
						r = False
					elif needs[pt] == 0 and not supply[pt] == 0:
						r = False
					# otherwise, either traits is 0 or there's more than one of a -1 trait
			if r:
				redundants.append(t)
		
		# return one of the redundants
		if len(redundants) > 0:
			# get rid of one of the traits with lowest stage
			if True: #random.random() < .75:
				min_stage = 100
				minT = []
				for t in redundants:
					if t.stage < min_stage:
						minT = [t]
						min_stage = t.stage
					elif t.stage == min_stage:
						minT.append(t)
				return random.choice(minT)
			else:
				return random.choice(redundants)
		else:
			return False
		
# traits have requirements, add tags, have genome codes
class Trait:
	pheno_prereqs = {} # phenotype prerequisites 
	pheno_tags = {}	# phenotype features (to satisfy prereqs for other traits)
	pheno_nopes ={} # organism features needed to *lock* trait		 
	biome_reqs = []	# biome prerequisites
	biome_tols = [] 
	biome_impacts = [] # features that impact biome 
	eco_impacts = [] 
	name = ''
	num_per_planet = -1
	id = 0
	description = ''
	genome = ''
	
	def __init__(self, name, pheno_prereqs, pheno_nopes, pheno_tags, biome_reqs, biome_tols, biome_impacts, eco_impacts, num_per_planet, description, stage, org_type, id):
		self.name = name
		self.pheno_prereqs = pheno_prereqs
		self.pheno_nopes = pheno_nopes
		self.pheno_tags = pheno_tags		
		self.biome_reqs = biome_reqs
		self.biome_tols = biome_tols
		self.biome_impacts = biome_impacts
		self.eco_impacts = eco_impacts
		self.num_per_planet = num_per_planet
		self.description = description
		self.stage = stage
		self.org_type = org_type
		self.id = id
		
	# make a random genome for yourself
	def genGenome(self): 
		# start with a random start codon
		start = random.choice(['AGG','ATT','CGG','CTT'])
		# end with random stop codon
		end = random.choice(['AAG','AAT','CCG','CCT'])		
		
		g = start
		
		id = self.id
		b4 = ''
		# convert id to base 4 with 5 digits
		for i in range(0,5):
			foo = pow(4,5-i)
			if id >= 3*foo:
				b4 = 3
				id -= 3*foo
			elif id >= 2*foo:
				b4 = 2
				id -= 2*foo
			elif id >= foo:
				b4 = 2
				id -= foo
			else:
				b4 = 0
			# for each digit, pick a code
			if b4 == 0:
				g += (random.choice(['AGT','GAT','TAG','GTA','TGA','ATG','GGT']))
			elif b4 == 1:
				g += (random.choice(['ACT','CAT','TAC','CTA','TCA','ATC','AAC']))
			elif b4 == 2:
				g += (random.choice(['GCT','GTC','CTG','CGT','TCG','TGC','TTC']))			
			elif b4 == 3:
				g += (random.choice(['ACG','AGC','GAC','GCA','CAG','CGA','CCA']))
				
		g += (end)
		self.genome = g


class Scene:	
	def __init__(self):
		self.view = 'galaxy'
		self.view_object = ''
		self.scale = 50
		self.star_size = height/100
		self.time = 0
		self.biomedisp = ''
		self.ecodisp = ''
		self.filter_dead = 'False'
		
	def draw(self):
		self.time += 1
		if self.view == 'galaxy':
			self.viewGalaxy()
		elif self.view == 'star':
			self.viewStar()
		elif self.view == 'planet':
			self.viewPlanet()
		elif self.view == 'lifeform':
			self.viewLifeform()
			
	def click(self,cpos):
		if self.view == 'galaxy':
			self.clickGalaxy(cpos)
		elif self.view == 'star':
			self.clickStar(cpos)
		elif self.view == 'planet':
			self.clickPlanet(cpos)
		elif self.view == 'lifeform':
			self.clickLifeform(cpos)		
			
	def viewGalaxy(self):	
		colour = (220,220,140)
		text = font.render("Age (My): "+str(sim.age),1,colour)		
		textpos = text.get_rect(right=width-20, centery=25)
		screen.blit(text, textpos)		
		# draw a clickable circle for each star. Color it green if there's life.
		ns = len(sim.stars)
		for star in sim.stars:						
			self.drawStar(star)
		

	def clickGalaxy(self,cpos):
		# check if you clicked on a star. Switch view and target.
		
		for star in sim.stars:
			starpos = self.starPos2ScenePos(star.position)
			if math.dist(cpos,starpos) < self.star_size:
				self.view_object = star
				self.view = 'star'		
		
	def drawStar(self,star):
		if star.hasLife():
			colour = (150,250,150)
		else:
			colour = (150,150,150)
		pg.draw.circle(screen, colour, self.starPos2ScenePos(star.position), self.star_size) 

	def starPos2ScenePos(self,starpos):
		return (width*starpos[0]/self.scale+width/2,height*starpos[1]/self.scale+height/2)
		
	def scenePos2StarPos(self,scenepos):
		return ((scenepos[0]-width/2) / width*self.scale, (scenepos[1]-height/2) / height*self.scale)

	def viewStar(self):				
		# draw a circle for the "star"
		pg.draw.circle(screen, (250,240,230),(width/2,height/2),height/20)
		
		# draw a clickable circle for each planet. Color it green if there's life.

		for planet in self.view_object.planets:
			r = planet.distance * height/5 
			speed = 1.0/r
			pos = (width/2+r*math.cos((self.time + planet.id)*speed), height/2 + r*math.sin((self.time + planet.id)*speed))
			pcolour = (70,50+20*math.sin(r+10),60+20*math.cos(r+14))
			if len(planet.lifeforms) > 0:
				pcolour = (70,min(200,20+len(planet.lifeforms)*0.05),60)
			
			pg.draw.circle(screen,pcolour,pos,height/40)
			colour = (220,220,220)
			text = smallfont.render(planet.name,1,colour)		
			textpos = text.get_rect(centerx=pos[0], centery=pos[1]+height/30)
			screen.blit(text, textpos)	
	
	def clickStar(self,cpos):
		if math.dist(cpos,(width/2,height/2)) < height/20:
			self.view_object = ''
			self.view = 'galaxy'
			return
				
		r = 0
		r_per_planet = height/len(self.view_object.planets)*0.4
		d =  math.dist(cpos,(width/2,height/2))

		for planet in self.view_object.planets:			
			r = planet.distance * height/5 
			if r-height/40 < d < r+height/40:
				self.view_object = planet
				self.view = 'planet'
				return
			
			
	def viewPlanet(self):
		# draw a big planet circle
		
		planet = self.view_object

		pcolour = (70,50,60)
		if len(planet.lifeforms) > 0:
			pcolour = (70,min(200,20+len(planet.lifeforms)*0.05),60)
		pg.draw.circle(screen,pcolour,(width/2,height/2),height*0.4)
		colour = (140,220,140)
		text = font.render("Biomes:",1,colour)		
		textpos = text.get_rect(left=20, centery=25)
		screen.blit(text, textpos)		
		

		# describe the biomes
		num = 1
		for b in self.view_object.biomes:
			text = font.render(b.type,1,colour)		
			textpos = text.get_rect(left=30, centery=num*25+55)
			screen.blit(text, textpos)
			num += 1
		
			
		lifelist = []	
		if self.biomedisp == '':	
			lifelist = planet.lifeforms
		else:
			if self.ecodisp == '':
				lifelist = self.biomedisp.lifeforms
			else:
				for form in self.biomedisp.lifeforms:
					if self.ecodisp in form.eco_niches:
						lifelist.append(form)
		
		text = font.render("Significant life: "+str(len(lifelist)),1,colour)
		textpos = text.get_rect(left=20, centery=height-125)
		screen.blit(text, textpos)
		
		# list the biggest living species		
		if len(lifelist) == 0:
			text = font.render("None",1,colour)		
			textpos = text.get_rect(left=30, centery=height-100)
			screen.blit(text, textpos)				
					
		num  = 1		
		for l in lifelist[-4:]:
			text = font.render(l.description,1,colour)		
			textpos = text.get_rect(left=30, centery=height-125+num*25)
			screen.blit(text, textpos)
			num += 1
		
		if not self.biomedisp == '':		
			# display biome info	
			colour = (220,220,140)
			hcolour = (220,40,40)
			text = font.render(self.biomedisp.type,1,colour)		
			textpos = text.get_rect(right=width-30, centery=25)
			screen.blit(text, textpos)
			num = 1
			for b in self.biomedisp.geo_tags:
				if b in self.biomedisp.hazards:
					text = font.render(b,1,hcolour)
				else:
					text = font.render(b,1,colour)		
				textpos = text.get_rect(right=width-30, centery=num*25+55)
				screen.blit(text, textpos)
				num += 1
			colour = (140,220,140)
			for b in self.biomedisp.eco_tags:
				text = font.render(b,1,colour)		
				textpos = text.get_rect(right=width-30, centery=num*25+55)
				screen.blit(text, textpos)
				num += 1

		# display planet
		colour = (220,80,140)
		text = font.render('Planet '+ self.view_object.name,1,colour)		
		textpos = text.get_rect(centerx=width/2, centery=50)
		screen.blit(text, textpos)

		
		colour = (250,130,130)
		text = font.render("Asteroid strike",1,colour)		
		textpos = text.get_rect(centerx=width/2, centery=100)
		screen.blit(text, textpos)				
				
	def clickPlanet(self,cpos):
		if math.dist(cpos,(width/2,height/2)) < height/20:
			self.view_object = self.view_object.star
			self.view = 'star'
			self.biomedisp = ''
			self.ecodisp = ''
			return

		# check if asteroid strike
		if width/2-75 < cpos[0] < width/2+75 and 80 < cpos[1] < 120:
			sim.asteroid(self.view_object)
		
		# check if click on biome or species
		if 30 < cpos[0] < 200:
			num = 1		
			for b in self.view_object.biomes:
				centery = num*25+55
				if centery-5 < cpos[1] < centery+5:
					self.biomedisp = b
					self.ecodisp = ''
					return				
				num += 1
			
			lifelist = []	
			if self.biomedisp == '':	
				lifelist = self.view_object.lifeforms
			else:
				if self.ecodisp == '':
					lifelist = self.biomedisp.lifeforms
				else:
					for form in self.biomedisp.lifeforms:
						if self.ecodisp in form.eco_niches:
							lifelist.append(form)
				
			num = 1	
			for l in lifelist[-4:]:
				centery = height-125+num*25
				if centery-5 < cpos[1] < centery+5:
					self.view_object = l
					self.view = 'lifeform'
					print(l.id)
					print(l.genome)
					print("need:")
					for f in l.pheno_needs:
						print('  ',f,l.pheno_needs[f])
					print("supply:")
					for f in l.pheno_supply:
						print('  ',f,l.pheno_supply[f]) 
					print("available traits:")
					traits = l.findAvailableTraits()
					for t in traits:
						print('   ',t.name)
					return				
				num += 1
				
		# check if click on biome ecolist
		if not self.biomedisp == '':
			if width-200 < cpos[0] < width-30:
				num = 0
				for b in self.biomedisp.geo_tags:				
					num += 1
	
				for b in self.biomedisp.eco_tags:
					if num*25+20 < cpos[1] < num*25+90:
						self.ecodisp = b
						print("displaying",b)
						return
					num += 1
					
	def viewLifeform(self):
		# list characteristics
		colour = (220,220,140)
		text = font.render("Traits:",1,colour)		
		textpos = text.get_rect(left=20, centery=25)
		screen.blit(text, textpos)
		num = 1
		for t in self.view_object.traits:
			text = smallfont.render(t.name+': '+t.description+' | '+str(t.stage),1,colour)		
			textpos = text.get_rect(left=30, centery=25+num*15)
			screen.blit(text, textpos)
			num += 1			
		
		text = font.render("Available:",1,colour)		
		textpos = text.get_rect(right=width-20, centery=25)
		screen.blit(text, textpos)
		num = 1
		traits = self.view_object.findAvailableTraits()
		for t in traits:
			text = smallfont.render(t.name,1,colour)		
			textpos = text.get_rect(right=width-30, centery=25+num*15)
			screen.blit(text, textpos)
			num += 1			
		
		# all/alive toggle
		if self.filter_dead:
			text = smallfont.render("Showing only alive",1,colour)		
		else:
			text = smallfont.render("Showing all",1,colour)					
		textpos = text.get_rect(centerx=width/2, centery=height-125)
		screen.blit(text, textpos)
			
		# display genome
		genefont = pg.font.Font(None, 14)
		text = genefont.render(self.view_object.genome,1,(200,200,200))		
		textpos = text.get_rect(centerx=width/2, centery=height-25)
		screen.blit(text, textpos)
		
		# display planet
		colour = (220,220,140)
		text = font.render('Planet: '+str(self.view_object.planet.name),1,colour)		
		textpos = text.get_rect(centerx=width/2, centery=height-50)
		screen.blit(text, textpos)
		
		# list biomes
		text = font.render("Occupied biomes:",1,colour)		
		textpos = text.get_rect(left=20, centery=height-125)
		screen.blit(text, textpos)
		num = 1
		for t in self.view_object.biomes:
			text = font.render(t.type,1,colour)		
			textpos = text.get_rect(left=30, centery=height-125+num*25)
			screen.blit(text, textpos)
			num += 1
			
		# draw clickable circles for parent and children
		self.drawTreeAround()
		
	def findNearestLivingParent(self,form):
		if form.parent:
			if form.parent.is_alive:
				return form.parent
			else:
				return self.findNearestLivingParent(form.parent)
	
	def findNearestLivingDescendants(self,form):
		children = []
		if form.children:
			for child in form.children:
				if child.is_alive:
					children.append(child)
				else:
					children += self.findNearestLivingDescendants(child)
		return children
		
	def hasLivingDescendants(self,form):
		if form.children:
			hasLiving = False
			for child in form.children:
				if child.is_alive:
					return True
				if self.hasLivingDescendants(child):
					return True
		return False
		
	def drawTreeAround(self):
		lcolour = (20,100,20)
		ccolour = (10,130,30)
		tcolour = (240,240,240)
		form = self.view_object 
		# current organism
		colour = ccolour
		if not form.is_alive:
			colour = (80,80,80)
		pg.draw.circle(screen,colour,(width/2,height/2),120)
		colour = (30,30,30)
		text = font.render(form.description,1,tcolour)		
		textpos = text.get_rect(centerx=width/2, centery=height/2-20)
		screen.blit(text, textpos)
		text = font.render(form.id,1,tcolour)		
		textpos = text.get_rect(centerx=width/2, centery=height/2+20)
		screen.blit(text, textpos)

		# draw parent
		if form.parent:
			pg.draw.line(screen,lcolour,(width/2-120,height/2),(70,2*height/3),3)
			colour = ccolour	
			parent = form.parent
			if not parent.is_alive:
				if self.filter_dead:
					parent = self.findNearestLivingParent(parent)
					if not parent:
						parent = form.parent
						colour = (80,80,80)
				else:
					colour = (80,80,80)
			pg.draw.circle(screen,colour,(70,2*height/3),50)
			text = smallfont.render(parent.description,1,tcolour)		
			textpos = text.get_rect(centerx=70, centery=2*height/3)
			screen.blit(text, textpos)
		
		# draw children:
		children = []
		if self.filter_dead:
			for c in form.children:
				if c.is_alive or self.hasLivingDescendants(c):
					children.append(c)
		else:
			children = form.children
		num_children = len(children)
			
		if(num_children < 1):
			return
			
		vspace = height / 2
		vs_per_child = vspace/num_children
		num = 1
		for c in children:
			pg.draw.line( screen, lcolour, (width/2+120,height/2), (width-70,height/4+num*vs_per_child), 3)
			colour = ccolour	
			if not c.is_alive:
				colour = (80,80,80)
			pg.draw.circle(screen,colour,(width-70,height/4+num*vs_per_child),50)
			colour = (80,80,80)
			text = smallfont.render(c.description,1,tcolour)		
			textpos = text.get_rect(centerx=width-70, centery=height/4+num*vs_per_child+20)
			screen.blit(text, textpos)
			text = smallfont.render(c.id,1,tcolour)		
			textpos = text.get_rect(centerx=width-70, centery=height/4+num*vs_per_child-20)
			screen.blit(text, textpos)

			num += 1
		
	
	def clickTreeAround(self,cpos):
		form = self.view_object
		if form.parent:
			if math.dist(cpos,(70,2*height/3)) < 50:
				parent = form.parent
				if not parent.is_alive:
					if self.filter_dead:
						parent = self.findNearestLivingParent(parent)
						if not parent:
							parent = form.parent
				self.view_object = parent
				print(form.parent.id)				
				print(form.parent.genome)
				print("need:")
				for f in form.parent.pheno_needs:
					print('  ',f,form.parent.pheno_needs[f])
				print("supply:")
				for f in form.parent.pheno_supply:
					print('  ',f,form.parent.pheno_supply[f])
				print("available traits:")
				traits = form.parent.findAvailableTraits()
				for t in traits:
					print('   ',t.name)
				return True
				
		children = []
		if self.filter_dead:
			for c in form.children:
				if c.is_alive or self.hasLivingDescendants(c):
					children.append(c)
		else:
			children = form.children
			
		num_children = len(children)
			
		if(num_children < 1):
			return False
			
		vspace = height / 2
		vs_per_child = vspace/num_children
		num = 1
		for c in children:
			if math.dist(cpos,(width-70,height/4+num*vs_per_child)) < 50:
				self.view_object = c
				print(c.id)
				print(c.genome)
				print("need:")
				for f in c.pheno_needs:
					print('  ',f,c.pheno_needs[f])
				print("supply:")
				for f in c.pheno_supply:
					print('  ',f,c.pheno_supply[f]) 
				print("available traits:")
				traits = c.findAvailableTraits()
				for t in traits:
					print('   ',t.name)				
				return True
			pg.draw.line(screen,(200,200,200),(width/2+120,height/2),(width-70,height/4+num*vs_per_child),3)
			pg.draw.circle(screen,(30,180,30),(width-70,height/4+num*vs_per_child),50)
			colour = (0,0,0)
			text = smallfont.render(c.description,1,colour)		
			textpos = text.get_rect(centerx=width-70, centery=height/4+num*vs_per_child)
			screen.blit(text, textpos)
			num += 1
		return False
	
	def clickLifeform(self,cpos):
		if self.clickTreeAround(cpos):
			return
		
		# all/alive toggle
		if width/2-50 < cpos[0] < width/2+50:
			if height-100 > cpos[1] > height-150:
				self.filter_dead = not self.filter_dead
				return
		
		# check to see if you clicked on an available trait
		if width-120 < cpos[0] < width-20:
			num = 1
			traits = self.view_object.findAvailableTraits()
			for t in traits:
				centery = 25+num*15
				if centery-5 < cpos[1] < centery+5:
					print("ADD TRAIT",t.name)
					trait = copy.copy(t)
					trait.genGenome()
					self.view_object.traits.append(trait)
					self.view_object.refresh()
					return	
				num += 1
		
		# check to see if you clicked on an existing trait
		if 30 < cpos[0] < 200:
			num = 1
			traits = self.view_object.traits
			for t in traits:
				centery = 25+num*15
				if centery-5 < cpos[1] < centery+5:
					print("REMOVE TRAIT",t.name)
					self.view_object.traits.remove(t)
					self.view_object.refresh()
					return	
				num += 1
		
		if math.dist(cpos,(width/2,height/2)) < 0.3*width:	
			self.view = 'planet'
			self.view_object = self.view_object.planet			
			return
	

## ------------------
# Program starts

def main():
	
	pg.init()
	global width, height, size, screen, background, font, smallfont, clock, sim, scene
	size = width, height = 800, 600
	black = 0,0,0

	screen = pg.display.set_mode(size)

	background = pg.Surface(screen.get_size())
	background = background.convert()
	background.fill(black)

	font = pg.font.Font(None, 36)
	smallfont = pg.font.Font(None, 16)
	text = font.render("Panspermia",1,(200,200,10))
	textpos = text.get_rect(centerx=background.get_width() / 2, centery=20)
	background.blit(text, textpos)

	clock = pg.time.Clock()

	drawCircle = False
	cpos = 0,0
	
	# initialise the sim 
	sim = Simulation(40,3)	#(num stars, num planets per star)
	scene = Scene()
	going = True
	while going:
		clock.tick(60)

		# Handle Input Events
		for event in pg.event.get():
			if event.type == pg.QUIT:
				going = False
			elif event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				going = False
			elif event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
				print("****")
				sim.running = not sim.running
			elif event.type == pg.KEYDOWN and event.key == pg.K_s:
				print("****")
				sim.iterate()
			elif event.type == pg.MOUSEBUTTONDOWN:
				cpos = pg.mouse.get_pos()	
				scene.click(cpos)
			elif event.type == pg.MOUSEBUTTONUP:
				drawCircle = False
		
		if sim.running:
			sim.iterate()
			
		screen.blit(background, (0,0))
		scene.draw()
	
		pg.display.flip()
	
	pg.quit()
	
if __name__ == '__main__':
    main()	