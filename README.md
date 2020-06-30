# DDoS Analysis & Detection
## Concept
- Analysis of Benign and DDoS data flows & packets, machine learning models to detect DDoS activity.

## Process
- Collect and clean data, normalize columns, drop NA and fix infinite values.
- Separate databases by protocol and attack, recombine into balanced and anomaly detection datasets.
- Exploratory data analysis & visualizations.
- Prediction models to detect DDoS attacks.

## Data
- Started with 19 datasets which were combined into 11 DDoS and 1 Benign dataset of over 70 common websites/services.
- 11 types of DDoS attacks: DNS, LDAP, MSSQL, NTP, NetBIOS, Portmap, SNMP, SSDP, Syn, TFTP, UDPLag.
- Over 500,000,000 datapoints combined, each representing one data flow.
- Target variables:
  - Malicious (Binary Classification).
  - Label (Multiclass Classification).
- Over 80 features:
  - Flow duration, down/uptime ratio.
  - Total forward & backward packets and size.
  - Protocol: TCP, UDP or HOPOPT.
  - Forward and backward packet length min, max, mean and std.
  - Forward and backward header size.
  - Total, forward and backward bytes/sec and packets/sec rates.
  - Total, forward and backward interarrival time min, max, mean and std.
  - Forward and backward PSH and URG flags, total FIN, SYN, RST, ACK, CWE and ECE flags.
  - Forward and backward subflow packets, size.
  - Time active and idle min, max, mean and std.
  - Forward and backward initial window size.

## Modeling
- Binary Classification in a balanced dataset:
  50% Benign, 50% Malicious.
- Multiclass Classification in a balanced dataset:
  50% Benign, 50% divided into 11 DDoS attacks.
  
## Results
- Binary Classification in a balanced dataset:
  - Dummy Classifier: Acc .512, F1 .513
  - Naive Bayes: Acc .822, F1 .844
  - Decision Tree: Acc .999, F1 .999
  - K Nearest Neighbors: Acc .997, F1 .997
  - Random Forest: Acc .999, F1 .999
  - XGBoost: Acc 1.0, F1 1.0
- Multiclass Classification in a balanced dataset:
  - Dummy Classifier: Acc .000, F1 .273
  - Naive Bayes: Acc .662, F1 .844
  - Decision Tree: Acc .924, F1 .933
  - K Nearest Neighbors: Acc .920, F1 .926
  - Random Forest: Acc .928, F1 .937
  - XGBoost: Acc .929, F1 .938

## Future Plans
- Binary Classification in an anomaly detection dataset:
  99% Benign, 1% Malicious.
- Multiclass Classification in an anomaly detection dataset:
  99% Benign, 1% divided into 11 DDoS attacks.

## Sources
- DDoS data collected from Canadian Institute for Cybersecurity:
  - https://www.unb.ca/cic/datasets/index.html

- Benign data collected from Kaggle:
  - https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps

- All data originally created with CICFlowMeter:
  - https://www.unb.ca/cic/research/applications.html#CICFlowMeter

- DDoS/Cybersecurity statistics obtained from Cybercrime Magazine & Wikipedia:
  - https://cybersecurityventures.com/the-15-top-ddos-statistics-you-should-know-in-2020/
  - https://en.wikipedia.org/wiki/Denial-of-service_attack
 
## Files 
### Notebooks
- Data_Cleaning_Notebook.ipynb
  Notebook used to drop NA values, normalize column names, separate data into CSVs by attack and protocol.
- EDA_Notebook.ipynb
  Notebook used for exploratory data analysis and the creation of visualizations.
- Modeling_Notebook.ipynb
  Notebook used to run dummy classifier and various machine learning models to classify DDoS attacks.

### /Model_Results/
- Directory containing model scores and feature importances.
  
### /Images/
- Directory containing all data visualizations.

### Other
- functions.py
  Functions used for data cleaning, reading in datasets, etc.
- README.md
  File explaining the project.
