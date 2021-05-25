#!/usr/bin/env python3

import sys
import pygame as pg
import random
import copy
import math

import traits
from lifeform import Lifeform
from lifeform import Trait
from galaxy import Star, Planet, Biome

### 
# to do list
#
#
#
#  citybuilding mass extinction, eco-disasters when migrating
#  
#  cities should have fewer species. make city into a hazard, introduce city-tolerance into traits – eg social brains, something like "quick-growing roots" (for weeds), stuff that make plants good food (root energy store, endosperm), fast reproduction (for small creatures, like rats and cockroaches)
#
#  soil: biome and traits (for plants, animals, and microbes)
#  toxic: traits
#  more traits: plant stuff, e.g. lichens in frozen biomes
#  more traits: camouflage and looks, e.g. mandibles
#   traits: stuff in caverns — how do I get a carbon source in there?

#  interplanetary/interstellar migration
#    cause mass extinction on destination planet
#    if interstellar meets interstellar (happens rarely, when interplanetary civ happens to send migrations to same planet), do a huge nuclear war.

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
		
		self.migrants = []		
		
		print("Creating stars & planets")
		# create stars with planets
		for i in range(0,num_stars):
			r = i*20/num_stars + random.randint(1,6)
			position = (r*math.sin(i*.5),r*math.cos(i*.5))
			num = num_planets_per_star + random.randint(-2,2)
			self.stars.append( Star(self,num, position,(r,i), self.traits ))
		
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
			name = t['name']
			pheno_prereqs = t.get('pheno_prereqs',{})
			pheno_reqs = t.get('pheno_reqs', {})			
			pheno_nopes = t.get('pheno_nopes', {})	
			pheno_tags = t.get('pheno_tags', {})
			biome_reqs = t.get('biome_reqs', [])
			biome_prereqs = t.get('biome_reqs', [])			
			biome_tols = t.get('biome_tols', [])
			biome_impacts = t.get('biome_impacts', [])
			eco_impacts = t.get('eco_impacts', [])
			description = t.get('description', '')
			stage = t['stage']
			org_type = t.get('org_type', '')
			trait = Trait(name, pheno_prereqs, pheno_reqs, pheno_nopes, pheno_tags, biome_reqs, biome_prereqs, biome_tols, biome_impacts, eco_impacts, description, stage, org_type, id)
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
		
		self.migrations()
		
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

	def addToCaravan(self,caravan,migrant,biome,eco_reqs,geo_reqs):
		caravan.append(migrant)
	#	print("added",migrant.description,"to caravan")
		new_ecos = []
		for req in migrant.biome_reqs:
			# decide if a tag is an eco_tag or not
			if req in biome.geo_tags and not req in geo_reqs:
