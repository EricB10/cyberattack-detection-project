# DDoS Attack Detection
## Concept
- Analysis of Benign and DDoS Attack dataflows, machine learning models to detect malicious DDoS activity.

## Process
- Collect and clean data, normalize columns, drop NA and fix infinite values.
- Separate databases by protocol and attack, recombine into balanced and anomaly detection datasets.
- Exploratory data analysis & visualizations.
- Prediction models to detect DDoS attacks.

## Data
- Started with 19 datasets which were combined into 11 DDoS and 1 Benign dataset of over 70 common websites/services.
- 11 types of DDoS attacks: DNS, LDAP, MSSQL, NTP, NetBIOS, Portmap, SNMP, SSDP, Syn, TFTP and UDPLag.
- Over 500,000,000 datapoints combined, each representing one data flow.
- Target variables:
  - Malicious (Binary Classification).
  - Label (Multiclass Classification).
- Over 80 features:
  - Protocol: TCP, UDP or HOPOPT.
  - Flow duration, down/uptime ratio.
  - Time active and idle min, max, mean and std.
  - Total forward & backward packets and size.
  - Forward and backward packet length min, max, mean and std.
  - Forward and backward header size.
  - Forward and backward bytes/sec and packets/sec rates.
  - Forward and backward interarrival time min, max, mean and std.
  - Forward and backward PSH and URG flags, total FIN, SYN, RST, ACK, CWE and ECE flags.
  - Forward and backward subflow packets, size.
  - Forward and backward initial window size.

## Modeling
- Binary Classification in a balanced dataset:
  50% Benign, 50% Malicious.
- Multiclass Classification in a balanced dataset:
  50% Benign, 50% divided into 11 DDoS attacks.
- Binary Classification in an anomaly detection dataset:
  99% Benign, 1% Malicious
- Multiclass Classification in an anomaly detection dataset:
  99% Benign, 1% divided into 11 DDoS attacks.
  
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
  
## Conclusions
- Simple models such as Decision Tree work very well.
- Given so much information about a dataflow (80+ features) it is easy to detect DDoS Attacks.
- It is hard to monitor that much information in real time so the following attributes should be monitored:
  - Min, max and mean packet size of a dataflow.
  - Mean header size.
  - Protocol.

## Future Plans
- Collect more benign data for dataset of .01% malicious dataflows.
- Test trained model on real-time data.
- Build front-end GUI.

![Min Packet Size](Images/Pkt_Length_Min.png)
![Max Packet Size](Images/Pkt_Length_Max.png)
![Mean Packet Size](Images/Pkt_Length_Mean.png)

## Sources
- DDoS data collected from Canadian Institute for Cybersecurity:
  - https://www.unb.ca/cic/datasets/index.html

- Benign data collected from Kaggle:
  - https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps

- All data originally created with CICFlowMeter:
  - https://www.unb.ca/cic/research/applications.html#CICFlowMeter
  
- Images obtained from WP DIY:
  - https://wpdoityourself.com/protection-ddos-attacks-wordpress-website/

- DDoS/Cybersecurity statistics and info obtained from Cybercrime Magazine, Cloudfare & Wikipedia:
  - https://cybersecurityventures.com/the-15-top-ddos-statistics-you-should-know-in-2020/
  - https://www.cloudflare.com/en-in/learning/ddos/what-is-a-ddos-attack/
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
