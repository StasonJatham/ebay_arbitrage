import pandas as pd 

pd.options.display.max_rows = 200
pd.options.display.max_columns = 999
data = pd.read_csv("ebay_categories.csv") 


print("------------------------------------------> 1")
print(data[data.columns[0]].dropna())
print("------------------------------------------> 2") # ---> some categoreis ?
print(data[data.columns[1]].dropna())

print("------------------------------------------> 3") # ---> some categoreis ?
print(data[data.columns[2]].dropna())
print("------------------------------------------> 4") # ---> some categoreis ?
print(data[data.columns[3]].dropna())
print("------------------------------------------> 5") # ---> some categoreis ?
print("------------------------------------------> 9") # ----> category ids
print(data[data.columns[8]].dropna())



#print(data[data.columns[4]])
#print("------------------------------------------> 6")
#print(data[data.columns[5]])
#print("------------------------------------------> 7")
#print(data[data.columns[6]])
#print("------------------------------------------> 8")
#print(data[data.columns[7]])
##print("------------------------------------------> 10")
#print(data[data.columns[9]])
#print("------------------------------------------> 11")
#print(data[data.columns[10]])

