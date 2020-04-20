#!/bin/bash

cp -a /Users/abhijit/Desktop/GIT_Projects/intl-iot/iot-data/us /Users/abhijit/Desktop/GIT_Projects/intl-iot/new-intermediate/us

targetfile='/Users/abhijit/Desktop/GIT_Projects/intl-iot/new-intermediate'
echo $targetfile
for outerfiles in $targetfile/*; ##outer
  do
    echo $outerfiles

            for nested_files2 in $outerfiles/*; ##devices
                do
                    echo "Processing Device: $nested_files2"
                    for nested_files3 in $nested_files2/*;  ##Label
                        do
                            echo "Processing Label: $nested_files3"
                            num=0
                            tshark_cmd=' /Applications/Wireshark.app/Contents/MacOS/tshark'
                            tshark_options='-Y ip -Tfields -e frame.number -e frame.time_epoch -e frame.time_delta -e frame.protocols -e frame.len -e eth.src -e eth.dst -e ip.src -e ip.dst -e tcp.srcport -e tcp.dstport -e http.host -e udp.srcport -e udp.dstport -E separator=/t'

                            for nested_files4 in $nested_files3/*; ##PCAP_FILES
                                do
                                       num=$((num+1))
                                       echo "processing file: $nested_files4"
                                       dname=`dirname $nested_files4`
                                       fname=`basename $nested_files4`
                                       fname=${fname%.pcap}.txt

                                       dirTarget=${dname}/${fname}

                                       $tshark_cmd -r $nested_files4 $tshark_options >> $dirTarget 2>/dev/null
                                       echo "Results in: $outfile ..."
                                       rm $nested_files4
                                done;
                            echo "Done processing $num files from $nested_files3!"
                        done;
                done;
  done;

