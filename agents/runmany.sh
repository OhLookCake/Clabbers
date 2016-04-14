
for i in `seq 1 1000`;
do
	echo $i
	echo $i >> resultsQvsG
	python interfaceQvsG.py $i | tail -6 >> resultsQvsG
	echo "------------------">>resultsQvsG
done
