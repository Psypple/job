import pandas as pd

table=pd.read_excel("mm.xlsx")
hole=table['hole'].values.tolist()
elec=table['elec'].values.tolist()
z=table['z'].values.tolist()

print(z)
print(hole)
print(elec)
print(len(z))