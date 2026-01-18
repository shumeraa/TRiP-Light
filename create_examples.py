"""
Script to generate example input files for TRiP-Light.

This creates sample Excel files that demonstrate the expected format:
- Example trip leader preference file
- Example TripStatusInfo.xlsx
- Example TLPromotionStatus.xlsx
"""

import pandas as pd
from openpyxl import load_workbook
from openpyxl.styles import PatternFill

# Sample data
SAMPLE_TRIPS = [
    ("Oct 12-14, 2025", "Backpacking: White Mountains", "Backpacking"),
    ("Oct 19-21, 2025", "Rock Climbing: Rumney", "Climbing"),
    ("Oct 26-28, 2025", "Paddling: Connecticut River", "Paddling"),
    ("Nov 2-4, 2025", "Backpacking: Presidential Range", "Backpacking"),
    ("Nov 9-11, 2025", "Ice Climbing: Frankenstein Cliff", "Climbing"),
]

SAMPLE_LEADERS = [
    ("john doe", {"Backpacking": "LG", "Climbing": "AG", "Paddling": ""}),
    ("jane smith", {"Backpacking": "AG", "Climbing": "LG", "Paddling": "LG"}),
]

CATEGORIES = ["Backpacking", "Climbing", "Paddling"]


def create_trip_status_file():
    """Create example TripStatusInfo.xlsx file."""
    # Create DataFrame with empty first row
    data = {
        "Trip Dates": [""] + [trip[0] for trip in SAMPLE_TRIPS],
        "Trip Name": [""] + [trip[1] for trip in SAMPLE_TRIPS],
        "Category": [""] + [trip[2] for trip in SAMPLE_TRIPS],
    }

    df = pd.DataFrame(data)
    output_path = "examples/Example_TripStatusInfo.xlsx"
    df.to_excel(output_path, index=False, sheet_name="Trip Status")

    print(f"Created: {output_path}")


def create_leader_status_file():
    """Create example TLPromotionStatus.xlsx file."""
    # Create DataFrame with empty first row and category headers
    rows = [
        [""] + [""] * (len(CATEGORIES) + 1),  # Empty row
        ["Name"] + CATEGORIES,  # Headers with categories
    ]

    # Add leader data
    for leader_name, statuses in SAMPLE_LEADERS:
        row = [leader_name] + [statuses.get(cat, "") for cat in CATEGORIES]
        rows.append(row)

    df = pd.DataFrame(rows)
    output_path = "examples/Example_TLPromotionStatus.xlsx"
    df.to_excel(output_path, index=False, header=False, sheet_name="Leader Guide Status")

    print(f"Created: {output_path}")


def create_trip_leader_file(name, prefs, guide_statuses):
    """Create example trip leader preference file."""
    # Create leader info sheet
    leader_info_data = {
        "": [""] * 20,  # Empty first column
        "Question": [
            "",  # Row 1: Empty
            "",  # Row 2: Empty
            "",  # Row 3: Empty
            "Name:",  # Row 4
            "How many semesters do you have left?",  # Row 5
            "Trip satisfaction (1-5):",  # Row 6
            "",  # Row 7
            "Trips assigned last semester:",  # Row 8
            "Trips dropped:",  # Row 9
            "Trips picked up:",  # Row 10
            "",  # Row 11
            "What is your main goal this semester?",  # Row 12
            "Which categories are you most interested in?",  # Row 13
            "",  # Row 14
            "Three leaders you'd like to work with:",  # Row 15
            "",  # Row 16
            "",  # Row 17
            "",  # Row 18
            "Additional notes:",  # Row 19
            "",  # Row 20
        ],
        "Answer": [
            "",  # Row 1: Empty
            "",  # Row 2: Empty
            "",  # Row 3: Empty
            name,  # Row 4
            "3",  # Row 5
            "5",  # Row 6
            "",  # Row 7
            "2",  # Row 8
            "0",  # Row 9
            "1",  # Row 10
            "",  # Row 11
            "Gain more experience leading technical climbs",  # Row 12
            "Climbing, Backpacking",  # Row 13
            "",  # Row 14
            "Alice Johnson",  # Row 15
            "Bob Wilson",  # Row 16
            "Carol Davis",  # Row 17
            "",  # Row 18
            "Excited for the semester!",  # Row 19
            "",  # Row 20
        ],
    }

    # Create preferences sheet with empty first row
    prefs_data = {
        "": [""] + [""] * len(SAMPLE_TRIPS),
        "Trip Dates": [""] + [trip[0] for trip in SAMPLE_TRIPS],
        "Trip Name": [""] + [trip[1] for trip in SAMPLE_TRIPS],
        "Category": [""] + [trip[2] for trip in SAMPLE_TRIPS],
        "Preference": [""] + prefs,
    }

    # Write to Excel
    safe_name = name.replace(" ", "_")
    output_path = f"examples/Example_TripLeader_{safe_name}.xlsx"

    # Create leader info sheet
    df_info = pd.DataFrame(leader_info_data)
    df_prefs = pd.DataFrame(prefs_data)

    with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
        df_info.to_excel(writer, index=False, header=False, sheet_name="Trip Leader Info")
        df_prefs.to_excel(writer, index=False, header=False, sheet_name="Trip Preferences")

    # Add black highlighting to unavailable trips (None preferences)
    wb = load_workbook(output_path)
    ws = wb["Trip Preferences"]

    black_fill = PatternFill(start_color="000000", end_color="000000", fill_type="solid")

    # Apply black fill to None preferences (E column, starting from row 3)
    for i, pref in enumerate(prefs, start=3):  # Start at row 3 (after empty row and header)
        if pref is None:
            ws[f"E{i}"].fill = black_fill

    wb.save(output_path)

    print(f"Created: {output_path}")


def main():
    """Generate all example files."""
    print("Generating example files...")
    print()

    # Create trip status file
    create_trip_status_file()

    # Create leader guide status file
    create_leader_status_file()

    # Create example trip leader files
    # John Doe - Lead Guide for Backpacking, prefers backpacking trips
    create_trip_leader_file(
        "John Doe",
        prefs=[1, 4, None, 2, 3],  # None = unavailable (black highlighted)
        guide_statuses={"Backpacking": "LG", "Climbing": "AG", "Paddling": ""},
    )

    # Jane Smith - Lead Guide for Climbing and Paddling
    create_trip_leader_file(
        "Jane Smith",
        prefs=[3, 1, 2, None, 4],  # None = unavailable
        guide_statuses={"Backpacking": "AG", "Climbing": "LG", "Paddling": "LG"},
    )

    print()
    print("=" * 60)
    print("Example files created successfully!")
    print("=" * 60)
    print()
    print("The files are in the 'examples' folder.")
    print("Copy them to the 'Data' folder to test the application.")
    print()
    print("Note: This example uses 5 trips instead of the default 47.")
    print("To test with these files, temporarily change 'numTrips' in")
    print("config.yaml from 47 to 5, then change it back for real data.")


if __name__ == "__main__":
    main()
