#!/usr/bin/env bash

cd /Volumes/Abhijit-Seagate/Data_iot/iot-idle/us/

find "$(pwd)" -name "*.pcap" > /Volumes/Abhijit-Seagate/Data_iot/list-untagged-data.txt

cd /Users/abhijit/IOT_Project/intl-iot/model
./raw2intermediate.sh /Volumes/Abhijit-Seagate/Data_iot/list-untagged-data.txt /Volumes/Abhijit-Seagate/Data_iot/Intermediate/untagged-intermediate

#python extract_features.py /Volumes/Abhijit-Seagate/Data_iot/Intermediate/tagged_intermediate /Volumes/Abhijit-Seagate/Data_iot/Features/tagged-features
