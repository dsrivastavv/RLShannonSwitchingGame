counter=0
while [ $counter -le 1 ]
do
	python trainSelfPlay.py 1 1 $counter
	python trainSelfPlay.py 0 0 $counter
	((counter++))
done
echo All done