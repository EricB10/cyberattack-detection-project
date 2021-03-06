import numpy as np
import pandas as pd
import sqlalchemy

import itertools
import os
from datetime import datetime

from sklearn.metrics import confusion_matrix

import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns





def clean_cols(df):
    '''
    Function to clean and normalize column names.
    Also drops unnecessary columns.
    '''
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    
    # Drop first character in column name if it is a space
    for col in df.columns:
        if col[0] == ' ':
            df.rename(columns={col:col[1:]}, inplace=True)
    
    # Replace remaining spaces and punctuation with underscores
    df.columns = df.columns.str.replace(' ', '_')
    df.columns = df.columns.str.replace('.', '_')
    df.columns = df.columns.str.replace('/', '_')
    
    # Rename columns for uniformity
    rename = {
            'Total_Fwd_Packets':'Fwd_Total_Pkts',
            'Total_Backward_Packets':'Bwd_Total_Pkts',
            'Total_Length_of_Fwd_Packets':'Fwd_Total_Bytes',
            'Total_Length_of_Bwd_Packets':'Bwd_Total_Bytes',
            'Flow_Bytes_s':'Flow_Bytes_Sec',
            'Flow_Packets_s':'Flow_Pkts_Sec',
            'Fwd_Packets_s':'Fwd_Pkts_Sec',
            'Bwd_Packets_s':'Bwd_Pkts_Sec',
            'Min_Packet_Length':'Pkt_Length_Min',
            'Max_Packet_Length':'Pkt_Length_Max',
            'Packet_Length_Mean':'Pkt_Length_Mean',
            'Packet_Length_Std':'Pkt_Length_Std',
            'Packet_Length_Variance':'Pkt_Length_Var',
            'Fwd_Packet_Length_Max':'Fwd_Pkt_Length_Max',
            'Fwd_Packet_Length_Min':'Fwd_Pkt_Length_Min',
            'Fwd_Packet_Length_Mean':'Fwd_Pkt_Length_Mean',
            'Fwd_Packet_Length_Std':'Fwd_Pkt_Length_Std',
            'Bwd_Packet_Length_Max':'Bwd_Pkt_Length_Max',
            'Bwd_Packet_Length_Min':'Bwd_Pkt_Length_Min',
            'Bwd_Packet_Length_Mean':'Bwd_Pkt_Length_Mean',
            'Bwd_Packet_Length_Std':'Bwd_Pkt_Length_Std',
            'Average_Packet_Size':'Pkt_Size_Mean',
            'Avg_Fwd_Segment_Size':'Fwd_Segment_Size_Mean',
            'Avg_Bwd_Segment_Size':'Bwd_Segment_Size_Mean',
            'Fwd_Avg_Bytes_Bulk':'Fwd_Byte_Bulk_Rate_Mean',
            'Fwd_Avg_Packets_Bulk':'Fwd_Pkt_Bulk_Rate_Mean',
            'Fwd_Avg_Bulk_Rate':'Fwd_Num_Bulk_Rate_Mean',
            'Bwd_Avg_Bytes_Bulk':'Bwd_Byte_Bulk_Rate_Mean',
            'Bwd_Avg_Packets_Bulk':'Bwd_Pkt_Bulk_Rate_Mean',
            'Bwd_Avg_Bulk_Rate':'Bwd_Num_Bulk_Rate_Mean',
            'Subflow_Fwd_Packets':'Fwd_Subflow_Pkts',
            'Subflow_Fwd_Bytes':'Fwd_Subflow_Bytes',
            'Subflow_Bwd_Packets':'Bwd_Subflow_Pkts',
            'Subflow_Bwd_Bytes':'Bwd_Subflow_Bytes',
            'Init_Win_bytes_forward':'Fwd_Init_Win_Bytes',
            'Init_Win_bytes_backward':'Bwd_Init_Win_Bytes',
            'act_data_pkt_fwd':'Fwd_Act_Data_Pkt',
            'min_seg_size_forward':'Fwd_Seg_Size_Min',
            'Active_Mean':'Time_Active_Mean',
            'Active_Std':'Time_Active_Std',
            'Active_Max':'Time_Active_Max',
            'Active_Min':'Time_Active_Min',
            'Idle_Mean':'Time_Idle_Mean',
            'Idle_Std':'Time_Idle_Std',
            'Idle_Max':'Time_Idle_Max',
            'Idle_Min':'Time_Idle_Min'
    }
    df.rename(columns=rename, inplace=True)
    
    # Create dummy columns for each protocol
    HOPOPT = df['Protocol'] == 0
    TCP = df['Protocol'] == 6
    UDP = df['Protocol'] == 17
    df['HOPOPT'] = np.where(HOPOPT, 1, 0)
    df['TCP'] = np.where(TCP, 1, 0)
    df['UDP'] = np.where(UDP, 1, 0)
    
    # Drop unnecessary columns
    df.drop(columns=['Source_IP', 'Source_Port', 'Destination_IP',
                     'Destination_Port', 'Protocol', 'Timestamp'],
            inplace=True)
    
    # Applies only to fully benign dataset:
    # Create target column Malicious and drop unnecessary columns
    if 'ProtocolName' in df.columns:
        df['Malicious'] = 0
        df.drop(columns=['Label', 'L7Protocol'], axis=1, inplace=True)
        df.rename(columns={'ProtocolName':'Label'}, inplace=True)
        df['Label'] = 'Benign_' + df['Label']
    
    # Applies to all datasets containing malicious flows:
    # Create target column Malicious and drop unnecessary columns
    else:
        filt = df['Label'] == 'BENIGN'
        df['Malicious'] = np.where(filt, 0, 1)
        df['Label'] = np.where(filt, 'Benign_Unknown', df['Label'])
        df.drop(columns=['SimillarHTTP', 'Inbound'], axis=1, inplace=True)
    
    return df





