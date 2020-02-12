#!/bin/bash

for outerfiles in /home/amenon/Desktop/GIT_Projects/intl-abhijit/intl-iot/iot-data/us/blink-camera/*;
  do
    echo $outerfiles
    echo "Files inside are...."
    for innerfiles in $outerfiles/*;
      do
        # please change the path names if necessary
        echo "Processing files inside $innerfiles"
        cap_files=$innerfiles

        outfile='outfile.csv'

        num=0
        tshark_cmd='tshark'
        tshark_options='-T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e frame.len -e _ws.col.Info  -E header=y -E separator=, -E quote=d -E occurrence=f'

        for file in $cap_files
        do
           num=$((num+1))
           echo "processing file: $file"
           outfile=$file.csv
           $tshark_cmd -r $file $tshark_options >> $outfile
           echo "Results in: $outfile ..."
        done

        echo "Done processing $num files from $innerfiles!"
        cd ..
      done;
  done;


