import pandas as pd


def file_upload(file):
	book = pd.read_excel(file).fillna(value='no')
	header = list(book.iloc[3])
	print(header[2])
	
	# for student in range(len(book)):
	# 	header = list(book.iloc[student])
	# 	first_name, middle_name, last_name = header[0].split(' ')[0], header[0].split(' ')[-2], header[0].split(' ')[-1] 
	# 	username = str('{}_{}'.format(first_name, last_name)).lower()
	# 	password = str(last_name.upper())
	# 	level, stream, of, year = header[1].split(' ')
	# 	#creating new students
	# 	room = '{}{}{}{}'.format(level, stream, of, year).lower()
	# 	print(first_name, middle_name, last_name)

 

file_upload('cat.xls')