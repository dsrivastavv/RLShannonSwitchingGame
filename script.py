import os

iterations = 2
for iterNo in range(iterations):
	os.system("python train.py {} {}".format(iterNo,'cut'))
	os.system("python train.py {} {}".format(iterNo,'connect'))