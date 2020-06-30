# DDoS Analysis & Detection
- DDoS data collected from Canadian Institute for Cybersecurity:
  - https://www.unb.ca/cic/datasets/index.html

- Benign data collected from Kaggle:
  - https://www.kaggle.com/jsrojas/ip-network-traffic-flows-labeled-with-87-apps

- All data originally created with CICFlowMeter:
  - https://www.unb.ca/cic/research/applications.html#CICFlowMeter

- DDoS/Cybersecurity Statistics obtained from Cybercrime Magazine & Wikipedia:
  - https://cybersecurityventures.com/the-15-top-ddos-statistics-you-should-know-in-2020/
  - https://en.wikipedia.org/wiki/Denial-of-service_attack
  
## Analysis of DDoS vs Benign data flows, models attempting to detect DDoS activity
- Clean data, create features
- Exploratory data analysis
- Prediction models to detect DDoS attacks (binary and multiclass models)
  
## Notebooks
- Data_Cleaning_Notebook.ipynb
- EDA_Notebook.ipynb
- Modeling_Notebook.ipynb

## Other Files
- functions.py - functions used for data cleaning, reading in datasets, etc
- Model_Scores.csv - Accuracy and F1 scores of various prediction models
- Feature_Importances.csv - feature importances of various prediction models
