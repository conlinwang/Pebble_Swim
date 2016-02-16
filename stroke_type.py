from sklearn import tree
from sklearn import linear_model
import numpy as np
import os
import math

from pylab import *
from matplotlib.pyplot import figure, show
from matplotlib.patches import Ellipse
import matplotlib.transforms as mtransforms
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.parasite_axes import SubplotHost

from matplotlib import rc

import pickle
#--------Forming the classifier for stroke type ----------------------
# X = [
# [4.258167109483742, 5.1607796969335995, 5.049802321275856], # Conlin
# [6.026831748274058, 4.416167815441384, 4.494770361557955], # Conlin 
# [5.283443202386331, 4.235601336026944, 3.6195378087809025], # Tina 
# [6.4159912820363205, 8.815477146332432, 3.9041820348314644], # Ziv
# [5.330344238715281, 5.972009776765859, 3.3086191546218897], # NTUSTLG
# [4.7787737257806056, 6.437064639414717, 3.7673256870631313], # Von
# [6.053026802645389, 5.26134044322414, 5.7631453021218215], # Lin
# [7.655007667442749, 4.787039988319831, 5.236184227551372], # CYChien
# [6.862142302934119, 5.704208184790894, 4.181513315513754], # Alex
# [3.969753286445754, 3.7346427994845706, 3.5593634678925485], # Von
# [5.693876278035194, 5.184343960841118, 6.941227353914321], # Lin
# [5.041563603044351, 5.505387550364817, 3.9633105639715613], # Von
# [4.741502971351223, 5.3531623981039544, 3.490022926768523], # Von
# [4.840276279573856, 5.154906582456634, 4.015285911139932], # Von
# [4.044510521523196, 5.4552681074719205, 4.055067215088487], # Von
# [4.4463529909134785, 5.571365700232008, 5.344923162573113], # Conlin 
# [4.417513121006324, 5.648301013983434, 5.856496385438099], # Conlin 
# [4.592673021259021, 5.058103427805754, 5.188265016232616], # Conlin 
# [4.177288601128735, 5.1450813097814745, 5.7081858657499165], # Conlin 
# [4.31385629257781, 5.283521410152408, 5.656397711052026], # Conlin 
# [3.7653647282606753, 5.352528327795089, 5.829807731549308], # Conlin 


# [2.765079449564977, 3.7409732608583237, 5.0912502239374104], # Young
# [3.962365057244604, 5.756014848736286, 8.262719290693102], # Jush
# [2.973503668003376, 4.486584056173793, 8.007347108744248], # Young
# [3.35442087935945, 4.417853419830711, 7.204451774313747], # Lui
# [3.0165267736665617, 4.29235752166719, 7.063914447045714], # BigFish
# [5.242126816850534, 3.007679403311016, 7.738184896695871], # Lumi
# [6.343270418278741, 5.3632332859433145, 5.996918631854699], # Jush
# [4.161530816361361, 2.7692237354452924, 5.610058965733049], # Ms_Wu
# [3.924235866444942, 3.7361959496114987, 9.966284782738361], # Waterman_Jr
# [6.326034945594617, 3.6651050965141385, 5.451214198090586], # Conlin
# [5.217639009338536, 4.870222723829737, 6.090019502400221], # Conlin
# [6.222945675816648, 5.236291911510433, 5.660008399512441], # Conlin
# [6.200197280787899, 5.275285020027619, 5.360520520999338], # Jush
# [5.820190249757631, 5.402584952760141, 5.636555293753538], # Jush
# [5.858881202730386, 5.121823000587285, 5.445501188453484], # Jush
# [5.704806511820068, 5.363881254874767, 5.731457584355861], # Jush
# [5.895061677235797, 4.90214415887095, 5.900537056843448], # Jush
# [5.13164320257306, 2.6431661468272303, 3.9444505289119123], # Ms_Wu
# [5.39478665443617, 4.5935501730137585, 6.527836432349635], # Lin
# [5.8765515338047685, 5.226046854023401, 5.519616896120244], # Jush
# [6.071377306117235, 4.894199932219474, 5.435754020245575], # Jush
# [5.999913223612588, 4.759768341940601, 5.711347318170588], # Jush

