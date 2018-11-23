counter=0
while [ $counter -le 10 ]
do
	python trainSelfPlay.py 1 1 $counter
	python trainSelfPlay.py 0 0 $counter
	((counter++))
done
echo All done