#				print("  new geo req",req)
				geo_reqs.append(req)
			elif req in biome.eco_tags and not req in eco_reqs:
				new_ecos.append(req)
			#else:
			#	print("Warning: requirement",req," not found in",biome.type)
				
		for req in new_ecos:
	#		print("    adding eco requirement",req)
			eco_reqs.append(req)
			# find a random species in biome that satisfies the requirement
			candidates = []
			for form in biome.lifeforms:
				if req in form.eco_niches:
					candidates.append(form)
			num_new = random.randint(1,min(4,len(candidates)))
			for i in range(num_new):
				new_member = random.choice(candidates) 
				# avoid picking existing caravan members. 
				if new_member in caravan:
					continue
				self.addToCaravan(caravan,new_member,biome,eco_reqs,geo_reqs)

	def migrations(self):
		if not len(self.migrants) > 0:
			return
		print("Performing migration")
		
		for migrant in self.migrants:
			if not migrant.is_alive or migrant.has_migrated:
				continue
			
			migrant.has_migrated = True
			

			# identify terraforming requirements (atmospheric + geological, e.g. city)
			# also identify necessary ecological niches
			# to select companion species
			eco_reqs = []
			geo_reqs = []
			caravan = []			
			biome = random.choice(migrant.biomes)
			print("migration from",biome.type," lead by",migrant.id)					
			self.addToCaravan(caravan,migrant,biome,eco_reqs,geo_reqs)								
			
			print("   migrating",len(caravan),"species")
			caravan.reverse() # so that we add the last species first
			
			# choose planets to migrate to			
			target_planets = []			
			if 'stellar' in migrant.description:
				print("interstellar migration from",migrant.planet.name)				
				# find nearby stars and seed life
				starPos  = migrant.planet.star.position
				spread_radius = 25
				for s in self.stars:
					if s == migrant.planet.star:
							continue
					# move to like 25% of available systems?
					if random.random() < 0.25 and math.dist(starPos,s.position) < spread_radius:						
						for p in s.planets:
							has_right_biome = False
							biometype = biome.type.split()[0]
							for b in p.biomes:
								if biometype in b.type and not 'interstellar' in b.eco_tags:
									has_right_biome = True
							if has_right_biome:								
								target_planets.append(p)
							
			else:
				print("   interplanetary migration from",migrant.planet.name)
				for p in migrant.planet.star.planets:
					if p == migrant.planet:
						continue
					has_right_biome = False
					has_interplanetary = False
					biometype = biome.type.split()[0]
					for b in p.biomes:
						if biometype in b.type:
							has_right_biome = True
						if 'interplanetary' in b.eco_tags:
							has_interplanetary = True
					if has_right_biome and not has_interplanetary:								
						target_planets.append(p)
		
			for p in target_planets:
				print("   migrating to",p.name)
			#	print("    terraforming...")
				
				# this is dumb. TODO: check the entire planet for interplanetaries
				for b in p.biomes:
					biometype = biome.type.split()[0]
					if biometype in b.type and not 'interplanetary' in b.eco_tags:
						the_biome = b
				
				target_biome = Biome(p,the_biome.type+' city',the_biome.atmo,the_biome.geo_tags+[],the_biome.eco_tags+[],the_biome.hazards+[])
				
				p.biomes.append(target_biome)
				
				for g in geo_reqs:
					if not g in target_biome.geo_tags:
						target_biome.addGeoTag(g)
				#		print("     Added",g,"to ",target_biome.type)


				for l in caravan:
			#		print("  migrating",l.description)
					form = l.makeCopyForPlanet(p)
					if l == migrant:
						form.member_of = migrant
					
					form.has_migrated = True		
								
					p.addLifeform(form)
					form.addImpactsToBiomes()
			#		print("  form is alive?",form.is_alive)
			
		self.migrants = []

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
		self.planet_life_scroll = 0
		self.planet_biome_scroll = 0
		self.lifeform_traits_scroll = 0
	
		
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
		
	
	def wheel(self,cpos,x):
		if self.view == 'planet':
			self.wheelPlanet(cpos,x)
		elif self.view == 'lifeform':
			self.wheelLifeform(cpos,x)
			
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
		scroll = min(len(lifelist),self.planet_life_scroll)
		for l in lifelist[-4-scroll:]:
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
			geoscroll = min(len(self.biomedisp.geo_tags),self.planet_biome_scroll)			
			for b in self.biomedisp.geo_tags[-8-geoscroll:]:
				if b in self.biomedisp.hazards:
					text = font.render(b,1,hcolour)
				else:
					text = font.render(b,1,colour)		
				textpos = text.get_rect(right=width-30, centery=num*25+55)
				screen.blit(text, textpos)
				num += 1
			colour = (140,220,140) 
			ecoscroll = min(len(self.biomedisp.eco_tags), self.planet_biome_scroll-geoscroll)
			for b in self.biomedisp.eco_tags[-8-ecoscroll:]:
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
			self.planet_life_scroll = 0			
			self.planet_biome_scroll = 0
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
			scroll = min(len(lifelist),self.planet_life_scroll)
			for l in lifelist[-4-scroll:]:
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
				geoscroll = min(len(self.biomedisp.geo_tags),self.planet_biome_scroll)			
				for b in self.biomedisp.geo_tags[-8-geoscroll:]:
					num += 1
	
				ecoscroll = min(len(self.biomedisp.eco_tags), self.planet_biome_scroll-geoscroll)
				for b in self.biomedisp.eco_tags[-8-ecoscroll:]:
					if num*25+20 < cpos[1] < num*25+90:
						self.ecodisp = b
						print("displaying",b)
						return
					num += 1
	
	def wheelPlanet(self,cpos,x):
		# check if scroll on species lists
		if 30 < cpos[0] < 200:
			if height-115 < cpos[1] < height:
				print("scroll lifeforms",x)		
				self.planet_life_scroll += x
				if self.planet_life_scroll < 0:
					self.planet_life_scroll = 0
		# check if scroll on biome features
		if width-200 < cpos[0] < width-30:
			self.planet_biome_scroll += x
			if self.planet_biome_scroll < 0:
				self.planet_biome_scroll = 0
					
	def viewLifeform(self):
		# list characteristics
		colour = (220,220,140)
		text = font.render("Traits:",1,colour)		
		textpos = text.get_rect(left=20, centery=25)
		screen.blit(text, textpos)
		num = 1
		scroll = min(len(self.view_object.traits),self.lifeform_traits_scroll)
		for t in self.view_object.traits[-10-scroll:]:
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
		
	def wheelLifeform(self,cpos,x):
		# check if scroll on traits lists
		if 30 < cpos[0] < 200:
			self.lifeform_traits_scroll += x
			if self.lifeform_traits_scroll < 0:
				self.lifeform_traits_scroll = 0
		
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
			scroll = min(len(traits),self.lifeform_traits_scroll)
			for t in traits[-10-scroll:]:
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
			self.lifeform_traits_scroll	= 0	
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
			elif event.type == pg.MOUSEWHEEL:
				scene.wheel(pg.mouse.get_pos(),event.y)
			elif event.type == pg.KEYDOWN and event.key == pg.K_UP:
				scene.wheel(pg.mouse.get_pos(),+1)
			elif event.type == pg.KEYDOWN and event.key == pg.K_DOWN:
				scene.wheel(pg.mouse.get_pos(),-1)								
		
		if sim.running:
			sim.iterate()
			
		screen.blit(background, (0,0))
		scene.draw()
	
		pg.display.flip()
	
	pg.quit()
	
if __name__ == '__main__':
    main()	
