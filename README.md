# per2py_lumicycle

1. Prepare data for analysis, depends on source of data:
   Need 2 files - signal.csv and XY.csv. XY must have same ID prefix, same columns and same number of or more of time/sample values. See .\_templates\ 
	(.\ refers to working directory with your per2py scripts, e.g. F:\PROGRAMY\Python\Per2Py\per2py_lumicycle)

1.A - Lumicycle data without XY coordinates   
   
	a. Open the first Lumicycle data file in LumiCycle Analysis.
	b. in Raw Data select by cursors the part to be analyzed, usually the whole curve.
	c. in Export menu select "Advance to next file after export"
	d. CTRL+SHIFT+T will export raw sequence to csv file, do this for all that are to be analyzed together.
	e. move the exported csv files to a common folder
	f. open PREPARE_LUMI_DF.py in spyder/idle, change the ID prefix to LUMI and run with F5.
	g. prompt will ask for the path to the csv containing folder, select it.
	h. move the resulting LUMI_signal.csv file to \data\analysis_output__\
	i. copy LUMI_XY.csv from '.\_templates' to '.\data\analysis_output__' as well

1.B - LV200 Fiji/ImageJ data created by CornerGridOverlay.py and OverlayMultiMeasure.ijm (single cell-sized grid in hand-drawn ROI)

	In Fiji, Plugins-Macro-Edit, open file: _OverlayMultiMeasure.ijm, then in new window File-Open: _GridOverlay.py.
	import image sequence, draw polygon ROI over the whole left SCN, hold SHIFT to draw multiple separate rois e.g. for right SCN.
	Use script CornerGridOverlay.py to create correct grid overlay. Set size of cells in pixels in variable L. Click on Run.
	In script _OverlayMultiMeasure.ijm, find 2 rows starting with SaveAs and ending with //change path. 
	Edit the path to desired folder and name the output csv file. Watch out for / not \ when copying from File Explorer. 
		Paths should point to ./data/analysis_output__/	if you want to analyze immediately.
		example path for signal file: F:/PROGRAMY/Python/Per2Py/per2py_lumicycle/data/analysis_output__/SCNGRID_signal.csv
		example path for XY file: F:/PROGRAMY/Python/Per2Py/per2py_lumicycle/data/analysis_output__/SCNGRID_XY.csv
	Run script OverlayMultiMeasure.ijm
	This creates 2 files with means and XY coordinates in the analysis folder. 
	

1.C - LV200 Fiji/ImageJ data created by _MultiMeasure.ijm (simple ROIs manually drawn, e.g. left and right SCN)

	In FIJI open Plugins-Macro-Edit, open file _MultiMeasure.ijm
	import image sequence, draw polygon ROI over the whole left SCN, press T to add to manager, repeat for right SCN
	Run macro _MultiMeasure.ijm (change path and name of the file in SaveAs)
	This creates file macro_SCN1.csv, repeat for all SCNs
	In python idle/spyder run script PREPARE_FIJI-ROI_DF.py 
	prompt will ask for the path to the csv containing folder, select it to combine all macro_SCN1-6 files to single FIJI_signal.csv file
	! If some data are missing (e.g. only wells 1,2,4,6 were analyzed), create those columns and fill them with number 1 (necessary to produce correct parameter heatmaps)
	Move FIJI_signal.csv to '.\data\analysis_output__' and copy FIJI_XY.csv from '.\_templates' to '.\data\analysis_output__' as well


2. Open file START_ALL.py in IDLE/spyder (via conda-per2py environment or using batch file, see installation notes)

3. Change INPUT_FILES = ['ID'] to match your file names ID_signal.csv and ID_XY.csv.

4. Set grid_overlay = True, if using ImageJ generated XY coordinates (1B), False if using mock XY file (1A/1C).

4. Time_factor should be 1/6 for Lumicycle, 1 or more for LV200, but change if needed [in hours].

5. Change treatment and end_h variables as needed (i.e. start and end times in hours for analysis of selected time intervals).
   To get exact timing on treatment, it may be useful to copy the signal data to prism and inspect the curve (need the exact hour from start).

6. Change variable nth=1 for all "single cell/SCN" plots, nth=10 for every 10th plot (for 1B with hundreds of grid cells)

7. Run by F5.

7. Plots are saved as png (for viewing) and svg (import to Corel Draw), output tables as csv files in .\data\analysis_output__\

8. Move all plots and tables to some folder, use this structure:
	\analysed_data\SCN1L\before (here goes data from first left SCN analyzed before any treatment)
	\analysed_data\SCN1L\after (here goes data from first left SCN analyzed after treatment)
	\analysed_data\SCN1R\before (here goes data from first right SCN analyzed before any treatment)
	...
9. Combine all experiments that you want to analyze together in this way. Then you can use script Z:\_install\Python scripts Martin\plots_tables\Composite_Per2Py.py
   to create nice composite figure with all plots together. Just set the total number of SCN folders and choose whcih type of graph do you want.
