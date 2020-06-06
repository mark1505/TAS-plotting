import numpy as np
import matplotlib.pyplot as plt
import glob

# Gets the wavelengths in order from the param file and puts them in a list
param_wavelengths = []
with open("run param.txt", "r") as f:
    for x in f.readlines():
        param_wavelengths.append(x[0:3])
    print("Wavelengths:", param_wavelengths)

scope_files = glob.glob("./*scopeavg")
scope_files = [s.replace('.\\', '') for s in scope_files]
scope_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))

DAQ_files = glob.glob("./*daqavg")
DAQ_files = [s.replace('.\\', '') for s in DAQ_files]
DAQ_files.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
print("Files in folder: ")
print(scope_files)
print(DAQ_files)

scope_array = []
DAQ_array = []

for x in scope_files:
    with open(x) as f:
        content = f.readlines()
        content = content[251:]
        data_file = np.loadtxt(content, delimiter="\t")
        scope_array.append(data_file)
print("scope_array")
print(scope_array)

for x in DAQ_files:
    with open(x) as f:
        content = f.readlines()
        content = content[251:]
        data_file = np.loadtxt(content, delimiter="\t")
        DAQ_array.append(data_file)
print("DAQ_array")
print(DAQ_array)


"""
graph_label = 0
n = 0

for x in range(len(param_wavelengths)):

    time = x[:, 0]
    absorbance = x[:, 1]
    plt.plot(time, absorbance)
    plt.ylabel("change in O.D.")
    plt.xscale("log")
    plt.xlabel("Time / s")
    plt.title(param_wavelengths[wavelength_tag] + " nm")
    plt.show()
    graph_tag += 1
"""