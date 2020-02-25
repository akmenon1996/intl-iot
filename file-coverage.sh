#!/bin/bash

for outerfiles in /Users/abhijit/Desktop/GIT_Projects/intl-iot/iot-data/us/yi-camera/*;
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
        tshark_cmd=' /Applications/Wireshark.app/Contents/MacOS/tshark'
        tshark_options=' -Y ip -Tfields -e frame.number -e frame.time_epoch -e frame.time_delta -e frame.protocols -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e http.host  -e udp.srcport -e udp.dstport -E separator=,'
##tshark_options='-T fields -e frame.number -e frame.time -e eth.src -e eth.dst -e ip.src -e ip.dst -e ip.proto -e frame.len -e _ws.col.Info  -E header=y -E separator=, -E quote=d -E occurrence=f'

        for file in $cap_files
        do
           num=$((num+1))
           echo "processing file: $file"
           outfile=$file.csv
           $tshark_cmd -r $file $tshark_options >> $outfile
           echo "Results in: $outfile ..."
        done;
        echo "Done processing $num files from $innerfiles!"
        cd ..
      done;
  done;


