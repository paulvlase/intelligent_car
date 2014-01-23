DATA_SET_FILE="BodyFat.csv"
CERINTA_2="cerinta2.dat"
CERINTA_3="cerinta3.dat"

> $CERINTA_2
> $CERINTA_3

FIRST_HIDDEN_LAYER="1 2 3 4 5 6 7 8 9 10 11 12"
SECOND_HIDDEN_LAYER="1 2 3 4 5 6 7 8 9 10 11 12"

for i in $FIRST_HIDDEN_LAYER; do
	for j in $SECOND_HIDDEN_LAYER; do
		./ia2-2012-hmw2.exe $DATA_SET_FILE $i $j 0.7
	done
done

gnuplot "cerinta2.plot"

cp $CERINTA2 ${CERINTA2}.1
> $CERINTA2

learningRatioList="0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9"
for learningRatio in $learningRatioList; do
	./ia2-2012-hmw2.exe $DATA_SET_FILE 9 9 $learningRatio
done

gnuplot "cerinta3.plot"
