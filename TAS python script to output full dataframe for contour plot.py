import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import glob

# Gets the wavelengths in order from the param file and puts them in a list
param_wavelengths = []
with open("run param.txt", "r") as f:
    for x in f.readlines():
        param_wavelengths.append(x[0:3])

print("Wavelengths:", param_wavelengths)

# Checks the directory for every relevant file (DAQ and scope avg)
scope_files = glob.glob("./*scopeavg")
scope_files = [s.replace('.\\', '') for s in scope_files]
scope_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

DAQ_files = glob.glob("./*daqavg")
DAQ_files = [s.replace('.\\', '') for s in DAQ_files]
DAQ_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print("\nFiles in folder: ")
print(scope_files)
print(DAQ_files)

# Removes the negative times from each file (the first 250 data points are before t=0 and not needed)
scope_files_new = []
DAQ_files_new = []

for x in scope_files:
    scope_files_new.append(x + "_new")
    with open(x, "r") as input1:
        with open(x + "_new", "w") as output:
            for line in input1:
                if line[0] != "-":
                    output.write(line)

for x in DAQ_files:
    DAQ_files_new.append(x + "_new")
    with open(x, "r") as input1:
        with open(x + "_new", "w") as output:
            for line in input1:
                if line[0] != "-":
                    output.write(line)


# Joins the DAQ and scope files into a single file and saves them as wavelength_joined
joined_files = []
n = 0
l = 0

for x in scope_files_new:
    joined_files.append(param_wavelengths[n] + "_joined")
    with open(x, "r") as input1:
        with open(param_wavelengths[n] + "_joined", "w") as output:
            for line in input1:
                output.write(line)
    with open(DAQ_files_new[l], "r") as input2:
        with open(param_wavelengths[n] + "_joined", "a") as output1:
            for line in input2:
                output1.write(line)
    n += 1
    l += 1

# Prints the number of DAQ and scope files found and the list of joined files created
print("\nFiles in folder t < 0 removed:")
print(scope_files_new)
print(DAQ_files_new)
print("\nJoined files:")
print(joined_files)

# Creates a dictionary and adds the time axis as 1 pair (time axis is the same for each file),
# and the y-axis from each joined file as a pair.
with open(joined_files[0]) as f:
   x_column = [(line.split()[0]) for line in f]

data_dict = {}
data_dict["Time"] = (x_column)

counter = 0
for x in joined_files:
    with open(x) as f:
        y_column = [(line.split()[1]) for line in f]
    data_dict[param_wavelengths[counter]] = (y_column)
    counter += 1

# The dictionary containing all data is loaded into a dataframe using Pandas
df = pd.DataFrame.from_dict(data_dict)

# Converts all values from strings to floats so that they can be plotted.
df['Time'] = df['Time'].astype(float)
for x in param_wavelengths:
    df[x] = df[x].astype(float)

# Cleans up the dataframe, removing duplicate time values, sort ascending and reordering columns then outputs as csv.
df.sort_values(by='Time', ascending=True, inplace=True)
df.drop_duplicates(keep='first', inplace=True, ignore_index=False, subset=['Time'])
df = df.reindex(sorted(df.columns), axis=1)
df = df.set_index('Time').reset_index()
print(df)
df.to_csv("Dataframe.csv", index=False)

# Plot each wavelength as line plot for quick check
df2 = df.copy()
df2['Time'] = np.log(df2['Time'])
df2 = df2.set_index('Time')
df2.plot(subplots=True, layout=(4,5), figsize=(15, 8))
plt.show()
