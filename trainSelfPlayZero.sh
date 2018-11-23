counter=0
while [ $counter -le 20 ]
do
	python trainSelfPlayZero.py 1 1 $counter
	((counter++))
done
echo All done