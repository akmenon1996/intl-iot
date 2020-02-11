#!/bin/bash

# please change the path names if necessary
cap_files='*.pcap'

outfile='outfile.csv'

num=0
tshark_cmd='tshark'
tshark_options='-T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e frame.len -E header=y -E separator=, -E quote=d -E occurrence=f'

for file in $cap_files
do
   num=$((num+1))
   echo "processing file: $file"
   outfile=$file.csv
   $tshark_cmd -r $file $tshark_options >> $outfile
   echo "Results in: $outfile ..."
done

echo "Done processing $num files!"