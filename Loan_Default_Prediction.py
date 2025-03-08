import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import pyodbc

# Step 1: Load Data
file_path = 'loan_data.csv' # Your dataset file
loan_data = pd.read_csv(file_path)

# Step 2: Data Preprocessing
loan_data.dropna(inplace=True)
loan_data['Loan_Status'] = loan_data['Loan_Status'].apply(lambda x: 1 if x=='Y' else 0)

# Convert categorical columns
loan_data = pd.get_dummies(loan_data, drop_first=True)

# Step 3: Split Data
X = loan_data.drop('Loan_Status', axis=1)
y = loan_data['Loan_Status']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 4: Model Building
clf = RandomForestClassifier()
clf.fit(X_train, y_train)

# Step 5: Model Evaluation
y_pred = clf.predict(X_test)
print("Accuracy:", accuracy_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))

# Step 6: Store Data in SQL Database
connection = pyodbc.connect('DRIVER={SQL Server};'
                            'SERVER=your_server_name;'
                            'DATABASE=your_database_name;'
                            'Trusted_Connection=yes;')

cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS LoanPrediction (
                    Gender VARCHAR(10),
                    Married VARCHAR(10),
                    Dependents INT,
                    Education VARCHAR(20),
                    Self_Employed VARCHAR(20),
                    ApplicantIncome INT,
                    CoapplicantIncome FLOAT,
                    LoanAmount FLOAT,
                    Loan_Amount_Term INT,
                    Credit_History INT,
                    Property_Area VARCHAR(20),
                    Loan_Status INT)''')

# Insert data into SQL
for index, row in loan_data.iterrows():
    cursor.execute("INSERT INTO LoanPrediction VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                   row.Gender, row.Married, row.Dependents, row.Education,
                   row.Self_Employed, row.ApplicantIncome, row.CoapplicantIncome,
                   row.LoanAmount, row.Loan_Amount_Term, row.Credit_History,
                   row.Property_Area, row.Loan_Status)

connection.commit()
connection.close()

print("Data Inserted into SQL Database Successfully")
