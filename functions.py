import numpy as np
import pandas as pd
import sqlalchemy

import os
from datetime import datetime


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


def load_balanced_df(sample_size=1000):
    '''
    Function to load in balanced dataframe from cleaned CSVs.
    
    Parameters:
        sample_size : int, number of rows to read in for each of the 18 attacks
                      in addition to 18 * this amount of benign data flows.
                      Default value is 1000.
    '''
    df = pd.read_csv('Datasets/Cleaned/clean_benign.csv', index_col=0, nrows=(18*sample_size))
    print(datetime.now().time(), 'Benign Database Shape: ', df.shape, '\n')

    for file in os.listdir('Datasets/Cleaned/'):
        if file[0] == '.':
            print('Dot File\n')
            pass
        elif file == 'clean_benign.csv':
            print(file, '\n')
            pass
        else:
            temp_df = pd.read_csv(f'Datasets/Cleaned/{file}', index_col=0, nrows=sample_size)
            print(datetime.now().time(), '-', file)
            print('Shape: ', temp_df.shape, '\n')
            df = pd.concat([df, temp_df])
            del temp_df

    df.reset_index(drop=True, inplace=True)
    print('Combined Database Shape: ', df.shape)
    return df