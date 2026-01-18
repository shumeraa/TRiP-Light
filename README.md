# TRiP-Light - Trip Leader Preference Processor

A user-friendly tool for processing trip leader preferences and generating assignment reports.

## What Does This Tool Do?

TRiP-Light helps you organize and analyze trip leader preferences by:
- Reading trip leader preference files from Excel spreadsheets
- Matching trip leaders with their guide status (Lead Guide or Assistant Guide)
- Generating color-coded reports that make it easy to see which leaders are qualified for which trips
- Creating summary reports with numerical data and text responses

## Quick Start Guide

### For Non-Technical Users

Follow these simple steps to get started:

#### Step 1: Install Python

1. **Windows:**
   - Download Python from [python.org/downloads](https://www.python.org/downloads/)
   - Run the installer
   - **Important:** Check the box that says "Add Python to PATH" during installation

2. **Mac:**
   - Open Terminal
   - Install Homebrew if you haven't already: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
   - Install Python: `brew install python3`

3. **Linux (Ubuntu/Debian):**
   - Open Terminal
   - Run: `sudo apt-get update && sudo apt-get install python3 python3-venv python3-pip`

#### Step 2: Set Up the Application

1. **Windows:**
   - Double-click `setup.bat`
   - Wait for the setup to complete (this may take a few minutes)

2. **Mac/Linux:**
   - Open Terminal in the TRiP-Light folder
   - Run: `./setup.sh`
   - Wait for the setup to complete (this may take a few minutes)

#### Step 3: Prepare Your Data

Create a folder named `Data` in the same location as this README (if it doesn't already exist), and add these files:

1. **Trip Leader Preference Files** (`.xlsx`)
   - One Excel file for each trip leader
   - Must contain two sheets:
     - Sheet 1: Trip leader information (name, questionnaire responses)
     - Sheet 2: Trip preferences
   - Must have exactly 1 empty row at the top

2. **TripStatusInfo.xlsx**
   - Contains the list of all available trips
   - Columns should include: Trip dates, Trip names, Trip categories

3. **TLPromotionStatus.xlsx**
   - Contains guide status for each trip leader
   - Shows which leaders are Lead Guides (LG) or Assistant Guides (AG) for each category

#### Step 4: Run the Application

1. **Using the Graphical Interface (Recommended for beginners):**
   - **Windows:** Double-click `run_gui.bat`
   - **Mac/Linux:** Double-click `run_gui.sh` (or run `./run_gui.sh` in Terminal)

2. **Using the Command Line (Advanced users):**
   - **Windows:**
     ```
     .venv\Scripts\activate
     python src\main.py
     ```
   - **Mac/Linux:**
     ```
     source .venv/bin/activate
     python src/main.py
     ```

#### Step 5: View Your Results

After processing completes, you'll find three Excel files in the `output` folder:

1. **prefsOutput.xlsx** - Trip preferences color-coded by guide status
   - Purple = Lead Guide (LG)
   - Pink = Assistant Guide (AG)
   - Black = Trip leader is unavailable for this trip

2. **numericalQuestionsOutput.xlsx** - Numerical data for each leader
   - Semesters left, satisfaction scores, trip counts, etc.

3. **shortAnswerQuestionsOutput.xlsx** - Text responses from leaders
   - Goals, interested categories, notes, etc.

## Troubleshooting

### "Python is not installed or not in PATH"
- Make sure you installed Python and checked "Add Python to PATH" during installation
- On Windows, you may need to restart your computer after installing Python

### "Data folder not found"
- Create a folder named `Data` (capital D) in the same location as this README
- Add your Excel files to this folder

### "No preference files found"
- Make sure your Excel files have the `.xlsx` extension
- Files starting with `~` (temporary Excel files) are automatically ignored
- Don't include TripStatusInfo.xlsx or TLPromotionStatus.xlsx in the count

### "Number of preferences does not match"
- Check that each preference file has exactly the correct number of trip preferences
- Verify the `numTrips` setting in `config.yaml` matches your actual number of trips
- Make sure there is exactly 1 empty row at the top of each preference sheet

### "File is open in another program"
- Close the Excel file if you have it open
- Make sure no other program is using the file

### "Permission denied"
- Make sure you have permission to read the input files
- Make sure you have permission to write to the `output` folder
- Close any output files if they're open in Excel

## Configuration

The `config.yaml` file contains all settings for the application. You can edit this file to:
- Change the number of trips for the current semester
- Modify cell mappings if your Excel files have a different format
- Update file paths for input data files

Example configuration:
```yaml
numTrips: 47  # Total number of trips for the current semester
prefsSheetIndex: 1  # Which sheet contains preferences (0=first, 1=second)
folderPath: "Data"  # Folder containing preference files
```

## File Format Requirements

### Trip Leader Preference Files

Each trip leader file should have:
- **Sheet 1 (Leader Info):** Name and questionnaire responses
- **Sheet 2 (Preferences):** Trip preferences (1 = first choice, 2 = second choice, etc.)
- Exactly 1 empty row at the top of each sheet
- Black-highlighted cells indicate unavailability for specific trips

### TripStatusInfo.xlsx

Should contain columns for:
- Trip dates (e.g., "Oct 12-14")
- Trip names (e.g., "Backpacking: White Mountains")
- Trip categories (e.g., "Backpacking", "Climbing", etc.)

### TLPromotionStatus.xlsx

Should contain:
- Trip leader names (one per row)
- Guide status for each category
  - "LG" = Lead Guide
  - Any other value (or blank) = Assistant Guide

## For Developers

### Running Tests

```bash
# Activate virtual environment
source .venv/bin/activate  # Mac/Linux
.venv\Scripts\activate  # Windows

# Run tests
pytest

# Run with verbose output
pytest -v
```

### Project Structure

```
TRiP-Light/
├── src/
│   ├── main.py              # Main entry point (command-line version)
│   ├── config.py            # Configuration loader
│   ├── functions.py         # Core processing functions
│   ├── tripManager.py       # Trip data management
│   ├── tripLeaderManager.py # Trip leader data management
│   └── utils.py             # Utility functions
├── Data/                    # Input files (you create this)
├── output/                  # Generated reports
├── config.yaml              # Configuration file
├── gui_app.py              # GUI application
├── setup.bat/.sh           # Setup scripts
├── run_gui.bat/.sh         # GUI launcher scripts
└── requirements.txt         # Python dependencies
```

### Key Architecture Details

- **Manager Classes:** `TripManager` and `TripLeaderManager` coordinate data processing
- **Excel Cell Mapping:** All cell references are centralized in `config.yaml`
- **Preference Processing:** Uses openpyxl to detect black-highlighted cells (unavailable trips)
- **Name Matching:** Fuzzy string matching handles minor spelling variations
- **Output Generation:** Color-coded Excel files using openpyxl conditional formatting

## Getting Help

If you encounter issues:

1. Check the error message carefully - they're designed to be helpful!
2. Review the Troubleshooting section above
3. Check that your files match the format requirements
4. Make sure all required files are in the `Data` folder
5. Verify your `config.yaml` settings

## Example Workflow

Here's a typical workflow:

1. Collect preference files from all trip leaders
2. Place all files in the `Data` folder
3. Update `config.yaml` if needed (e.g., new semester with different trip count)
4. Run the GUI application
5. Review the three output files
6. Use the color-coded preferences to make trip assignments

## Technical Details

- **Language:** Python 3.8+
- **Key Libraries:** pandas, openpyxl, PyYAML, tkinter (built-in)
- **Input Format:** Excel (.xlsx) files
- **Output Format:** Excel (.xlsx) files with conditional formatting

## License

This project is for internal use in managing trip leader assignments.
