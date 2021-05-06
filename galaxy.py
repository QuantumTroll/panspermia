import random
import copy
import math

from lifeform import Lifeform
from lifeform import Trait

# stars just have a list of planets
class Star:

	def __init__(self,sim,num_planets,pos,params,traits):
		self.sim = sim
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
			self.star.sim.asteroid(self)
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
