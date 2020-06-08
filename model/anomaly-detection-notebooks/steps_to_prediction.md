# Documentation for getting predictions on unseen data for new device. 

## Step 1: Knn model development
If the knn model for the particular device is not available, then use the following steps for developing the knn model. 

- Convert the tagged pcap files for the device to text files by running raw2intermediate.sh
- Run the extract_features.py to generate features from the text files. 
- Run eval_models.py by passing knn as the model parameter. 
- Use the generated model from eval_models.py as the base model. 

## Step 2: Anomaly model development
- Use the anomaly-detection-notebooks/anomaly_detection.ipynb notebook to generate a multivariate anomaly detection model for your device. 
- While setting threshold make sure to analyse what threshold works best for your device. Ideally crossvalidate from -100000 to +400. 
- Save model. 


## Step 3: Prediction on new data. 
- Use the sliding_split.py to split your data into smaller time steps if neccessary. 
    - Ideally set time_window to 30 seconds. 
    - If you do not want to analyse specific time steps set slide_int = time_window.
    - If you want a sliding window the set slide_int to a value less than time_window. Ideally less than 10. 
- Use the code/anomaly-predict-newdata.py by changing the label, base_model and root_model addresses and pass the new data path. 

## Step 4: Evaluation
- Use Results.ipynb and replace the results variable with the path to the results file generated in the last step. 
