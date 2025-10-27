## 💱 Currency Risk Management for an American Company

This project addresses the **currency risk exposure** of an American company organizing trips to the Euro area for students. The company needs to cover costs in euros, which exposes it to fluctuations in the euro-dollar exchange rate.  

- **Payment obligation:** 1000 euros per student at the time of departure \( t = T \)  
- **Uncertainties:**  
  - Number of student participants  
  - Euro-dollar exchange rate at time \( T \)

At the initial time \( t = 0 \), the spot exchange rate \( p_0 \) is known.

---

## 🛠 Hedging Instruments

To mitigate exchange rate risk, the company can use derivative instruments:  

- **Forward contracts**  
- **European call options** with three strike prices: \( K_1 \), \( K_2 \), \( K_3 \) (all expiring at \( t = T \))

---

## 🎯 Project Objective

Determine the **optimal combination of derivatives** that minimizes the company's exposure to currency risk.

---

## 📁 Project Structure

RiskManagementProject/
├── .vscode/ # VSCode configuration files
├── files_analysis/ # Folder containing analysis data/files
├── images_report/ # Folder with images for the report
├── DataServer.py # Script to manage data server
├── GenerateScenarios.py # Script for generating scenarios
├── HedgingModel.py # Script implementing the hedging model
├── PricingDerivatives.py # Script for pricing derivative instruments
├── README.md # Project README
├── analysis_notebook.ipynb # Jupyter notebook for analysis
├── main.py # Main script to run the project
└── report_Omento_Racca_Ruffinello.pdf # Final project report
