# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TRiP-Light is a Python-based tool for processing trip leader preferences and generating assignment reports. It reads preference data from Excel files, matches trip leaders with their guide status across different trip categories, and produces formatted output files for trip assignment planning.

## Setup and Installation

```bash
# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Configuration

The application uses `config.yaml` in the project root for all configuration settings including:
- Number of trips for the current semester
- Excel cell mappings for extracting data from preference files
- File paths for input data files

To modify cell mappings or file paths, edit `config.yaml` directly - no code changes needed.

## Running the Application

```bash
# Run the main processing script
python src/main.py
```

The script expects:
- Preference files (`.xlsx`) in the `Data/` directory
- `TripStatusInfo.xlsx` in `Data/` containing trip information
- `TLPromotionStatus.xlsx` in `Data/` containing leader guide status
- `config.yaml` in the project root with cell mappings

Output files are generated in the `output/` directory:
- `prefsOutput.xlsx` - Preferences highlighted by leader guide status
- `numericalQuestionsOutput.xlsx` - Numerical metrics for each leader
- `shortAnswerQuestionsOutput.xlsx` - Text responses from leaders

## Testing

```bash
# Run all tests
pytest

# Run a specific test file
pytest test_data/test_filename.py

# Run tests with verbose output
pytest -v
```

## Architecture

### Core Components

**Manager Classes**: The system uses two manager classes that coordinate data processing:
- `TripManager` (in `tripManager.py`) manages trip data and provides trip querying
- `TripLeaderManager` (in `tripLeaderManager.py`) manages trip leader data and provides leader lookup

Both managers use a `cell_mappings` dictionary (loaded from `config.yaml` via `config.py`) to map semantic field names to Excel cell locations. The `reformat_cells()` utility in `utils.py` converts Excel-style cell references (e.g., "B2") into zero-indexed DataFrame coordinates.

**Data Flow**: The main processing pipeline (`main.py`) follows this sequence:
1. Process all preference files in the `Data/` folder via `process_all_pref_files()`
2. Read trip information from `TripStatusInfo.xlsx` via `process_trip_status_file()`
3. Read leader guide status from `TLPromotionStatus.xlsx` via `process_leader_status_file()`
4. Generate three output Excel files with formatting

**Excel Cell Mapping**: All Excel cell references are centralized in `config.yaml` with two main sections:
- `tripInfo` - Maps trip-related fields to cells in `TripStatusInfo.xlsx`
- `leaderInfo` - Maps leader-related fields to cells in preference files and `TLPromotionStatus.xlsx`

Cell references are strings like "C4" or lists like `["C15", "D15", "E15"]` for multi-cell fields. The `config.py` module loads these from YAML, and `utils.py` handles conversion from Excel notation to DataFrame indices.

**Preference Processing**: The `create_leader()` function in `functions.py` reads each preference file using openpyxl to detect black-highlighted cells (which indicate unavailable trips for that leader). Black highlighting is identified by checking if `start_color` and `end_color` are both 1 or 64. Preferences in black-highlighted cells are stored as `None`.

**Name Matching**: The system uses fuzzy string matching (via `difflib.SequenceMatcher`) in `addLeaderGuideStatus()` to match leader names between preference files and the guide status file. This handles minor spelling variations or whitespace differences with a default threshold of 0.8 similarity.

**Output Generation**: Functions like `outputPrefsHighlightOnLeader()` use openpyxl to apply conditional formatting:
- Purple fill for Lead Guide status (guideStatus == 1)
- Pink fill for Assistant Guide status (guideStatus == 0)
- Black fill for unavailable preferences (None values)

### Key Files

- `config.yaml` - YAML configuration file with cell mappings and settings (edit this to change configuration)
- `src/config.py` - Configuration loader that reads config.yaml and provides Python interface
- `src/main.py` - Entry point that orchestrates the processing pipeline
- `src/functions.py` - Core data processing functions for reading Excel files and generating outputs
- `src/tripManager.py` - Trip class and TripManager for managing trip data
- `src/tripLeaderManager.py` - TripLeader class and TripLeaderManager for managing leader data
- `src/utils.py` - Utility functions for Excel cell reference conversion

### Important Implementation Details

- Excel files must have exactly 1 empty row at the top (automatically removed by pandas with `row_number - 2`)
- The number of preferences must match `numTrips` variable (currently 47 for Spring 2026)
- File names starting with `~` are ignored (temporary Excel files)
- Leader names are normalized to lowercase and stripped of whitespace for matching
- The system validates that guide categories in `TLPromotionStatus.xlsx` are a subset of trip categories
