import os
to_directory = 'untagged-intermediate-split-sliding/yi-camera/untagged'
from_directory = 'untagged-intermediate/yi-cameraNOSYNC.tmp/unctrl'
for file in os.listdir('untagged-intermediate/yi-cameraNOSYNC.tmp/unctrl/'):
    print(f"Opening File {file}")
    table=open(f'{from_directory}/{file}',"r")
    num_file = 0
    out1=((f"{to_directory}/{file}_part{num_file}.txt"))
    temp_out=open(out1,'w')

    for line_num,line in enumerate(table):
        first,second,the_rest= line.split("\t",2)
        if line_num == 0:
            initial_val = second

        if (float(second)-float(initial_val)) <= 35 :
            print(line)
            # Close the current file
            temp_out.close()
            out1=((f"{to_directory}/{file}_part{num_file}.txt"))
            temp_out=open(out1,"a")
            temp_out.write(line)
        else:
            print(f"Difference is = {float(second)-float(initial_val)}")
            print("Closing old file. Opening New one")
            print("Line")
            initial_val = second
            num_file+=1
            temp_out.close()
            out1=((f"{to_directory}/{file}_part{num_file}.txt"))
            temp_out=open(out1,"a")
            temp_out.write(line)
    print(f'Closing file -> {file}')
    print('#######################################################')
