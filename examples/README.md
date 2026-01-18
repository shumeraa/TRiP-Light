# Example Files

This folder contains example input files that demonstrate the expected format for TRiP-Light.

## What's Included

1. **Example_TripLeader_JohnDoe.xlsx** - Sample trip leader preference file
2. **Example_TripStatusInfo.xlsx** - Sample trip information file
3. **Example_TLPromotionStatus.xlsx** - Sample guide status file

## How to Use These Examples

### Option 1: Test the Application
1. Copy all example files from this folder to the `Data` folder
2. Run the GUI application to see how it works
3. Check the `output` folder for the generated reports

### Option 2: Create Your Own Files
1. Open the example files in Excel to see the expected format
2. Use them as templates for creating your own files
3. Pay attention to:
   - Sheet structure (which sheet contains what data)
   - Column positions and headers
   - The empty row at the top
   - How black-highlighted cells indicate unavailability

## File Format Details

### Trip Leader Preference Files

Each file represents one trip leader and contains two sheets:

#### Sheet 1: "Trip Leader Info"
- Contains personal information and questionnaire responses
- Row 1: Empty (required)
- Row 2+: Header and data

Key cells (based on default config.yaml):
- C4: Trip leader name
- C5: Semesters left
- C6: Trip satisfaction (1-5 scale)
- C8: Number of trips assigned last semester
- C9: Number of trips dropped
- C10: Number of trips picked up
- C12: Main goal for the semester
- C13: Interested categories
- C15, D15, E15: Three leaders they'd like to work with
- B19: Additional notes

#### Sheet 2: "Trip Preferences"
- Contains trip preferences (1 = first choice, 2 = second choice, etc.)
- Row 1: Empty (required)
- Row 2: Headers
- Row 3+: Trip data with preferences

Columns:
- B: Trip dates
- C: Trip name
- D: Trip category
- E: Preference ranking (1, 2, 3, etc.)

**Black-highlighted cells** in the preference column (E) indicate the leader is NOT available for that trip.

### TripStatusInfo.xlsx

Contains the master list of all trips for the semester.

Structure:
- Row 1: Empty (required)
- Row 2: Headers
- Row 3+: Trip data

Columns (based on default config.yaml):
- B: Trip dates (e.g., "Oct 12-14, 2025")
- C: Trip name (e.g., "Backpacking: White Mountains")
- D: Trip category (e.g., "Backpacking", "Climbing", "Paddling")

### TLPromotionStatus.xlsx

Contains guide status information for all trip leaders.

Structure:
- Row 1: Empty (required)
- Row 2: Headers
- Row 3: Category names
- Row 4+: Leader data

Columns (based on default config.yaml):
- C: Trip leader name
- D onwards: Guide status for each category
  - "LG" = Lead Guide (can lead trips in this category)
  - Any other value or blank = Assistant Guide

## Important Notes

1. **Empty Row at Top:** All files MUST have exactly 1 empty row at the top. This is a requirement of the system.

2. **File Naming:**
   - Trip leader files can have any name (e.g., "John_Doe.xlsx", "preferences_jane_smith.xlsx")
   - The two status files MUST be named exactly:
     - `TripStatusInfo.xlsx`
     - `TLPromotionStatus.xlsx`

3. **Number of Trips:** The number of trip preferences in each leader file must match:
   - The number of trips in TripStatusInfo.xlsx
   - The `numTrips` setting in config.yaml
   - Currently set to 47 for Spring 2026

4. **Black Highlighting:** In trip leader preference files, use Excel's "Fill Color" feature with black to indicate unavailability. The system automatically detects black-highlighted cells.

5. **Categories:** The categories in TLPromotionStatus.xlsx must match (or be a subset of) the categories in TripStatusInfo.xlsx.

## Adapting for Your Needs

If your Excel files have a different structure, you can:
1. Modify the cell mappings in `config.yaml`
2. Adjust the `numTrips` value for your semester
3. Change sheet indices if your data is on different sheets

See `config.yaml` for all configurable options.
