import numpy as np
import matplotlib.pyplot as plt
import glob

# Searches for all txt files (.txt) with any name (*) in the current python project directory (./)
files = glob.glob("./*.txt")
print("Files in folder: ")
print(files)
print("\nOutput file names: ")

colours = ["k", "r", "b", "g", "tab:purple", "c", "tab:orange", "y", "deeppink", "navy", "lime", "tab:brown", "tab:gray", "lightcoral", "teal", "olive", "gold", "mediumorchid"]
multi_plot = []
number_of_plots = 0
file_names_for_legend = []

# cycles through each txt file, extracts x, y , plots, renames, saves, and adds the x, y to multi_plot array
# and adds to the file_names_for_legend list for the multiplot.
# there has to be the same number of x values as y values (UV-probe sometime records additional x with no y values)
for x in files:
    a = x.replace(".", "")
    b = a.replace("\\", "")
    c = b.replace("txt", "")
    print(c)
    file_names_for_legend.append(c)
    with open(x) as f:
        content = f.readlines()
        content = content[2:]
        data_file = np.loadtxt(content, delimiter=",")
        time = data_file[:, 0]
        absorbance = data_file[:, 1]
        plt.plot(time, absorbance)
        plt.xlabel("Wavelength / nm")
        plt.ylabel("O.D.")
        plt.savefig("plot_" + str(c) + ".pdf")
        plt.show()
        multi_plot.append(data_file)
        number_of_plots += 1
        f.close()
        
# Draw all the lines in the same plot, assigning a label for each one to be
print("")
print("Number of plots:", number_of_plots)

# The data for multiplot, sets up a multiplot graph and then a function cycles through_number of_cycles times
# and gets the data. Colours are turned to numbers.

def loop_plot(multi_plot):
    fig, ax = plt.subplots(1, figsize=(8, 6))
    fig.suptitle('Plot overlay', fontsize=15)
    plt.xlabel("Wavelength / nm")
    plt.ylabel("O.D.")

    for a in range(number_of_plots):
        x = multi_plot[a][:, 0]
        y = multi_plot[a][:, 1]
        ax.plot(x, y, color=colours[a], label=file_names_for_legend[a])
        plt.legend(loc="upper right", title="", frameon=False)
    plt.savefig("Overlay.pdf")
    plt.show()

loop_plot(multi_plot)


"""x1 = multi_plot[0][:, 0]
x2 = multi_plot[1][:, 0]
x3 = multi_plot[2][:, 0]
y1 = multi_plot[0][:, 1]
y2 = multi_plot[1][:, 1]
y3 = multi_plot[2][:, 1]

# Initialise the figure and axes.
fig, ax = plt.subplots(1, figsize=(8, 6))

# Set the title for the figure
fig.suptitle('Plot overlay', fontsize=15)

# shown in the legend.
ax.plot(x1, y1, color="red", label="My Line 1")
ax.plot(x2, y2, color="green", label="My Line 2")
ax.plot(x3, y3, color="blue", label="My Line 3")

# Add plot axis
plt.xlabel("Wavelength / nm")
plt.ylabel("O.D.")

# Add a legend, and position it on the lower right (with no box)
plt.legend(loc="upper right", title="", frameon=False)

# Show the plot
plt.show()"""