#!/bin/bash
# created 2017
# last update 2017-11-29
# ex : ./split-month-4.sh nov 2017-nov.csv
#./split-month-4.sh month filename


mname=$1 
index=1
cpath=$(pwd)
cpath=${cpath%/*}
yr=$(date +'%Y')

rm -f $yr-$mname-mobile.csv
rm -f not-found-list-sort
rm -f not-found-list

#fline=$(head -n 1 $2) #get first line

while read line
do
col=${line##*,} # extract last column
rt=${line%,*} #extract first two colomn
flist=$(find -L ${cpath%/*}/video -type f -name $col)
fname=$(sed 's/\/media\/data\//..\/..\//g' <<< $flist) #replace ../../
pname=$(sed 's/\/media\/data\/video\/dharmavahini\///g' <<< $flist)
aname=$(sed 's/\//-/g' <<<  $pname)


if [ "${line##*,}" == "#day" ]
then
dayname=$mname-$index.m3u
((index++))
elif [ ! -f "$flist" ]
then
echo "find : " $flist
echo "not-found :"$col
echo $col " Location : $flist" >> not-found-list
else
echo $fname >> $dayname
fi
echo $rt,$aname >> $yr-$mname-mobile.csv # write filename not exist

done < $2

sed -i -- 's/-480p.mp4//' $yr-$mname-mobile.csv
sort not-found-list | uniq > not-found-list-sort
sleep 5
rm not-found-list


