from datetime import datetime
import os

GPSData = 'GPSData000001.txt';				# Путь и имя исходного файла с регистратора
time_correct = 60*60*(8);					# Поправка на часовой пояс, в секундах
time_correct_name_file = 60*60*(8+6);			# Поправка на часовой пояс в названии файла, в секундах
folder_done = "done/";							# Папка для готовых gpx файлов, "./" - текущая дериктория

#Значения по умолчанию
f = open(GPSData)
f.close()

header_autor = 'Author';
header_time = '2011-09-22T18:56:51Z';
header_name = 'Name';
header_desc = 'Description';
header_trk_name = 'Track Name';

os.makedirs(folder_done,exist_ok=True)

def header(header_autor, header_time, header_name, header_desc, header_trk_name):
	header = '''<?xml version="1.0" encoding="UTF-8"?>
	<gpx
	xmlns="http://www.topografix.com/GPX/1/1"
	version="1.1"
	creator="Sc0rpion"
	xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
	xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">
	  <time>'''+header_time+'''</time>
	  <metadata>
	    <name>'''+header_name+'''</name>
	    <desc>'''+header_desc+'''</desc>
	    <author>
	     <name>'''+header_autor+'''</name>
	    </author>
	  </metadata>
	  <trk>
	    <name>'''+header_trk_name+'''</name>
		<trkseg>'''
	return header

footer = '''
	</trkseg>
  </trk>
</gpx>''';

with open(GPSData, "r") as file1:
	for line in file1:
		if ('$V02' in line.strip()):
			flag = 1
		else:
			pieces = line.strip().split(",")
			timedone = int(pieces[0])+int(time_correct)
			iso8601 = str(datetime.utcfromtimestamp(timedone).isoformat())+".0Z"
			stroka = '''
	        <trkpt lat="'''+pieces[2]+'''" lon="'''+pieces[3]+'''">
	          <time>'''+iso8601+'''</time>
	        </trkpt>'''
			
			if (flag == 1):
				if f.closed == False:
					f.writelines(footer)
					f.close()
				
				iso860_name = str(datetime.utcfromtimestamp(int(pieces[0])+int(time_correct_name_file)).isoformat())
				file_name = folder_done+iso860_name.replace(':','_').replace('T',' ') +'.gpx'
				f = open(file_name, "w")
				f.writelines(header(header_autor, iso8601, iso8601, header_desc, iso8601))
				flag = 0
			
			f.writelines(stroka)
f.writelines(footer)
f.close()