def load_malicious_df(directory, sample_size=1000):
    '''
    Function to load in dataframe of only ddos dataflows from cleaned CSVs.
    
    Parameters:
        sample_size : int, max number of rows to read in for each of the 11 attacks
    '''
    
    # Read in benign dataset, nrows = 11 * sample_size
    df = pd.read_csv(f'Datasets/{directory}/{directory}_Benign.csv', index_col=0, nrows=0)
    
    # Read a sample of each of 11 attack datasets, nrows = sample_size
    for file in os.listdir(f'Datasets/{directory}/'):
        if file[0] == '.':
            pass
        elif file == f'{directory}_Benign.csv':
            pass
        else:
            try:
                temp_df = pd.read_csv(f'Datasets/{directory}/{file}', index_col=0, nrows=sample_size)
                df = pd.concat([df, temp_df])
                # Add equal num of rows to benign size
                benign_size += len(temp_df)
                del temp_df
            except:
                pass
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    return df





def load_benign_df(directory, sample_size=1000):
    '''
    Function to load in dataframe of only benign dataflows from cleaned CSV.
    
    Parameters:
        sample_size : int, max number of rows to read in
    '''
    
    # Read in benign dataset, nrows = 11 * sample_size
    df = pd.read_csv(f'Datasets/{directory}/{directory}_Benign.csv', index_col=0, nrows=sample_size)
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    return df





def load_balanced_df(directory, sample_size=1000):
    '''
    Function to load in balanced dataframe from cleaned CSVs.
    
    Parameters:
        sample_size : int, number of rows to read in for each of the 11 attacks
                      in addition to 11 * this amount of benign data flows.
                      Default value is 1000.
    '''
    
    # Size of benign data to load
    benign_size = 0
    
    # Read in benign dataset, nrows = 11 * sample_size
    df = pd.read_csv(f'Datasets/{directory}/{directory}_Benign.csv', index_col=0, nrows=0)
    
    # Read a sample of each of 11 attack datasets, nrows = sample_size
    for file in os.listdir(f'Datasets/{directory}/'):
        if file[0] == '.':
            pass
        elif file == f'{directory}_Benign.csv':
            pass
        else:
            try:
                temp_df = pd.read_csv(f'Datasets/{directory}/{file}', index_col=0, nrows=sample_size)
                df = pd.concat([df, temp_df])
                # Add equal num of rows to benign size
                benign_size += len(temp_df)
                del temp_df
            except:
                pass
        
    # Read a sample of benign database, nrows = benign_size
    temp_df = pd.read_csv(f'Datasets/{directory}/{directory}_Benign.csv', index_col=0, nrows=benign_size)
    df = pd.concat([df, temp_df])
    del temp_df
    
    # Reset index
    df.reset_index(drop=True, inplace=True)
    return df





def load_balanced_df2(sample_size=1000):
    '''
    Function to load in balanced dataframe from cleaned CSVs.
    
    Parameters:
        sample_size : int, number of rows to read in for each of the 18 attacks
                      in addition to 11 * this amount of benign data flows.
                      Default value is 1000.
    '''
    
    # Read in benign dataset, nrows = 11 * sample size
    df = pd.read_csv('Datasets/Final/Final_Benign.csv', index_col=0, nrows=(11*sample_size))
    
    # Add a sample of each of 11 attack datasets, nrows = sample size
    for file in os.listdir('Datasets/Final/'):
        if file[0:5] != 'Final':
            pass
        elif file == 'Final_Benign.csv':
            pass
        else:
            temp_df = pd.read_csv(f'Datasets/Final/{file}', index_col=0, nrows=sample_size)
            df = pd.concat([df, temp_df])
            del temp_df

    # Reset index
    df.reset_index(drop=True, inplace=True)
    return df





def plot_confusion_matrix(cm, classes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.Blues):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
        print("Normalized confusion matrix")
    else:
        print('Confusion Matrix, without normalization')
    print(cm)
    plt.figure(figsize=(20,20))
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, color='white')
    plt.colorbar()
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, color='white', rotation=45)
    plt.yticks(tick_marks, classes, color='white')
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt), fontsize=15,
                 horizontalalignment="center", verticalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.tight_layout()
    plt.ylabel('True Label', color='white')
    plt.xlabel('Predicted Label', color='white')