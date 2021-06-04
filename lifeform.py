
import random
import copy
import math

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
		self.member_of = None
		self.members = []
		self.has_migrated = False
		self.is_multicellular = False
		self.is_jealous = False
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
	
	def dict(self):
		dict = {}
		dict['id'] = self.id
		dict['traits'] = []
		for t in self.traits:
			dict['traits'].append(t.dict())
		dict['genome'] = self.genome
		dict['age'] = self.age
		dict['size'] = self.size
		dict['description'] = self.description
		#self.name = ''
		if self.member_of:
			dict['member_of'] = self.member_of.id
		else:
			dict['member_of'] = ''	
		dict['members'] = []
		for m in self.members:
			dict['members'].append(m.id)
		dict['has_migrated'] = self.has_migrated
		dict['is_multicellular'] = self.is_multicellular
		dict['is_jealous'] = self.is_jealous
		dict['pheno_needs'] = self.pheno_needs
		dict['pheno_supply'] = self.pheno_supply
		dict['biome_reqs'] = self.biome_reqs
		dict['biome_tols'] = self.biome_tols
		dict['eco_tags'] = self.eco_tags
		dict['eco_niches'] = self.eco_niches
		dict['pheno_needs'] = self.pheno_needs
		dict['pheno_supply'] = self.pheno_supply		
		
		dict['children'] = []
		for c in self.children:
			dict['children'].append(c.dict())
		return dict
	
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
		self.caravan = []
	
	def makeCopyForPlanet(self, planet):
		form = Lifeform(self,planet,self.traits)
		self.children.append(form)
		return form
		
	def kill(self):
		self.is_alive = False
		self.planet.removeLifeform(self)
		for b in self.biomes:
			b.removeLifeform(self)
		
		for form in self.members:
			form.kill()
	
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
					
		if 'interplanetary' in self.description:
			print(">",self.description,"needs:") 			
			for req in self.biome_reqs:
				print(req)
	def findBiomes(self):
		# clear biomes list
		self.biomes = []		
		# iterate through self.planet.biomes
		for b in self.planet.biomes:
				
			# evaluate if b has the stuff in reqs_tags
			all_sat = True
			for req in self.biome_reqs:
				# check if req is in b.geo_tags or b.eco_tags 				
				if not (req in b.geo_tags or req in b.eco_tags):
					#if 'interplanetary' in self.description:
					#	print(">>",req,"not found in",b.type)
					all_sat = False
			if not all_sat:
				continue
				
			for h in b.hazards:
				if not h in self.biome_tols:
					#if 'interplanetary' in self.description:
					#	print(">>",h,"not tolerated in",b.type)
					all_sat = False		
					
			if all_sat:
				self.biomes.append(b) 
				b.addLifeform(self)
			
		if len(self.biomes) < 1:
			#if 'interplanetary' in self.description:
			#	print("No biomes found. Killing lifeform",self.description)
		
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
		micropropel = 0
		macropropel = 0
		for trait in self.traits:
		
			if 'multicellular' in trait.pheno_tags:
				self.is_multicellular = True

			if 'micro_size' in trait.pheno_tags:
				microsize += trait.pheno_tags['micro_size'] 

			if 'micro_size' in trait.pheno_reqs:
				microsize -= trait.pheno_reqs['micro_size'] 
					
			if 'size' in trait.pheno_tags:
				macrosize += trait.pheno_tags['size']

			if 'size' in trait.pheno_reqs:
				macrosize += trait.pheno_reqs['size']
				
			if 'micro_propel' in trait.pheno_tags:
				micropropel += trait.pheno_tags['micro_propel'] 

			if 'micro_propel' in trait.pheno_reqs:
				micropropel -= trait.pheno_reqs['micro_propel'] 
					
			if 'propel' in trait.pheno_tags:
				macropropel += trait.pheno_tags['propel']

			if 'propel' in trait.pheno_reqs:
				macropropel += trait.pheno_reqs['propel']
				
				
			for bt in trait.biome_impacts:
				if not bt in biome_tags:
					biome_tags.append(bt)
			for et in trait.eco_impacts:
				if not et in eco_tags:
					eco_tags.append(et)
		
		if self.is_multicellular:
			self.size = macrosize+100 
			self.propel = macropropel
		else:
			self.size = microsize
			self.propel = micropropel
		
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
				if self.propel > 0:
					self.eco_niches.append('macro_predator')	
				else:
					self.eco_niches.append('trap_predator')				
		
		if 'grazer' in eco_tags:
			if self.propel > 0:
				self.eco_niches.append('grazer')
			else:  #this did happen!
				self.eco_niches.append('parasitic growth')
			
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
			self.is_jealous = True
			self.caravan = []
			for b in self.biomes:
				eco_reqs = []
				geo_reqs = []
				self.addToCaravan(self.caravan,self,b,eco_reqs,geo_reqs)
			cities = self.planet.cityBuilder(self)
		
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
		
		if 'interstellar' in self.description:
			return False
		
		if 'interplanetary' in self.description and not 'interstellar' in self.description:
			if self.age > 1:
				self.has_migrated = False
				# find interstellar trait
				for t in self.planet.traits:
					if t.name == 'interstellar':
						interstellar = copy.copy(t)
						loc = random.randint(0,len(self.traits))
						self.traits.insert(loc,interstellar)
						self.refresh()		
		
			if self.has_migrated:
				return False
		
		
		if (len(self.children) > 2) or random.random() > 2.0/(self.age+2):					
			return False						
		
		

			
		#print("Evolving ",self.genome)
		new_traits = copy.copy(self.traits)
		
		# 25%: go through traits list, make list of unnecessary ones
			# remove the trait, updating genome
		if random.random() < 0.25 and len(self.traits) > 2:
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
			for dem in t.pheno_reqs:
				if dem not in pheno_needs:
					pheno_needs[dem] = t.pheno_reqs[dem]
				else:
					if t.pheno_reqs[dem] > 0:
						pheno_needs[dem] += t.pheno_reqs[dem]	
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
			# in Python 3.9, there's a | operand for this:
			requires = {**t.pheno_prereqs,**t.pheno_reqs}
			for prereq in requires:
				if prereq not in self.pheno_supply:
					if not requires[prereq] == 0:
						all_sat = False
				elif prereq in self.pheno_needs:
					if requires[prereq] > 0 and requires[prereq]+self.pheno_needs[prereq] > self.pheno_supply[prereq]:
						all_sat = False
				else:
					if requires[prereq] > 0 and requires[prereq] > self.pheno_supply[prereq]:
						all_sat = False
					
			
			for nope in t.pheno_nopes:
				if nope in self.pheno_supply and not self.pheno_supply[nope] == 0:
					if self.pheno_supply[nope] >= t.pheno_nopes[nope]:
						all_sat = False
			
			if all_sat:		
				candidates.append(t)

						
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
				for req in c.biome_reqs+c.biome_prereqs:
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
		
	def addToCaravan(self,caravan,migrant,biome,eco_reqs,geo_reqs):
		caravan.append(migrant)
	#	print("--added",migrant.description,"to caravan in",biome.type,"on",biome.planet.name)
		new_ecos = []
		old_ecos = []
		for req in migrant.biome_reqs:
			# decide if a tag is an eco_tag or not
			if req in biome.geo_tags and not req in geo_reqs:
		#		print("  new geo req",req)
				geo_reqs.append(req)
			elif req in biome.eco_tags:# and not req in eco_reqs:
				if not req in eco_reqs:
					new_ecos.append(req)
				else:
					old_ecos.append(req)
			#else:
			#	print("Warning: requirement",req," not found in",biome.type)
				
		for req in new_ecos:
		#	print("    adding eco requirement",req)
			eco_reqs.append(req)
			# find a random species in biome that satisfies the requirement
			candidates = []
		#	print("       checking",len(biome.lifeforms))
			for form in biome.lifeforms:
				if req in form.eco_niches:
					candidates.append(form)
					#print("----new candidate:",form.description)
			if len(candidates) < 1:
				return
			
			num_new = random.randint(min(3,len(candidates)),min(8,len(candidates)))
		#	print("----taking",num_new,"new candidates to meet req",req)			
			for i in range(num_new):
				new_member = random.choice(candidates) 
				# avoid picking existing caravan members. 
				if new_member in caravan:
					continue
				self.addToCaravan(caravan,new_member,biome,eco_reqs,geo_reqs)
		
		for req in old_ecos:
			# find a random species in biome that satisfies the requirement
			candidates = []
		#	print("       checking",len(biome.lifeforms))
			for form in biome.lifeforms:
				if req in form.eco_niches:
					candidates.append(form)
					#print("----new candidate:",form.description)
			if len(candidates) < 1:
				return
		#	print("---- taking one of",len(candidates),"new candidates to meet req",req)
			
			new_member = random.choice(candidates) 
			# avoid picking existing caravan members. 
			if new_member in caravan:
				caravan.append(caravan.pop(caravan.index(new_member)))
				continue
			self.addToCaravan(caravan,new_member,biome,eco_reqs,geo_reqs)	
		
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
	
	def __init__(self, name, pheno_prereqs, pheno_reqs, pheno_nopes, pheno_tags, biome_reqs, biome_prereqs, biome_tols, biome_impacts, eco_impacts, description, stage, org_type, id):
		self.name = name
		self.pheno_prereqs = pheno_prereqs
		self.pheno_reqs = pheno_reqs
		self.pheno_nopes = pheno_nopes
		self.pheno_tags = pheno_tags		
		self.biome_reqs = biome_reqs
		self.biome_prereqs = biome_prereqs
		self.biome_tols = biome_tols
		self.biome_impacts = biome_impacts
		self.eco_impacts = eco_impacts
		self.num_per_planet = 0
		self.description = description
		self.stage = stage
		self.org_type = org_type
		self.id = id
		
	def dict(self):
		dict = {}
		dict['name'] = self.name
		dict['pheno_prereqs'] = self.pheno_prereqs
		dict['pheno_nopes'] = self.pheno_nopes
		dict['pheno_tags'] = self.pheno_tags
		dict['biome_reqs'] = self.biome_reqs
		dict['biome_prereqs'] = self.biome_prereqs
		dict['biome_tols'] = self.biome_tols
		dict['biome_impacts'] = self.biome_impacts
		dict['eco_impacts'] = self.eco_impacts
		dict['num_per_planet'] = self.num_per_planet
		dict['description'] = self.description
		dict['stage'] = self.stage
		dict['org_type'] = self.org_type
		dict['id'] = self.id
		return dict
						
								
	
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

