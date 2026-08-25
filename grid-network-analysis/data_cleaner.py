# Step 1: Load and examine raw data
import pandas as pd
import numpy as np
 
utilities = pd.read_csv('data_sets/utilities.csv')
substations = pd.read_csv('data_sets/substations.csv')
lines = pd.read_csv('data_sets/lines.csv')

print(substations.columns)
#print(substations.info())
# Step 2: Handle missing values
# Even though the generator produces clean data, treat this step seriously —
# Decide on imputation strategies for different columns and document your decisions and rationale.
if substations.isnull().sum().sum() == 0:
    print("No missing values")
    pass
else:
    print("Values missing, imputation beginning")
# Input imputation code here
# Remeber to compute imputations for each table

 
# Step 3: Data validation

# Verify every Source/Destination Substation ID in lines.csv exists in substations.csv
source_id_ver = lines['Source Substation ID'].isin(substations['Substation ID'])
dest_id_ver = lines['Destination Substation ID'].isin(substations['Substation ID'])

source_ver = True
dest_ver = True
for value in source_id_ver:
    source_ver = value
    if source_ver == False:
        break #print("Unidentified source id")   
    else: 
        pass

for value in dest_id_ver:
    dest_ver = value
    if dest_ver == False:
        break #print("Unidentified destination id") 
    else: 
        pass

#print(source_ver)
#print(dest_ver)

if source_ver== False or dest_ver==False:
    print(f"Unidentified Source or Destination ID in lines. \nSourceID:{source_ver}\nDestID:{dest_ver}.\nStopping program...")
    exit()
else:
    print("All Source IDs & Destination IDs verified")



# Check for duplicate entries

if utilities.duplicated().sum() == 0:
    print("No duplicates in utilities.csv")
else:
    print("deleting duplicates...")
    utilities.drop_duplicates(inplace=True)
    print("duplicates deleted")

if lines.duplicated().sum() == 0:
    print("No duplicates in lines.csv")
else:
    print("deleting duplicates...")
    lines.drop_duplicates(inplace=True)
    print("duplicates deleted")

if substations.duplicated().sum() == 0:
    print("No duplicates in substations.csv")
else:
    print("deleting duplicates...")
    substations.drop_duplicates(inplace=True)
    print("duplicates deleted")

#Duplicate entries were identified as rows where all column values were identical


# Validate that latitude/longitude fall within plausible West African bounds#

if substations["Latitude"].between(4,28).all() == True:
    print("All Latitude values within reasonable West African bounds")
else: pass
if substations["Longitude"].between(-16, 15).all() == True:
    print("All Longitude values within reasonable West African bounds")
else: pass


# Ensure data type consistency (numeric columns are truly numeric)
print(
substations.dtypes,
lines.dtypes,
utilities.dtypes)