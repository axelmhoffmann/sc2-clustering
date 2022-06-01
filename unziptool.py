import urllib3
import os
import shutil
import zipfile
import sc2reader

############################################################
# A script to unzip all the files in the current directory #
############################################################

path = os.getcwd();

# Walk all zipfiles in path
zips = [f for f in os.listdir(path) if (os.path.isfile(os.path.join(path, f)) & f.endswith('.zip'))]
print('Unzipping {0} files...'.format(len(zips)))

# Unzip each one
for z in zips:
	zipPath = path + '/' + z
	print("Unzipping: {0}".format(zipPath))
	with zipfile.ZipFile(zipPath, 'r') as zref:
		zref.extractall(path)
		
print('Done!')