# [2.9805044539890035, 5.431384341913829, 2.8065512722048385], # Tina
# [2.8951567587411837, 3.7031505029640455, 3.4182421147582116], # Von
# [3.1267409480538615, 3.091055814988739, 1.5654773979346148], # Gaberial
# [4.013050027307855, 4.955462626492724, 3.768854371810235], # Conlin
# [4.979298978933073, 7.468682467850381, 4.37543088199944], # Ray
# [4.315388718624799, 4.732015852107748, 3.398530905620988], # Lin
# [4.675596041992688, 5.934431977615027, 2.245721128482231], # CY_Chein
# [4.628096661654964, 7.593472231653638, 2.225300702105375], # Wendy03
# [9.522984130500301, 7.469000482138801, 5.846196473397603], # Wendy04

# [5.82009330425254, 3.7705046261475377, 5.1331716543472705], # Ms_Wu Back
# [4.044110467141591, 4.468425887541186, 5.494850752308301], # Conlin FSC
# [4.542105629158751, 6.642532977305399, 5.53081649237409], # Josh Back
# [4.279800397622035, 3.1406716326177606, 4.82720134792613], # Ms_Wu Back  NOTE 3 not 1
# [4.656154369146447, 5.437857328355814, 3.726760560508063], # Von
# [6.647873174894923, 13.057263829083329, 13.897204241115936], # Lui Fly
# [8.614967531469976, 9.315560754716516, 6.8536602376528775], # Lui Fly
# [7.414944101494218, 13.19493220512587, 10.16290356093231], # Lui Fly
# [6.647873174894923, 13.057263829083329, 13.897204241115936] # Lui Fly

# ]

# Y = [  0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
#        1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
#        2, 2, 2, 2, 2, 2, 2, 2, 2,
#        1, 0, 1, 3, 3, 3, 3, 3, 3
#        ]
# clf = tree.DecisionTreeClassifier(random_state = 1)
# clf = clf.fit(X, Y)

# pickle.dump(clf, open("./tree_Back_opt02.clf", "wb"))

data_dir = './classifier_paradump/'
clf = pickle.load(open("./tree_Back_opt.clf", 'r'))

with open(data_dir+"tree_Back_opt.txt", 'w') as f:    
        f = tree.export_graphviz(clf, out_file=f)    


def stroke_type( instance ):

	element_4 = clf.predict_proba( instance )
	element2 = str(element_4)
	element3 = element2.split(".")
	element4 = element3[0].split("[")
	
	# print int(element4[2]), int(element3[1]), int(element3[2]), int(element3[3])

	if( int(element4[2]) !=0 ):
		return 0
	elif ( int(element3[1]) !=0 ):
		return 1
	elif ( int(element3[2]) !=0 ):
		return 2
	elif ( int(element3[3]) !=0 ):
		return 3
	else:
		print "Error occurred"


# print clf.predict_proba([8.422661121769135, 6.197017768312967, 5.680578771681779])
#---------------------For Multiple data-----------------------
input_data = open("./file_list_06.txt", "r+") # input_data
line = input_data.readlines() # load data into python

Decision_Tree_counter = 0
Conlin_rule_counter = 0
Rule_FCS_counter = 0
Rule_BrS_counter = 0
Rule_Fly_counter = 0
Rule_Back_counter = 0
total_length_swim = 0

