# This PyOrigin example will import an ASCII file into an Origin worksheet and
# create a scatter plot from the data.
import PyOrigin
import math

# Define function to test if string represents a number.
def isNumber(str):
	try:
		float(str);
		return 1;
	except ValueError:
		return 0;


# Get path and name of a data file in Origin's Samples folder.
originPath = PyOrigin.GetPath(PyOrigin.PATHTYPE_SYSTEM)
dataFileName = originPath + "\\Samples\\Curve Fitting\\Step01.dat"

# Read all non-empty lines from file.
content = [i for i in open(dataFileName) if i[:-1]]
totalrow = len(content)

# Count header lines by finding first row with 80% of it's content is numeric.
elementFlag = []
rowFlag = []
for i in list(range(totalrow)):
	content[i] = content[i].rstrip().split("\t")
	elementFlag = [isNumber(element) for element in content[i]]
	if sum(elementFlag) / len(elementFlag) < 0.8:
		rowFlag.append(0)
	else:
		rowFlag.append(1)

headerlines = len(rowFlag) - rowFlag[::-1].index(0)
nheadercol = max([len(x) for x in content[0:headerlines]])

colUnits = content[headerlines - 2]    # second last header line has units
colComments = content[headerlines - 1] # last header line has comments
colLongNames = []
colLongNames.extend(''.join(element) for element in content[0:headerlines - 2])
colLongNames = '         '.join(colLongNames)

## Number of numeric columns and rows
ncol = max([len(x) for x in content[headerlines:totalrow]])
nrow = totalrow - headerlines

## Obtain numeric data in file "Step01.dat"
data = []
columns = []
for i in list(range(ncol)):
	columns = [float(element[i]) if isNumber(element[i]) else element[i] for element in content[headerlines:totalrow]]
	data.append(columns)

# Create worksheet page named 'MyData' using template named 'Origin'.
pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_WKS, "MyData", "Origin", 1)
wp = PyOrigin.Pages(str(pgName)) # Get page
wks = PyOrigin.ActiveLayer()     # Get sheet

# Setup worksheet.
wks.SetData(data, -1)                     # Put imported data into worksheet.
wks.SetName(dataFileName.split("\\")[-1]) # Set sheet name to file name without path.

# Set worksheet X column designations.
for i in list(range(math.floor(ncol / 2))):
	wks.Columns(2 * i + 1).SetType(PyOrigin.COLTYPE_DESIGN_X)

# Set worksheet label rows.
wks.Columns(0).SetLongName(colLongNames)
for i in list(range(nheadercol)):
	wks.Columns(i).SetUnits(colUnits[i])
	wks.Columns(i).SetComments(colComments[i])

# Create graph page named 'MyGraph' using template named 'Origin'.
pgName = PyOrigin.CreatePage(PyOrigin.PGTYPE_GRAPH, "MyGraph", "Origin", 1)
gp = PyOrigin.Pages(str(pgName))
gp.LT_execute("layer1.x.opposite = 1;layer1.y.opposite = 1;")
gl = gp.Layers(0)

# Create data range and plot it into the graph layer.
rng = PyOrigin.NewDataRange()  # Create data range.
rng.Add('X', wks, 0, 1, -1, 1) # Add worksheet's 2nd col as X.
rng.Add('Y', wks, 0, 2, -1, 2) # Add worksheet's 3rd col as Y.
dp = gl.AddPlot(rng, 201)      # Plot data range.