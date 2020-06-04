import os
to_directory = 'untagged-intermediate-split-sliding/yi-camera/untagged'dxdsdsdsd
from_directory = 'untagged-intermediate/yi-cameraNOSYNC.tmp/unctrl/'


def file_splitter_intervals(file,time_stamp,out_file,num_file):
    flag = True
    temp_out=open(out_file,'w')
    table=open(f'{from_directory}/{file}',"r")
    for line_num,line in enumerate(table):
        first,second,the_rest = line.split("\t",2)
        if (float(second) >= time_stamp) and (flag):
            initial_val = second
            flag = False
        if flag==False:
            if (float(second)-float(initial_val)) <= 35 :
                # Close the current file
                temp_out.close()
                temp_out=open(out_file,"a")
                temp_out.write(line)
            else:
                print(f"Difference is = {float(second)-float(initial_val)}")
                print("Closing old file. Opening New one")
                print("Line")
                return num_file+1
        else:
            pass


for file in os.listdir('untagged-intermediate/yi-cameraNOSYNC.tmp/unctrl/'):
    print(f"Opening File {file}")
    table = open(f'{from_directory}/{file}', "r")
    time_array = []
    flag_time = True
    for line_num, line in enumerate(table):
        first, second, the_rest = line.split("\t", 2)
        if flag_time:
            time_val = float(second)
            time_array.append(time_val)
            flag_time = False
        if float(second) > time_val + 5:
            time_val = float(second)
            time_array.append(time_val)
    num_file = 0
    out1 = ((f"{to_directory}/{file}_part{num_file}.txt"))
    for time in time_array:
        num_file = file_splitter_intervals(file, time, out1, num_file)
        out1 = ((f"{to_directory}/{file}_part{num_file}.txt"))

    print(f'Closing file -> {file}')
    print('#######################################################')