for index in range(0, len(line), 1):
	file_name_temp = line[index].split('\n')
	file_name = str(file_name_temp[0])
	# print "The file now running is = ",file_name
	file_name_profile = file_name.split("_")

	element01 = file_name_profile[-3].split("m")
	total_length_swim += int(element01[0])
	testing_data = [0, 0, 0]
	
	input_stroke_type_data = open("./stroke_count_Evaluation/"+file_name+"/stroke_type/stroke_type.txt", "r+")
	stroke_type = input_stroke_type_data.readlines()
	output_result = [0, 0, 0, 0]
	for index in range(0, len(stroke_type), 1):
		element = stroke_type[index].split("\n")
		element_1 = element[0].split(",")
		element_2 = element_1[0].split("[")
		element_3 = element_1[2].split("]")
		testing_data[0] = float(element_2[1])
		testing_data[1] = float(element_1[1])
		testing_data[2] = float(element_3[0])
		Conlin_rule_counter +=1
		# Back
		if( (float(testing_data[2]) > 7) and (float(testing_data[2]) < 10) and  (float(testing_data[2]) > float(testing_data[1]) ) and  (float(testing_data[2]) > float(testing_data[0]) ) ):
			output_result[1] += 1
			Rule_Back_counter += 1
		
		# Fly
		elif( (float(testing_data[0]) > 8) and (float(testing_data[0]) > float(testing_data[2])) ):
			output_result[3] += 1
			Rule_Fly_counter += 1

		# BrS
		elif ((float(testing_data[1]) >5.8) and (float(testing_data[0]) >4.0) and (float(testing_data[0]) < 6.4) and (float(testing_data[2]) < 5.0) and (float(testing_data[2]) > 4.0) and ((float(testing_data[1]) < 8.0)) and ( float(testing_data[1]) > float(testing_data[0]) > float(testing_data[2]) )):
			output_result[2] += 1
			Rule_BrS_counter += 1

		# FCS
		elif( float(testing_data[0]) > 6.5 and float(testing_data[0]) > float(testing_data[1]) and float(testing_data[0]) > float(testing_data[2]) ):
			output_result[0] += 1
			Rule_FCS_counter += 1

		#FCS	
		# elif( float(testing_data[0]) <= 6.5 and ( float(testing_data[0]) + float(testing_data[1]) ) / 2.0  > float(testing_data[2]) ):
		# 	output_result[0] += 1
		# 	Rule_FCS_counter += 1

		# Desicion Tree
		else:
			# print file_name
			# print "rule failed"
			# print testing_data
			element_4 = clf.predict_proba(testing_data)
			element2 = str(element_4)
			element3 = element2.split(".")
			element4 = element3[0].split("[")
			Decision_Tree_counter +=1
			# print int(element4[2]), int(element3[1]), int(element3[2]), int(element3[3])

			output_result[0] += int(element4[2])
			output_result[1] += int(element3[1])
			output_result[2] += int(element3[2])
			output_result[3] += int(element3[3])


	print output_result
	print max(output_result)
	stroke_type_result = 0
	if (output_result.index( max(output_result) ) == 0):
		# print "FCS"
		stroke_type_result = "FCS"
	elif (output_result.index( max(output_result) ) == 1):
		# print "Back"
		stroke_type_result = "Back"
	elif (output_result.index( max(output_result) ) == 2):
		# print "BrS"
		stroke_type_result = "BrS"
	elif (output_result.index( max(output_result) ) == 3):
		# print "Fly"
		stroke_type_result = "Fly"
	else:
		print "Predict stroke type Error occurred"
	if(file_name_profile[3] == stroke_type_result):
		# print "predict correct!!"
		# print "output_result =", output_result
		continue
	else:
		print "predict Error!!"
		print "The file now running is = ",file_name
		print "stroke_type_result=", stroke_type_result
		print "output_result =", output_result
		print ""


print "(Rule, Desicion Tree, Rule_Fly, Rule_FCS, Rule_BrS, Rule_Back)=\n(",
print int(Conlin_rule_counter) - int(Decision_Tree_counter),
print ",          ",
print int(Decision_Tree_counter),
print ",   ",
print int(Rule_Fly_counter),
print ",     ",
print int(Rule_FCS_counter),
print ",  ",
print int(Rule_BrS_counter) ,
print ",  ",
print int(Rule_Back_counter),
print ")"
print "(FCS, Back, BrS, Fly)"
print "total_length_swim =", total_length_swim

input_data.close()
input_stroke_type_data.close()