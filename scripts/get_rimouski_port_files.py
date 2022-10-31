import sys, os, shutil, subprocess
from tqdm import tqdm


# may to august dates
dates = ["2022.05.30_", "2022.06.06_", "2022.06.13_", "2022.06.20_", "2022.06.27_", "2022.05.04_", "2022.05.11_", "2022.05.18_", "2022.05.25_"]

deltaTime = [200000, 240000]

if len(sys.argv) != 2:
	sys.stderr.write("Usage: get_rimouski_port_files.py directory \n")
	sys.exit(1)


directory = sys.argv[1]


packageByDateTime = {}

for File in os.listdir(directory):

	if File[-3:] == "ubx":
		#print("skip")
		continue;

	try:
		time = int(File[11:17])
	except ValueError:
		continue;
	if time > deltaTime[0] and time < deltaTime[1]:
		for date in dates:
			if date in File:
				dateTime = date + str(time)
				fileType = File[18:21]
				pos = 3
				
				if fileType == "gns":
					pos = 0
				elif fileType == "imu":
					pos = 1
				elif fileType == "son":
					pos = 2

				package = ["0","1","2"]
				
				if dateTime not in packageByDateTime:
					package[pos] = File
					packageByDateTime[dateTime] = package
				else:
					package = packageByDateTime[dateTime]
					package[pos] = File
					packageByDateTime[dateTime] = package
"""	
print(packageByDateTime)

outputPath = "/home/pat/Documents/linux_virt_share/bella"

for key in packageByDateTime.keys():
	package = packageByDateTime[key]
	for File in package:
		print(package)
		shutil.move(os.path.join(directory, File), os.path.join(outputPath, File))
"""

output = "/home/pat/projet/sat-img-processing/data/points/test.xyz" # TODO make it a param
parserPath = "" # TODO make it a param

for key in tqdm(packageByDateTime.keys()):
	package = packageByDateTime[key]
	gnss = os.path.join(directory, package[0])
	imu = os.path.join(directory, package[1])
	sonar = os.path.join(directory, package[2])
	p = subprocess.Popen('./../../MBES-lib/build/bin/hb-parser {} {} {} >> {}'.format(gnss, imu, sonar, output) , shell='True')
	p.wait()

