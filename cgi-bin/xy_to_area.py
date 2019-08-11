
#convert coordinate to area
def to_area(x_list, y_list):
	area_list = []
	area = ''
	for i in range(len(x_list)):
		if( y_list[i] == 417):
			if( x_list[i] < 40):
				area = "D0"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "B0"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A0"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "C0"
			elif( x_list[i] >= 350):
				area = "E0"
		elif( y_list[i] < 14):
			if( x_list[i] < 40):
				area = "D4"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "B4"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A4"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "C4"
			elif( x_list[i] >= 350):
				area = "E4"
		elif( y_list[i] < 78.02):
			if( x_list[i] < 40):
				area = "D3"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "B3"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A3"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "C3"
			elif( x_list[i] >= 350):
				area = "E3"
		elif( y_list[i] < 277.98):
			if( x_list[i] < 40):
				area = "D2"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "B2"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A2"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "C2"
			elif( x_list[i] >= 350):
				area = "E2"
		elif( y_list[i] < 417):
			if( x_list[i] < 40):
				area = "D1"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "B1"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A1"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "C1"
			elif( x_list[i] >= 350):
				area = "E1"
		elif( y_list[i] < 556.02):
			if( x_list[i] < 40):
				area = "E1"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "C1"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A1"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "B1"
			elif( x_list[i] >= 350):
				area = "D1"
		elif( y_list[i] < 755.12):
			if( x_list[i] < 40):
				area = "E2"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "C2"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A2"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "B2"
			elif( x_list[i] >= 350):
				area = "D2"
		elif( y_list[i] < 820):
			if( x_list[i] < 40):
				area = "E3"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "C3"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A3"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "B3"
			elif( x_list[i] >= 350):
				area = "D3"
		elif( y_list[i] >= 820):
			if( x_list[i] < 40):
				area = "E4"	
			if( x_list[i] >= 40 and x_list[i] < 105.1):
				area = "C4"
			elif( x_list[i] >= 105.1 and x_list[i] < 283.35):
				area = "A4"
			elif( x_list[i] >= 283.35 and x_list[i] < 350):
				area = "B4"
			elif( x_list[i] >= 350):
				area = "D4"
		area_list.append(area)

	return area_list