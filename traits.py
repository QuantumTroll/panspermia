# Traits module

def micro_fundamentals(traits):
	
	t = {}
	t['name'] = 'radiation_tolerance'
	t['pheno_reqs'] = {'energy':1}			# organism features needed to unlock trait
	t['pheno_nopes'] = {'multicellular':-1}			# organism features needed to *lock* trait		
	t['pheno_tags'] = {'rad_tol':-1} 			# traits contributes organism feature
	t['biome_tols'] = ['radiation']			# tag that forbids a biome
	t['description'] = "survives in hard radiation"
	t['stage'] = 1						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'radiovore'
	t['pheno_reqs'] = {'rad_tol':-1}			# organism features needed to unlock trait
	t['pheno_tags'] = {'energy':4,'foo':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['radiation']			# tag needed in biome
	t['description'] = "captures hard radiation"
	t['stage'] = 1						# advancement level of trait
	t['org_type'] = 'radiovore' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'micro_eat_sludge_2'
	t['pheno_reqs'] = {}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'multicellular':-1,'foo':-1,'predate':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'energy':1,'carbon':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['sludge']			# tag needed in biome
	t['biome_impacts'] = ['methane']		# trait adds tags to biome
	t['eco_impacts'] = ['primary']			# tags used to interpret ecosystem niche
	t['description'] = "feeds upon simple organic compounds"
	t['stage'] = 0						# advancement level of trait
	t['org_type'] = "basic microorganism" 			# species descriptor, if any		
	traits.append(t)
	t = {}
	t['name'] = 'micro_eat_sludge_1'
	t['pheno_reqs'] = {}
	t['pheno_nopes'] = {'multicellular':-1,'foo':-1,'predate':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'energy':1,'carbon':1} 
	t['biome_reqs'] = ['sludge']
	t['biome_impacts'] = ['CO2']
	t['eco_impacts'] = ['primary']
	t['description'] = "feeds upon simple organic compounds"
	t['stage'] = 0						# advancement level of trait
	t['org_type'] = "basic microorganism" 			# species descriptor, if any		
	traits.append(t)
	t = {}
	t['name'] = 'micro_breathe_sulfate'
	t['pheno_reqs'] = {}
	t['pheno_nopes'] = {'multicellular':-1,'foo':-1,'predate':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'energy':1} 
	t['biome_reqs'] = ['sulfate']
	t['biome_impacts'] = ['H2S']
	t['eco_impacts'] = ['primary']
	t['description'] = "uses sulfate respiration"
	t['stage'] = 0						# advancement level of trait
	t['org_type'] = "basic microorganism" 			# species descriptor, if any		
	traits.append(t)
	t = {}
	t['name'] = 'micro_size_1'
	t['pheno_reqs'] = {'carbon':1}
	t['pheno_nopes'] = {'multicellular':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_size':1} 
	t['stage'] = 0						# advancement level of trait					
	traits.append(t)
	t = {}
	t['name'] = 'micro_size_2'
	t['pheno_reqs'] = {'carbon':1}
	t['pheno_nopes'] = {'multicellular':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_size':1} 
	t['stage'] = 0						# advancement level of trait		
	traits.append(t)
	t = {}
	t['name'] = 'photosynthesis_1'
	t['pheno_prereqs'] = {'micro_size':1}
	t['pheno_nopes'] = {'animalia':-1,'predate':-1}
	t['pheno_tags'] = {'energy':2,'carbon':3,'foo':-1,'plant':-1,'micro_size':1} 
	t['biome_reqs'] = ['CO2','light']
	t['biome_impacts'] = ['O2']
	t['eco_impacts'] = ['primary']
	t['description'] = "captures sun's energy into organic compounds"
	t['stage'] = 2						# advancement level of trait
	t['org_type'] = 'cyanobacterium' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'micro_size_3'
	t['pheno_reqs'] = {'carbon':1}
	t['pheno_nopes'] = {'multicellular':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_size':1} 
	t['stage'] = 0						# advancement level of trait			
	traits.append(t)
	t = {}
	t['name'] = 'eukaryote'
	t['pheno_reqs'] = {'energy':2}
	t['pheno_tags'] = {'multi_prereq':1} 
	t['description'] = "has a cell nucleus"	
	t['stage'] = 2						# advancement level of trait
	t['org_type'] = 'complex microorganism' 			# species descriptor, if any	
	traits.append(t)
	t = {}
	t['name'] = 'mitochondria'
	t['pheno_reqs'] = {'carbon':1}
	t['pheno_tags'] = {'multi_prereq':1,'energy':2} 
	t['biome_reqs'] = ['O2']	
	t['biome_impacts'] = ['CO2']			# trait adds tags to biome
	t['description'] = "has mitochondria that perform respiration"		
	t['stage'] = 2						# advancement level of trait
	t['org_type'] = 'complex microorganism' 			# species descriptor, if any	
	traits.append(t)


def micro_predator(traits):
	t = {}	
	t['name'] = 'cilia'
	t['pheno_reqs'] = {'energy':1,}
	t['pheno_nopes'] = {'multicellular':-1,'micro_propel':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_propel':1} 		
	t['biome_prereqs'] = ['water']
	t['eco_impacts'] = ['motile']
	t['description'] = "moves using cilia"		
	t['stage'] = 1						# advancement level of trait
	t['org_type'] = 'simple motile microorganism' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'flagellum'
	t['pheno_reqs'] = {'energy':1}
	t['pheno_nopes'] = {'multicellular':-1,'micro_propel':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_propel':1,'flagellum':1} 
	t['biome_prereqs'] = ['water']
	t['eco_impacts'] = ['motile']
	t['description'] = "moves using flagellum"
	t['stage'] = 1						# advancement level of trait
	t['org_type'] = 'simple motile microorganism' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'flagellum-2'
	t['pheno_reqs'] = {'energy':1,'flagellum':1}
	t['pheno_nopes'] = {'multicellular':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'micro_propel':1} 
	t['eco_impacts'] = ['motile']
	t['description'] = "has a rotating flagellum"		
	t['stage'] = 1						# advancement level of trait
	t['org_type'] = 'simple motile microorganism' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'micro_predator'
	t['pheno_reqs'] = {'micro_propel':-1}
	t['pheno_nopes'] = {'multicellular':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'predate':-1,'energy':3,'carbon':4} 
	t['biome_reqs'] = ['micro_producer']
	t['eco_impacts'] = ['micro_predator']
	t['description'] = "consumes microorganisms"	
	t['stage'] = 1						# advancement level of trait
	t['org_type'] = 'predatory microbe' 			# species descriptor, if any	
	traits.append(t)

def fungus(traits):
	t = {}
	t['name'] = 'hyphae'
	t['pheno_reqs'] = {'tissues':-1}
	t['pheno_nopes'] = {'animalia':-1}	# otherwise, animal or plant
	t['pheno_tags'] = {'hyphae':-1} 
	t['biome_tols'] = ['toxin']		
	t['description'] = "forms threads"		
	t['stage'] = 4						# advancement level of trait
	t['org_type'] = 'simple fungus' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'lignase'
	t['pheno_reqs'] = {'hyphae':-1}
	t['pheno_nopes'] = {'wood':-1}	
	t['pheno_tags'] = {'carbon':1,'energy':1} 
	t['biome_reqs'] = ['lignin']
	t['description'] = "breaks down dead wood"		
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'saprotrophic fungus' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'root_symbiosis'
	t['pheno_reqs'] = {'hyphae':-1}
	t['pheno_nopes'] = {}	
	t['pheno_tags'] = {'carbon':1,'energy':1} 
	t['biome_reqs'] = ['root']
	t['eco_impacts'] = ['root_symbiont']
	t['description'] = "forms symbioses with producers"		
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'symbiotic fungus' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'fungal_chitin'
	t['pheno_reqs'] = {'hyphae':-1,'carbon':1}
	t['pheno_nopes'] = {'wood':-1,'animalia':-1}	
	t['pheno_tags'] = {'chitin':-1} 
	t['biome_tols'] = ['dry']		
	t['description'] = "forms structures with chitin"		
	t['stage'] = 4						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'fruiting_body'
	t['pheno_reqs'] = {'chitin':-1,'carbon':1}
	t['pheno_nopes'] = {'seeds':-1}
	t['pheno_tags'] = {'mushroom':-1} 
	t['biome_tols'] = ['cold']		
	t['eco_impacts'] = ['mushroom']
	t['description'] = "forms a fruiting body"		
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'mushroom' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'spore gills'
	t['pheno_reqs'] = {'mushroom':-1}
	t['pheno_nopes'] = {'puffball':-1,'pores':-1}	
	t['pheno_tags'] = {'spore_gills':-1} 
	t['biome_reqs'] = ['soil']
	t['description'] = "has spore gills"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'gilled mushroom' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'labyrinthine gills'
	t['pheno_reqs'] = {'spore_gills':-1}
	t['pheno_nopes'] = {'puffball':-1,'pores':-1}	
	t['description'] = "has fractal gills"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'gilled mushroom' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'puffball'
	t['pheno_reqs'] = {'mushroom':-1}
	t['pheno_nopes'] = {'spore_gills':-1,'pores':-1}	
	t['pheno_tags'] = {'puffball':-1} 
	t['description'] = "forms puffballs"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'puffball' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'floating puffball'
	t['pheno_reqs'] = {'puffball':-1,'carbon':1}
	t['pheno_nopes'] = {}	
	t['pheno_tags'] = {'floats':-1} 
	t['biome_reqs'] = ['Nitrogen']
	t['eco_impacts'] = ['sky_food']
	t['description'] = "puffballs float in the air"		
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'skyball' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'pores'
	t['pheno_reqs'] = {'mushroom':-1}
	t['pheno_nopes'] = {'spore_gills':-1,'puffball':-1}	
	t['pheno_tags'] = {'pores':-1} 
	t['biome_reqs'] = ['soil']
	t['description'] = "releases spores from tiny pores"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'polypore' 			# species descriptor, if any
	traits.append(t)

def animalia(traits):
	t = {}
	t['name'] = 'algagrazer'
	t['pheno_prereqs'] = {'propel':1}
	t['pheno_reqs'] = {'multicellular':-1}
	t['pheno_nopes'] = {'hunt':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'energy':2,'carbon':2,'graze':-1} 
	t['biome_reqs'] = ['micro_producer']
	t['eco_impacts'] = ['grazer']
	t['description'] = "grazes on algae"		
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'algae grazer' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'grazer'
	t['pheno_prereqs'] = {'propel':1}	
	t['pheno_reqs'] = {'multicellular':-1}
	t['pheno_nopes'] = {'hunt':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'energy':3,'carbon':3,'graze':-1} 
	t['biome_reqs'] = ['macro_producer']
	t['eco_impacts'] = ['grazer']
	t['description'] = "grazes on plants"		
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'plant grazer' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'hunter'
	t['pheno_prereqs'] = {'propel':2}	
	t['pheno_reqs'] = {'multicellular':-1,'muscle':-1}
	t['pheno_nopes'] = {'graze':-1}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'energy':4,'carbon':4,'hunt':-1} 
	t['biome_reqs'] = ['grazer']
	t['eco_impacts'] = ['predator']
	t['description'] = "hunts grazers"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'predator' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'no cell wall' 		# otherwise fungus
	t['pheno_reqs'] = {'multicellular':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'plant':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'animalia':-1} 
	t['eco_impacts'] = ['animal']			# tags used to interpret ecosystem niche
	t['description'] = "has animal-like cells"		
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'fungoid animal' 			# species descriptor, if any
	traits.append(t)
	fungus(traits)
	t = {}
	t['name'] = 'muscle cells' 		# otherwise sponge
	t['pheno_reqs'] = {'animalia':-1,'tissues':-1,'energy':1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'root':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'propel':2,'muscle':-1} 			# traits contributes organism feature
	t['description'] = "uses distinct muscle cells for locomotion"	
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'jellyfish' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'bilateral' 		# otherwise jellyfish and the like
	t['pheno_reqs'] = {'animalia':-1,'muscle':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'root':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'bilateral':-1,'propel':1} 			# traits contributes organism feature
	t['description'] = "has bilateral symmetry and a digestive tract with two ends"	
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'bilateral animal' 			# species descriptor, if any
	traits.append(t)
	eyes(traits)
	arthropods(traits)
	t = {}
	t['name'] = 'chordate' 		# otherwise arthropods/molluscs
	t['pheno_reqs'] = {'bilateral':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'exoskeleton':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'structure':1} 	
	t['description'] = "has a spine"	
	t['stage'] = 8						# advancement level of trait
	t['org_type'] = 'chordate' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'slow' 		# jawed chordates are like fish, not creepy worms
	t['pheno_reqs'] = {'structure':1,'propel':1,'energy':1}		# organism features needed to unlock trait
	t['biome_tols'] = ['cold']					# tag that forbids a biome
	t['description'] = "tolerates cold"	
	t['stage'] = 7						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'coordinated' 		# jawed chordates are like fish, not creepy worms
	t['pheno_prereqs'] = {'structure':1}	
	t['pheno_reqs'] = {'energy':1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'root':-1}	
	t['pheno_tags'] = {'propel':1} 			# traits contributes organism feature
	t['description'] = "moves with coordination"	
	t['stage'] = 7						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'hibernates' 		# jawed chordates are like fish, not creepy worms
	t['pheno_reqs'] = {'energy':1}		# organism features needed to unlock trait
	t['biome_prereqs'] = ['water']
	t['biome_reqs'] = ['cold']			# tag needed in biome
	t['biome_tols'] = ['frozen']					# tag that forbids a biome
	t['description'] = "can become dormant"	
	t['stage'] = 7						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'jawed' 		# jawed chordates are like fish, not creepy worms
	t['pheno_prereqs'] = {'structure':1,'eyes':2}		# organism features needed to unlock trait
	t['pheno_tags'] = {'energy':2,'jaws':-1} 			# traits contributes organism feature
	t['description'] = "has a jaw"	
	t['stage'] = 9						# advancement level of trait
	t['org_type'] = 'jawed chordate' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'sharp teeth' 		# jawed chordates are like fish, not creepy worms
	t['pheno_reqs'] = {'jaws':-1,'hunt':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'graze':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'energy':2,'carbon':2} 			# traits contributes organism feature
	t['biome_reqs'] = ['grazer']			# tag needed in biome
	t['description'] = "has sharp teeth"	
	t['stage'] = 10						# advancement level of trait
	t['org_type'] = 'carnivore' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'flat teeth' 		# jawed chordates are like fish, not creepy worms
	t['pheno_reqs'] = {'jaws':-1,'graze':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'hunt':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'energy':2,'carbon':2} 			# traits contributes organism feature
	t['description'] = "has grinding teeth"	
	t['stage'] = 10						# advancement level of trait
	t['org_type'] = 'herbivore' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'multifunctional teeth' 		# jawed chordates are like fish, not creepy worms
	t['pheno_reqs'] = {'jaws':-1,'hunt':-1,'graze':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'energy':4,'carbon':4} 			# traits contributes organism feature
	t['description'] = "has multiple types of teeth"	
	t['stage'] = 10						# advancement level of trait
	t['org_type'] = 'omnivore' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'bones' 		# has hard bones, not just cartilage
	t['pheno_prereqs'] = {'structure':1}
	t['pheno_reqs'] = {'bilateral':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'exoskeleton':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'size':1,'structure':1,'bones':-1} 			# traits contributes organism feature
	t['description'] = "has hard internal bones"	
	t['stage'] = 10						# advancement level of trait
	t['org_type'] = 'bony fish' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'scales' 	
	t['pheno_prereqs'] = {'structure':2}	
	t['pheno_reqs'] = {'carbon':1,'bones':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'fur':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'scales':-1} 			# traits contributes organism feature
	t['description'] = "scales protect the body"		
	t['stage'] = 11						# advancement level of trait
	t['org_type'] = 'reptiloid' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'lobe_fins' 		# has hard bones, not just cartilage
	t['pheno_prereqs'] = {'structure':2}	
	t['pheno_reqs'] = {'bones':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'propel':1} 			# traits contributes organism feature
	t['description'] = "has lobe-shaped fins"	
	t['stage'] = 12						# advancement level of trait
	t['org_type'] = 'lobe-finned fish' 			# species descriptor, if any
	traits.append(t)
	tetrapods(traits)
	
def tetrapods(traits):
	t = {}
	t['name'] = 'lungs' 		
	t['pheno_prereqs'] = {'structure':2,'propel':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'lungs':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['O2']			# tag needed in biome
	t['biome_tols'] = ['dry']					# tag that forbids a biome
	t['description'] = "can breathe in the air"		
	t['stage'] = 13						# advancement level of trait
	t['org_type'] = 'tetrapod' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'amniotic' 		
	t['pheno_reqs'] = {'lungs':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'amniote':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['dry']			# tag needed in biome
	t['description'] = "can reproduce on dry land"		
	t['stage'] = 14						# advancement level of trait
	t['org_type'] = 'amniote' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'homeotherm' 		
	t['pheno_reqs'] = {'energy':1}		# organism features needed to unlock trait
	t['pheno_prereqs'] = {'size':2,'propel':1}
	t['pheno_tags'] = {'size':1,'warmblooded':-1,'propel':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['dry']			# tag needed in biome
	t['biome_tols'] = ['cold','arid']		# tag that forbids a biome
	t['description'] = "tolerates a variety of temperatures"		
	t['stage'] = 15						# advancement level of trait
	t['org_type'] = 'land animal' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'fur' 		
	t['pheno_reqs'] = {'warmblooded':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'scales':-1,'feathers':-1,'fur':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'fur':-1} 			# traits contributes organism feature
	t['biome_tols'] = ['freezing']		# tag that forbids a biome
	t['description'] = "fur keeps it warm"		
	t['stage'] = 16						# advancement level of trait
	t['org_type'] = 'mammal' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'spine fur' 		
	t['pheno_reqs'] = {'fur':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'spikes':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['macro_predator']			# tag needed in biome
	t['description'] = "has defensive spikes"		
	t['stage'] = 17						# advancement level of trait
	t['org_type'] = 'hedgehog' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'feathers' 		
	t['pheno_reqs'] = {'scales':-1}		# organism features needed to unlock trait
	t['pheno_prereqs'] = {'size':1}
	t['pheno_tags'] = {'feathers':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['sand']			# tag needed in biome
	t['description'] = "has feather covering"		
	t['stage'] = 16						# advancement level of trait
	t['org_type'] = 'theropod' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'spikes' 		
	t['pheno_reqs'] = {'scales':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'feathers':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'spikes':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['macro_predator']			# tag needed in biome
	t['description'] = "has defensive spikes"		
	t['stage'] = 17						# advancement level of trait
	t['org_type'] = 'terrorsaur' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'birdwings' 		
	t['pheno_reqs'] = {'feathers':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'flight':-1,'size':3}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'flight':-1} 			# traits contributes organism feature
	t['description'] = "has feathered wings"		
	t['stage'] = 17						# advancement level of trait
	t['org_type'] = 'bird' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'batwings' 	
	t['pheno_prereqs'] = {'propel':2}	
	t['pheno_reqs'] = {'energy':2,'bones':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'feathers':-1,'flight':-1,'size':2}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'flight':-1} 			# traits contributes organism feature
	t['description'] = "has leather wings"		
	t['stage'] = 17						# advancement level of trait
	t['org_type'] = 'bird' 			# species descriptor, if any
	traits.append(t)
	
	# go nuts. Wings? Warm-blooded? Live birth? Feathers? Horns, claws?
	toolusers(traits)

def toolusers(traits):
	t = {}
	t['name'] = 'big brains' 
	t['pheno_prereqs']= {'eyes':3,'structure':2,'size':2}	
	t['pheno_reqs'] = {'energy':2}		# organism features needed to unlock trait
	t['pheno_tags'] = {'brains':1} 			# traits contributes organism feature
	t['description'] = "has a big brain"		
	t['stage'] = 17						# advancement level of trait
	t['org_type'] = 'big brain' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'social brains' 
	t['pheno_prereqs'] = {'brains':1}		
	t['pheno_reqs'] = {'energy':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'brains':1} 			# traits contributes organism feature
	t['description'] = "lives in complex social groups"		
	t['stage'] = 18						# advancement level of trait
	t['org_type'] = 'social animal' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'prehensile paws' 		
	t['pheno_prereqs'] = {'structure':2,'brains':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'prehensile':2} 			# traits contributes organism feature
	t['description'] = "has prehensile paws"		
	t['stage'] = 17						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'prehensile antennae' 		
	t['pheno_reqs'] = {'antennae':-1}		# organism features needed to unlock trait
	t['pheno_prereqs'] = {'brains':1}
	t['pheno_tags'] = {'prehensile':2} 			# traits contributes organism feature
	t['description'] = "has prehensile antennae"		
	t['stage'] = 17						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'prehensile tail' 		
	t['pheno_prereqs'] = {'structure':3,'brains':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'prehensile':1} 			# traits contributes organism feature
	t['description'] = "has a prehensile tail"		
	t['stage'] = 16						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'toolmaking' 		
	t['pheno_prereqs'] = {'prehensile':2,'brains':1,'size':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'toolmaking':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['rock']			# tag needed in biome
	t['biome_tols'] = ['arid','freezing']		# tag that forbids a biome
	t['eco_impacts'] = ['toolmaker']			# tags used to interpret ecosystem niche
	t['description'] = "makes advanced tools"		
	t['stage'] = 18						# advancement level of trait
	t['org_type'] = 'toolmaker' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'citybuilder' 		
	t['pheno_prereqs'] = {'toolmaking':-1,'brains':2}		# organism features needed to unlock trait
	t['pheno_tags'] = {'citybuilder':-1} 			# traits contributes organism feature
	t['biome_tols'] = []		# tag that forbids a biome
	t['biome_impacts'] = []		# trait adds tags to biome
	t['eco_impacts'] = ['citybuilder']			# tags used to interpret ecosystem niche
	t['description'] = "builds its own biome"		
	t['stage'] = 19						# advancement level of trait
	t['org_type'] = 'builder' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'interplanetary' 		
	t['pheno_reqs'] = {'citybuilder':-1,'energy':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'interplanetary':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['city']			# tag needed in biome
	t['eco_impacts'] = ['interplanetary']			# tags used to interpret ecosystem niche
	t['description'] = "moves between planets"		
	t['stage'] = 20					# advancement level of trait
	t['org_type'] = 'interplanetary' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'interstellar' 		
	t['pheno_reqs'] = {'interplanetary':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'interstellar':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['city']			# tag needed in biome
	t['eco_impacts'] = ['interstellar']			# tags used to interpret ecosystem niche
	t['description'] = "moves between stars"		
	t['stage'] = 21						# advancement level of trait
	t['org_type'] = 'interstellar' 			# species descriptor, if any
	traits.append(t)

def eyes(traits):
	t = {}
	t['name'] = 'eyespots' 		
	t['pheno_prereqs'] = {'propel':2}
	t['pheno_reqs'] = {'energy':1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'eyes':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['light']			# tag needed in biome
	t['description'] = "has simple eye spots"	
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = '' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'simple eyes' 	
	t['pheno_prereqs'] = {	'eyes':1}
	t['pheno_reqs'] = {'energy':1}					# organism features needed to unlock trait	
	t['pheno_tags'] = {'eyes':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['light']			# tag needed in biome
	t['description'] = "has simple eyes for limited sight"
	t['stage'] = 8						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'compound eyes' 
	t['pheno_prereqs'] = {	'eyes':2}		
	t['pheno_reqs'] = {'energy':1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'ce':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'eyes':1,'ce':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['light']			# tag needed in biome
	t['description'] = "has compound eyes"
	t['stage'] = 9						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'complex eyes' 		
	t['pheno_prereqs'] = {	'eyes':2}	
	t['pheno_reqs'] = {'energy':1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'ce':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'eyes':1,'ce':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['light']			# tag needed in biome
	t['description'] = "has complex eyes"
	t['stage'] = 10						# advancement level of trait
	traits.append(t)

def arthropods(traits):
	t = {}
	t['name'] = 'exoskeleton' 		
	t['pheno_reqs'] = {'bilateral':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'bones':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'structure':2,'exoskeleton':-1} 			# traits contributes organism feature
	t['description'] = "has an exoskeleton"
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'arthropod' 			# species descriptor, if any
	traits.append(t)	
	t = {}
	t['name'] = 'nymf' 		
	t['pheno_reqs'] = {'exoskeleton':-1,'energy':1}		# organism features needed to unlock trait
	t['biome_tols'] = ['cold']					# tag that forbids a biome
	t['description'] = "goes through a nymf stage"
	t['stage'] = 6						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'antenna' 		
	t['pheno_reqs'] = {'exoskeleton':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'eyes':1,'antennae':-1} 			# traits contributes organism feature
	t['description'] = "uses sensitive antenna"
	t['stage'] = 6						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'claw' 		
	t['pheno_prereqs'] = {	'eyes':1}	
	t['pheno_reqs'] = {'exoskeleton':-1,'hunt':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'carbon':1,'energy':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['animal']			# tag needed in biome
	t['description'] = "catches animals with its claw"
	t['stage'] = 6						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'wings'
	t['pheno_prereqs'] = {	'eyes':2}		 		
	t['pheno_reqs'] = {'exoskeleton':-1,'energy':2}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'size':2}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'flight':-1} 			# traits contributes organism feature
	t['biome_tols'] = ['dry']					# tag that forbids a biome
	t['description'] = "flies on diaphenous wings"
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'flying insect' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'nectar_drinker' 		
	t['pheno_reqs'] = {'flight':-1}		# organism features needed to unlock trait
	t['pheno_nopes'] = {'size':1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'energy':1,'carbon':1} 			# traits contributes organism feature
	t['biome_reqs'] = ['flower']			# tag needed in biome
	t['biome_tols'] = ['arid']					# tag that forbids a biome
	t['eco_impacts'] = ['pollinator']			# tags used to interpret ecosystem niche
				# # of times this trait may be evolved
	t['description'] = "consumes nectar from flowers"
	t['stage'] = 8						# advancement level of trait
	t['org_type'] = 'pollinating insect' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'legs' 		
	t['pheno_reqs'] = {'exoskeleton':-1,'energy':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'propel':1} 			# traits contributes organism feature
	t['description'] = "crawls on legs"
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'insect' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'shedding' 		
	t['pheno_reqs'] = {'exoskeleton':-1,'carbon':1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'size':1} 			# traits contributes organism feature
	t['description'] = "sheds its skin"
	t['stage'] = 6						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'fuzz' 		
	t['pheno_reqs'] = {'exoskeleton':-1,'warmblooded':-1}		# organism features needed to unlock trait
	t['pheno_tags'] = {'fur':-1} 			# traits contributes organism feature
	t['pheno_nopes'] = {'fur':-1}
	t['biome_tols'] = ['freezing']		# tag that forbids a biome
	t['description'] = "fuzz keeps it warm"		
	t['stage'] = 6						# advancement level of trait
	traits.append(t)
	
def flora(traits):
	t = {}							# moss es and liverworts
	t['name'] = 'root'
	t['pheno_reqs'] = {'multicellular':-1,'tissues':-1}
	t['pheno_nopes'] = {'propel':-1}		
	t['pheno_tags'] = {'root':-1} 
	t['biome_reqs'] = ['sand']
	t['biome_tols'] = ['dry']
	t['eco_impacts'] = ['root']
	t['description'] = "has root"	
	t['stage'] = 4						# advancement level of trait
	t['org_type'] = 'mossy plant' 			# species descriptor, if any
	traits.append(t)
	t = {}							
	t['name'] = 'ion pump'
	t['pheno_reqs'] = {'multicellular':-1,'tissues':-1}
	t['pheno_nopes'] = {'propel':-1,'animalia':-1}		
	t['biome_prereqs'] = ['water']
	t['biome_tols'] = ['cold']		
	t['description'] = "tolerates cold waters"	
	t['stage'] = 4						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'stem' 		
	t['pheno_reqs'] = {'root':-1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'vessels':-1} 			# traits contributes organism feature
	t['description'] = "transports fluids through a vascular system"
	t['stage'] = 5						# advancement level of trait
	t['org_type'] = 'vascular plant' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'leaves' 					# ferns, conifers, endosperms
	t['pheno_reqs'] = {'vessels':-1,'photosynthesis':-1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'energy':1,'carbon':1,'leaves':-1} 			# traits contributes organism feature
	t['eco_impacts'] = ['leaves']			# tags used to interpret ecosystem niche
	t['description'] = "has leaves that absorb more sunlight"
	t['stage'] = 6						# advancement level of trait
	t['org_type'] = 'leafy plant' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'needles' 					# ferns, conifers, endosperms
	t['pheno_reqs'] = {'leaves':-1,'carbon':1}					# organism features needed to unlock trait
	t['biome_tols'] = ['cold']					# tag that forbids a biome
	t['eco_impacts'] = ['needles']			# tags used to interpret ecosystem niche
	t['description'] = "has thick needles that tolerate cold"
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'wintergreen' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'plant_size1' 		
	t['pheno_reqs'] = {'vessels':-1,'carbon':1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'size':1} 			# traits contributes organism feature
	t['description'] = "grows tall"
	t['stage'] = 5						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'plant_size2' 		
	t['pheno_reqs'] = {'root':-1,'carbon':1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'size':1} 			# traits contributes organism feature
	t['description'] = "grows wide"
	t['stage'] = 5						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'seeds' 						# conifers and angiosperm
	t['pheno_reqs'] = {'vessels':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'mushroom':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'seeds':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['sand']			# tag needed in biome
	t['eco_impacts'] = ['seeds']			# tags used to interpret ecosystem niche
	t['description'] = "forms seeds, which are hardier than spores"
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'conifer' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'wood' 						# conifers and angiosperm
	t['pheno_reqs'] = {'vessels':-1,'carbon':1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'chitin':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'wood':-1,'energy':1} 			# traits contributes organism feature
	t['eco_impacts'] = ['lignin']			# tags used to interpret ecosystem niche
				# # of times this trait may be evolved
	t['description'] = "forms wood, which enables larger size and long life"
	t['stage'] = 7						# advancement level of trait
	t['org_type'] = 'tree' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'tree_size1' 		
	t['pheno_reqs'] = {'wood':-1,'carbon':1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'size':2} 			# traits contributes organism feature
	t['eco_impacts'] = ['tree']			# tags used to interpret ecosystem niche
	t['description'] = "grows very tall"
	t['stage'] = 5						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'cactuswax' 		
	t['pheno_reqs'] = {'seeds':-1}					# organism features needed to unlock trait
	t['biome_tols'] = ['arid']					# tag that forbids a biome
	t['description'] = "a layer of wax minimises water loss"
	t['stage'] = 7						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'endosperm' 					
	t['pheno_reqs'] = {'seeds':-1}					# organism features needed to unlock trait
	t['eco_impacts'] = ['endosperm']			# tags used to interpret ecosystem niche
				# # of times this trait may be evolved
	t['description'] = "includes an energy store in its seeds"
	t['stage'] = 7						# advancement level of trait
	traits.append(t)
	flowers(traits)

def flowers(traits):
	t = {}
	t['name'] = 'flower' 					
	t['pheno_reqs'] = {'seeds':-1}					# organism features needed to unlock trait
	t['pheno_tags'] = {'flower':-1} 			# traits contributes organism feature
	t['eco_impacts'] = ['flower']			# tags used to interpret ecosystem niche
	t['description'] = "develops a short-lived flower"
	t['stage'] = 8						# advancement level of trait
	t['org_type'] = 'flowering plant' 			# species descriptor, if any
	traits.append(t)
	t = {}
	t['name'] = 'bell flower' 					
	t['pheno_reqs'] = {'flower':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'specificflower':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'specificflower':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['pollinator']			# tag needed in biome
	t['eco_impacts'] = ['flower']			# tags used to interpret ecosystem niche
	t['description'] = "has a bell-shaped flower"
	t['stage'] = 9						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'tube flower' 					
	t['pheno_reqs'] = {'flower':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'specificflower':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'specificflower':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['pollinator']			# tag needed in biome
	t['eco_impacts'] = ['flower']			# tags used to interpret ecosystem niche
	t['description'] = "has a tube-shaped flower"
	t['stage'] = 9						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'cluster flower' 					
	t['pheno_reqs'] = {'flower':-1}					# organism features needed to unlock trait
	t['pheno_nopes'] = {'specificflower':-1}	# organism features needed to *lock* trait		
	t['pheno_tags'] = {'specificflower':-1} 			# traits contributes organism feature
	t['biome_reqs'] = ['pollinator']			# tag needed in biome
	t['eco_impacts'] = ['flower']			# tags used to interpret ecosystem niche
	t['description'] = "has a cluster of small flowers"
	t['stage'] = 9						# advancement level of trait
	traits.append(t)
		
	
def getTraits():
	traits = []
	micro_fundamentals(traits)
	micro_predator(traits)
	animalia(traits)
	flora(traits)
	t = {}
	t['name'] = 'tissues'
	t['pheno_reqs'] = {'multicellular':-1}
	t['pheno_tags'] = {'tissues':-1,'size':1}
	t['description'] = "exhibits differentiated tissues"
	t['stage'] = 5						# advancement level of trait
	traits.append(t)	
	
	t = {}
	t['name'] = 'macro_size_1'
	t['pheno_reqs'] = {'multicellular':-1,'carbon':1}
	t['pheno_nopes'] = {}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'size':1} 
	t['description'] = ""	
	t['stage'] = 5						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'macro_size_2'
	t['pheno_reqs'] = {'multicellular':-1,'carbon':1}
	t['pheno_nopes'] = {}	# organism features needed to *lock* trait				
	t['pheno_tags'] = {'size':1} 
	t['description'] = ""	
	t['stage'] = 5						# advancement level of trait
	traits.append(t)
	t = {}
	t['name'] = 'multicell'
	t['pheno_reqs'] = {'multi_prereq':2,'micro_size':1}
	t['pheno_tags'] = {'multicellular':-1} 
	t['biome_prereqs'] = ['water']
	t['description'] = "is multicellular"	
	t['stage'] = 4						# advancement level of trait
	t['org_type'] = 'multicellular organism' 			# species descriptor, if any	
	traits.append(t)
	

	return traits