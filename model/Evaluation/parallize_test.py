import pandas as pd
import numpy as np
import os
from glob import glob
import csv
import multiprocessing as mp
import numpy as np

column_names = ['frame_no', 'ts', 'ts_delta', 'protocols', 'frame_len', 'eth_src',
                'eth_dst', 'ip_src', 'ip_dst', 'tcp_srcport', 'tcp_dstport',
                'http_host', 'sni', 'udp_srcport', 'udp_dstport']

root = '/Volumes/Abhijit-Seagate/Data_iot/Intermediate/idle-intermediate/echo'
idle_time_dict = {}
idle_time_dict['idle'] = []
for files in os.listdir(root):
    tmp = pd.read_csv(f'{root}/{files}',sep='\t',names=column_names)
    idle_time_dict['idle'].extend(tmp['ts'])

root = '/Volumes/Abhijit-Seagate/Data_iot/Intermediate/tagged_intermediate/google-home-mini'
time_dict = {}
for file in os.listdir(root):
    if '.DS' not in file:
        print(f"Generating Dictionary for --> {file}")
        time_dict[file] = []
        for files in os.listdir(f'{root}/{file}'):
            tmp = pd.read_csv(f'{root}/{file}/{files}',sep='\t',names=column_names)
            time_dict[file].extend(tmp['ts'])
results = pd.read_csv('/Volumes/Abhijit-Seagate/Data_iot/results/results_google_mini_req/results/model_results.csv')
results.head()

results['labelled_data'] = 'unknown'
max_arr = []
min_arr = []
for keys,values in time_dict.items():
    max_arr.append(max(values))
    min_arr.append(min(values))
max_arr = max(max_arr)
min_arr = min(min_arr)

test_label = results[(results['start_time']>=min_arr) & (results['end_time'] <= max_arr)]


def label_tagged(split_df):
    num_rows = 0
    for index, row in split_df.iterrows():
        num_rows+=1
        print(f"Completed labelling of {num_rows}/{split_df.shape[0]} rows \n")
        for label, time_stamps in time_dict.items():
            for time_step in time_stamps:
                if (time_step<= row['end_time']) and (time_step>= row['start_time']):
                    if row['labelled_data']=='unknown':
                        row['labelled_data']=f"{label}"
                        split_df.at[index,'labelled_data']= f"{label}"
                        print(f'Row {index} has been labelled as a {label}')
                        break
                    else:
                        row['labelled_data']=f"{row['labelled_data']}|{label}"
                        split_df.at[index,'labelled_data']= f"{row['labelled_data']}|{label}"
                        print(f'Row {index} has been labelled as a {label}')
                        break
                    print(f'Row {index} has been labelled as a {label}')
    return(split_df)

def idle_tagged(split_df):
    num_rows = 0
    for index, row in split_df.iterrows():
        num_rows+=1
        print(f"Completed labelling of {num_rows}/{split_df.shape[0]} rows \n")
        for label, time_stamps in idle_time_dict.items():
            for time_step in time_stamps:
                if (time_step<= row['end_time']) and (time_step>= row['start_time']):
                    if row['labelled_data']=='unknown':
                        row['labelled_data']=f"{label}"
                        split_df.at[index,'labelled_data']= f"{label}"
                        print(f'Row {index} has been labelled as a {label}')
                        break
                    else:
                        row['labelled_data']=f"{row['labelled_data']}|{label}"
                        split_df.at[index,'labelled_data']= f"{row['labelled_data']}|{label}"
                        print(f'Row {index} has been labelled as a {label}')
                        break
                    print(f'Row {index} has been labelled as a {label}')
    return(split_df)


def parallelize_dataframe(df, func):
    num_cores = mp.cpu_count()-4
    num_partitions = num_cores #number of partitions to split dataframe
    df_split = np.array_split(df, num_partitions)
    pool = mp.Pool(num_cores)
    df = pd.concat(pool.map(func, df_split))
    pool.close()
    pool.join()
    return df


print("Labelling Tagged Data")
test_label = parallelize_dataframe(test_label,label_tagged)
test_label.head(50)
test_label.to_csv('/Volumes/Abhijit-Seagate/Data_iot/results/results_winkhub2/results/parallel_labelled_results.csv',index=False)

results_table = test_label
results_table['Accurate-label'] = 0
results_table['Accurate-anomaly'] = 1
for index,rows in results_table.iterrows():
    if rows['prediction'] in rows['labelled_data']:
        results_table.at[index,'Accurate-label'] = 1
    else:
        pass
for index,rows in results_table.iterrows():
    if rows['labelled_data'] =='unknown':
        results_table.at[index,'Accurate-anomaly'] = 0
    else:
        pass

results_table = results_table[results_table['labelled_data']!='unknown']

filtered_table = results_table
Accuracy_labelling = sum(filtered_table['Accurate-label'])/filtered_table.shape[0]
Accuracy_anomaly = sum(filtered_table['Accurate-anomaly'])/filtered_table.shape[0]
print(f'Labelling -> {Accuracy_labelling}',
      f'Anomaly -->{Accuracy_anomaly}')

max_arr = []
min_arr = []
for keys,values in idle_time_dict.items():
    max_arr.append(max(values))
    min_arr.append(min(values))
max_arr = max(max_arr)
min_arr = min(min_arr)

filtered_table = results[(results['start_time']>=min_arr) & (results['end_time'] <= max_arr)]
filtered_table.shape
filtered_table = parallelize_dataframe(filtered_table,idle_tagged)
filtered_table.to_csv('/Volumes/Abhijit-Seagate/Data_iot/results/results_google_mini_req/results/parallel_idle_labelled_results.csv',index=False)
idle_filtered = filtered_table[filtered_table['labelled_data']=='idle']
idle_filtered['prediction'] = idle_filtered['prediction'].map(lambda x: 'idle' if x=='anomaly' else x)
Accuracy_labelling = sum(results_table['Accurate-anomaly'])/results_table.shape[0]
print(f'Accuracy --> {Accuracy_labelling}')


