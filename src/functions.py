import os
import pandas as pd
import math
from tripLeaderManager import TripLeaderManager, TripLeader
from openpyxl import load_workbook
from openpyxl.styles import Font, Alignment, PatternFill
from openpyxl.utils import get_column_letter
from io import BytesIO


def create_leader(
    prefsDF,
    tripLeaderDF,
    trip_leader_manager,
    file_path,
):
    # Name and prefs
    name, prefs = get_leader_name_and_prefs(
        prefsDF, tripLeaderDF, trip_leader_manager, file_path
    )

    # Numerical questions
    (
        semestersLeft,
        tripSatisfaction,
        tripsAssigned,
        tripDropped,
        tripPickedUp,
        tripCancelled,
    ) = getNumericalQuestions(
        tripLeaderDF,
        trip_leader_manager,
        file_path,
    )

    # Short answer questions
    (
        tripInvolvement,
        mainGoal,
        interestedCategories,
        threeLeaders,
        leadershipStyle,
        additionalNotes,
    ) = getShortAnswerQuestions(tripLeaderDF, trip_leader_manager, file_path)

    leader = TripLeader(
        name,
        prefs,
        semestersLeft,
        tripSatisfaction,
        tripsAssigned,
        tripDropped,
        tripPickedUp,
        tripCancelled,
        tripInvolvement,
        mainGoal,
        interestedCategories,
        threeLeaders,
        leadershipStyle,
        additionalNotes,
    )

    trip_leader_manager.add_trip_leader(leader)


def getShortAnswerQuestions(
    tripLeaderDF,
    trip_leader_manager,
    file_path,
):
    # combine the three cells into one string, and remove any empty cells
    def combineThreeCells(listOfThreeCells):
        return ", ".join(
            [
                tripLeaderDF.iloc[cell[0], cell[1]]
                for cell in listOfThreeCells
                if not pd.isnull(tripLeaderDF.iloc[cell[0], cell[1]])
            ]
        )

    tripInvolvementXY = trip_leader_manager.cell_mappings["tripInvolvementCell"]
    mainGoalXY = trip_leader_manager.cell_mappings["mainGoalCell"]
    interestedCategoriesXY = trip_leader_manager.cell_mappings[
        "interestedCategoriesCell"
    ]
    threeLeadersXY = trip_leader_manager.cell_mappings["threeLeadersCell"]
    leadershipStyleXY = trip_leader_manager.cell_mappings["leadershipStyleCell"]
    additionalNotesXY = trip_leader_manager.cell_mappings["additionalNotesCell"]

    tripInvolvement = tripLeaderDF.iloc[tripInvolvementXY[0], tripInvolvementXY[1]]
    mainGoal = tripLeaderDF.iloc[mainGoalXY[0], mainGoalXY[1]]
    interestedCategories = tripLeaderDF.iloc[
        interestedCategoriesXY[0], interestedCategoriesXY[1]
    ]
    # since additional notes is the last row, if it is empty it will be out of bounds, so check if it is in bounds first
    additionalNotes = (
        tripLeaderDF.iloc[additionalNotesXY[0], additionalNotesXY[1]]
        if additionalNotesXY[0] < len(tripLeaderDF) and additionalNotesXY[1] < len(tripLeaderDF.columns)
        else None
    )
    
    threeLeaders = combineThreeCells(threeLeadersXY)
    leadershipStyle = combineThreeCells(leadershipStyleXY)

    allShortAnswerQuestions = [
        tripInvolvement,
        mainGoal,
        interestedCategories,
        threeLeaders,
        leadershipStyle,
        additionalNotes,
    ]

    # if any of the questions are empty, print a warning and set them to an empty string
    for question in allShortAnswerQuestions:
        if pd.isnull(question):
            print(
                f"Warning: A short answer question is empty in {file_path}. Setting to empty string."
            )
            question = ""

    return (
        tripInvolvement,
        mainGoal,
        interestedCategories,
        threeLeaders,
        leadershipStyle,
        additionalNotes,
    )


def getNumericalQuestions(
    tripLeaderDF,
    trip_leader_manager,
    file_path,
):

    semestersLeftXY = trip_leader_manager.cell_mappings["semestersLeftCell"]
    tripSatisfactionXY = trip_leader_manager.cell_mappings["tripSatisfactionCell"]
    tripsAssignedXY = trip_leader_manager.cell_mappings["tripsAssignedCell"]
    tripDroppedXY = trip_leader_manager.cell_mappings["tripDropCell"]
    tripPickedUpXY = trip_leader_manager.cell_mappings["tripPickupCell"]
    tripCancelledXY = trip_leader_manager.cell_mappings["tripCancelledCell"]

    semestersLeft = tripLeaderDF.iloc[semestersLeftXY[0], semestersLeftXY[1]]
    tripSatisfaction = tripLeaderDF.iloc[tripSatisfactionXY[0], tripSatisfactionXY[1]]
    tripsAssigned = tripLeaderDF.iloc[tripsAssignedXY[0], tripsAssignedXY[1]]
    tripDropped = tripLeaderDF.iloc[tripDroppedXY[0], tripDroppedXY[1]]
    tripPickedUp = tripLeaderDF.iloc[tripPickedUpXY[0], tripPickedUpXY[1]]
    tripCancelled = tripLeaderDF.iloc[tripCancelledXY[0], tripCancelledXY[1]]

    allNumericalQuestions = [
        semestersLeft,
        tripSatisfaction,
        tripsAssigned,
        tripDropped,
        tripPickedUp,
        tripCancelled,
    ]

    # if any of the questions are empty, print a warning and set them to 0
    # use pandas isnull to check if the value is NaN
    for question in allNumericalQuestions:
        if pd.isnull(question):
            print(f"Warning: Numerical question is empty in {file_path}. Setting to 0.")
            question = 0

    return (
        semestersLeft,
        tripSatisfaction,
        tripsAssigned,
        tripDropped,
        tripPickedUp,
        tripCancelled,
    )


def get_leader_name_and_prefs(
    prefsDF,
    tripLeaderDF,
    trip_leader_manager,
    file_path,
):

    nameXY = trip_leader_manager.cell_mappings["nameCell"]
    prefXY = trip_leader_manager.cell_mappings["leaderPrefsCell"]
    tripXY = trip_leader_manager.cell_mappings["leaderTripCell"]
    numberOfTrips = trip_leader_manager.cell_mappings["numTrips"]

    name = tripLeaderDF.iloc[nameXY[0], nameXY[1]]
    name = (
        name.lower().strip()
    )  # make name lowercase and remove any leading/trailing whitespace

    currentRow = prefXY[0] + 1

    prefs = []

    # while the corresponding trip is not empty, add the preferences to the list
    while currentRow < len(prefsDF) and not pd.isnull(
        prefsDF.iloc[currentRow, tripXY[1]]
    ):
        prefs.append(prefsDF.iloc[currentRow, prefXY[1]])
        currentRow += 1

    if pd.isnull(name):
        raise ValueError(f"Error: Name is empty in {file_path}.")
    if not isinstance(name, str):
        raise ValueError(f"Error: Name is not a string in {file_path}.")

    # check that the number of prefs matches the number of trips, return for this
    if len(prefs) != numberOfTrips:
        raise ValueError(
            f"Error: Number of preferences does not match number of trips in {file_path}."
        )

    # make sure there are no repeating numbers in the prefs, excluding pd.isnull values
    repeatedPrefs = [
        pref for pref in prefs if not pd.isnull(pref) and prefs.count(pref) > 1
    ]
    if repeatedPrefs:
        # raise ValueError(
        #     f"Error: Repeating preferences in {file_path}. Repeated preferences: {repeatedPrefs}."
        # )
        print(
            f"Error: Repeating preferences in {file_path}. Repeated preferences: {repeatedPrefs}."
        )

    return name, prefs


def addTrips(trip_manager, tripDF, file_path):

    dateXY = trip_manager.cell_mappings["datesCell"]
    tripXY = trip_manager.cell_mappings["tripCell"]
    categoryXY = trip_manager.cell_mappings["tripCategoryCell"]
    numberOfTrips = trip_manager.cell_mappings["numTrips"]

    # iterate through the rows of the tripDF, adding each trip date and name to the trip_manager
    currentRow = dateXY[0] + 1

    while currentRow < len(tripDF) and not pd.isnull(
        tripDF.iloc[currentRow, dateXY[1]]
    ):
        name = tripDF.iloc[currentRow, tripXY[1]]
        date = tripDF.iloc[currentRow, dateXY[1]]
        category = tripDF.iloc[currentRow, categoryXY[1]]
        trip_manager.add_trip(name, date, category)
        currentRow += 1

    # return if that the number of trips added matches the number of trips in the tripDF

    if len(trip_manager.get_trips()) != numberOfTrips:
        print(
            f"Error: Number of trips added does not match number of trips in {file_path}. Expected {numberOfTrips}, got {len(trip_manager.get_trips())}."
        )
        raise


def addLeaderGuideStatus(guideStatusDF, trip_leader_manager, trip_manager):
    nameCellGuideStatus = trip_leader_manager.cell_mappings["nameCellGuideStatus"]
    firstPromotionalCategoryCell = trip_leader_manager.cell_mappings[
        "firstPromotionalCategoryCell"
    ]

    # first, get all of the available guide categories
    availableGuideCategories = []
    currentCategoryCol = firstPromotionalCategoryCell[1]
    # iterate from the first category to the first empty col
    while currentCategoryCol < len(guideStatusDF.columns) and not pd.isnull(
        guideStatusDF.iloc[firstPromotionalCategoryCell[0], currentCategoryCol]
    ):
        category = guideStatusDF.iloc[
            firstPromotionalCategoryCell[0], currentCategoryCol
        ]
        category.lower().strip()
        availableGuideCategories.append(category)
        currentCategoryCol += 1

    trip_categories = trip_manager.get_available_categories()

    if not set(availableGuideCategories).issubset(set(trip_categories)):
        raise ValueError(
            f"Guide categories in the guide status doc do not match the trip categories. Guide categories: {availableGuideCategories}, Trip categories: {trip_categories}."
        )

    print("The categories are: ", availableGuideCategories)

    # now iterate through every leader to get their guide status and add it to their leader object
    # if the cell has LG, set status to 1, if anything else, set status to 0
    currentLeaderRow = nameCellGuideStatus[0] + 1  # skip the header row
    while currentLeaderRow < len(guideStatusDF) and not pd.isnull(
        guideStatusDF.iloc[currentLeaderRow, nameCellGuideStatus[1]]
    ):
        name = guideStatusDF.iloc[currentLeaderRow, nameCellGuideStatus[1]]
        name = name.lower().strip()

        leaderObject = trip_leader_manager.find_trip_leader(name)

        if leaderObject != None:
            # the leader exists, so we can add the guide status to them
            guideStatusDict = {}
            currentCategoryCol = firstPromotionalCategoryCell[1]
            for category in availableGuideCategories:
                guideStatus = guideStatusDF.iloc[currentLeaderRow, currentCategoryCol]

                if isinstance(guideStatus, str):
                    guideStatus = guideStatus.lower().strip()

                if guideStatus == "lg":
                    guideStatusDict[category] = 1
                else:
                    guideStatusDict[category] = 0
                currentCategoryCol += 1

            leaderObject.guideStatus = guideStatusDict
            currentLeaderRow += 1
        else:
            print(
                f" WARNING:Leader {name} from the leader guide status doc does not match any leaders from the prefs."
            )
            currentLeaderRow += 1


def process_all_pref_files(
    trip_leader_manager,
    prefsSheetIndex,
    tripLeaderInfoIndex,
    leaderGuideStatusFileName,
    tripStatusFileName,
    folder_path="Data",
):
    if not os.path.exists(folder_path):
        print("Folder does not exist.")
        return

    files = [
        f
        for f in os.listdir(folder_path)
        if f.endswith(".xlsx")
        and not f.startswith("~")
        and os.path.basename(f) != os.path.basename(leaderGuideStatusFileName)
        and os.path.basename(f) != os.path.basename(tripStatusFileName)
    ]

    if not files:
        print("No valid Excel files found in the folder.")
        return

    for index, file_name in enumerate(files):
        file_path = os.path.join(folder_path, file_name)

        # Checking if the file is empty
        try:

            df = pd.ExcelFile(file_path, engine="openpyxl")
            sheetNames = df.sheet_names
            prefsDF = pd.read_excel(file_path, sheet_name=sheetNames[prefsSheetIndex])
            # modified_file = remove_black_highlighted_cells_in_column(file_path, sheetNames[prefsSheetIndex], prefXY[1])
            tripLeaderDF = pd.read_excel(
                file_path, sheet_name=sheetNames[tripLeaderInfoIndex]
            )

            if prefsDF.empty or tripLeaderDF.empty:
                print(f"File {file_name} has an empty sheet, skipping.")
                raise
        except Exception as e:
            print(f"Could not read {file_name}: {e}")
            raise

        # fix this to use all create_leader params
        create_leader(
            prefsDF,
            tripLeaderDF,
            trip_leader_manager,
            file_path,
        )


def process_leader_status_file(trip_leader_manager, trip_manager):
    file_path = trip_leader_manager.cell_mappings["leaderGuideStatusFileName"]

    try:
        guideStatusExcel = pd.ExcelFile(file_path, engine="openpyxl")
        guideStatusDF = pd.read_excel(guideStatusExcel, sheet_name=0)

        if guideStatusDF.empty:
            print(f"File {file_path} has an empty sheet")
            raise
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        raise

    addLeaderGuideStatus(
        guideStatusDF,
        trip_leader_manager,
        trip_manager,
    )


def process_trip_status_file(trip_manager):
    file_path = trip_manager.cell_mappings["tripStatusFileName"]

    try:
        tripStatusExcel = pd.ExcelFile(file_path, engine="openpyxl")
        tripStatusDF = pd.read_excel(tripStatusExcel, sheet_name=0)

        if tripStatusDF.empty:
            print(f"File {file_path} has an empty sheet")
            raise
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        raise

    addTrips(trip_manager, tripStatusDF, file_path)


def createExcelFileHighlighedOnThirds(trip_leader_manager, trip_manager):
    outputFileName = "output/output.xlsx"

    # if output file already exists, delete it
    try:
        if os.path.exists(outputFileName):
            os.remove(outputFileName)
    except Exception as e:
        print("Error: Cannot have the file open. Details:", e)

    # create an empty dataframe with "Dates" and "TRiP" as columns
    df = pd.DataFrame(columns=["Dates", "TRiP"])

    # populate the first and second columns with trip dates and names
    trip_data = [
        {"Dates": trip.date, "TRiP": trip.name} for trip in trip_manager.get_trips()
    ]
    df = pd.concat([df, pd.DataFrame(trip_data)], ignore_index=True)

    # populate the rest of the columns with the header of the trip leader name, and underneath their preferences
    for leader in trip_leader_manager.get_all_trip_leaders():
        # Ensure the list of preferences is the same length as the number of trips
        prefs = leader.prefs + [None] * (len(df) - len(leader.prefs))
        df[leader.name] = prefs

    # write the dataframe to an excel file
    df.to_excel(outputFileName, index=False)

    # Load the workbook and select the active worksheet
    wb = load_workbook(outputFileName)
    ws = wb.active

    # Bold the headers and center all cells
    header_font = Font(bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")

    # Apply formatting to headers
    for cell in ws[1]:  # First row (headers)
        cell.font = header_font
        cell.alignment = center_alignment

    # Colors for different categories
    color_map = {
        "bottom third": PatternFill(
            start_color="00FF00", end_color="00FF00", fill_type="solid"
        ),  # Red
        "middle third": PatternFill(
            start_color="FFFF00", end_color="FFFF00", fill_type="solid"
        ),  # Yellow
        "top third": PatternFill(
            start_color="FF0000", end_color="FF0000", fill_type="solid"
        ),  # Green
        "nan": PatternFill(
            start_color="000000", end_color="000000", fill_type="solid"
        ),  # Black
    }

    # Apply center alignment and color based on preference category
    for i, leader in enumerate(
        trip_leader_manager.get_all_trip_leaders(), start=3
    ):  # Columns start from C
        categories = leader.categorize_prefs()
        for row_num, (pref, category) in enumerate(
            categories, start=2
        ):  # Rows start from 2 (first row is header)
            cell = ws.cell(row=row_num, column=i)
            cell.alignment = center_alignment

            if pd.isna(pref):
                cell.fill = color_map["nan"]
            else:
                cell.fill = color_map.get(category, None)

    # Save the formatted Excel file
    wb.save(outputFileName)

    print(f"Excel file '{outputFileName}' created and formatted successfully.")


def outputPrefsHighlightOnLeader(trip_leader_manager, trip_manager):
    outputFileName = "output/prefsOutput.xlsx"

    # if output file already exists, delete it
    try:
        if os.path.exists(outputFileName):
            os.remove(outputFileName)
    except Exception as e:
        print("Error: Cannot have the file open. Details:", e)

    # create an empty dataframe with "Dates", "TRiP", and "Category" as columns
    df = pd.DataFrame(columns=["Dates", "TRiP", "Category"])

    # populate the cols with trip dates, names, and categories
    trip_data = [
        {"Dates": trip.date, "TRiP": trip.name, "Category": trip.category}
        for trip in trip_manager.get_trips()
    ]
    df = pd.concat([df, pd.DataFrame(trip_data)], ignore_index=True)

    # populate the rest of the columns with the header of the trip leader name, and underneath their preferences
    for leader in trip_leader_manager.get_all_trip_leaders():
        # Ensure the list of preferences is the same length as the number of trips
        prefs = leader.prefs + [None] * (len(df) - len(leader.prefs))
        df[leader.name] = prefs

    # write the dataframe to an excel file
    df.to_excel(outputFileName, index=False)

    # Load the workbook and select the active worksheet
    wb = load_workbook(outputFileName)
    ws = wb.active

    # Bold the headers and center all cells
    header_font = Font(bold=True)
    center_alignment = Alignment(horizontal="center", vertical="center")
    purple_fill = PatternFill(
        start_color="D9D2E9", end_color="D9D2E9", fill_type="solid"
    )
    pink_fill = PatternFill(start_color="F4CCCC", end_color="F4CCCC", fill_type="solid")
    black_fill = PatternFill(
        start_color="000000", end_color="000000", fill_type="solid"
    )
    white_font = Font(color="FFFFFF")  # To ensure visibility in black-filled cells

    # Apply formatting to headers
    for cell in ws[1]:  # First row (headers)
        cell.font = header_font
        cell.alignment = center_alignment

    # Highlight cells based on guide status or emptiness
    for row_idx, row in enumerate(
        df.itertuples(index=False), start=2
    ):  # Start from second row
        category = row.Category
        for col_idx, leader in enumerate(
            trip_leader_manager.get_all_trip_leaders(), start=4
        ):  # Start after "Dates", "TRiP", "Category"
            guide_status = leader.guideStatus.get(category, None)
            cell = ws.cell(row=row_idx, column=col_idx)

            if cell.value is None:  # Highlight empty preference cells black
                cell.fill = black_fill
            elif guide_status is not None:
                if guide_status == 1:  # Lead Guide
                    cell.fill = purple_fill
                elif guide_status == 0:  # Assistant Guide
                    cell.fill = pink_fill
                elif pd.isnull(guide_status):
                    raise ValueError(
                        f"Guide status for leader '{leader.name}' in category '{category}' is None."
                    )
            cell.alignment = center_alignment

    # Save the updated workbook
    wb.save(outputFileName)

    print(f"Excel file '{outputFileName}' created and formatted successfully.")


def outputNumericalQuestions(trip_leader_manager):
    outputFileName = "output/numericalQuestionsOutput.xlsx"

    # Remove existing file safely
    if os.path.exists(outputFileName):
        try:
            os.remove(outputFileName)
        except Exception as e:
            print(
                f"Error: Unable to delete the file. Make sure it is closed. Details: {e}"
            )
            return

    # Define column names
    columns = [
        "Name",
        "Semesters Left",
        "Trip Satisfaction",
        "Trips Assigned",
        "Trip Dropped",
        "Trip Picked Up",
        "Trip Cancelled",
    ]

    # Collect data efficiently
    leader_data = [
        {
            "Name": leader.name,
            "Semesters Left": leader.semestersLeft,
            "Trip Satisfaction": leader.tripSatisfaction,
            "Trips Assigned": leader.tripsAssigned,
            "Trip Dropped": leader.tripDropped,
            "Trip Picked Up": leader.tripPickedUp,
            "Trip Cancelled": leader.tripCancelled,
        }
        for leader in trip_leader_manager.get_all_trip_leaders()
    ]

    # Create the DataFrame
    df = pd.DataFrame(leader_data, columns=columns)

    # Write the DataFrame to an Excel file
    try:
        df.to_excel(outputFileName, index=False)
        print(f"Data successfully written to {outputFileName}.")
    except Exception as e:
        print(f"Error: Failed to write to {outputFileName}. Details: {e}")


def outputShortAnswerQuestions(trip_leader_manager):
    outputFileName = "output/shortAnswerQuestionsOutput.xlsx"

    # Remove existing file safely
    if os.path.exists(outputFileName):
        try:
            os.remove(outputFileName)
        except Exception as e:
            print(
                f"Error: Unable to delete the file. Make sure it is closed. Details: {e}"
            )
            return

    # Define column names
    columns = [
        "Name",
        "Trip Involvement",
        "Main Goal",
        "Interested Categories",
        "Three Leaders",
        "Leadership Style",
        "Additional Notes",
    ]

    # Collect data efficiently
    leader_data = [
        {
            "Name": leader.name,
            "Trip Involvement": leader.tripInvolvement,
            "Main Goal": leader.mainGoal,
            "Interested Categories": leader.interestedCategories,
            "Three Leaders": leader.threeLeaders,
            "Leadership Style": leader.leadershipStyle,
            "Additional Notes": leader.additionalNotes,
        }
        for leader in trip_leader_manager.get_all_trip_leaders()
    ]

    # Create the DataFrame
    df = pd.DataFrame(leader_data, columns=columns)

    # Write the DataFrame to an Excel file
    try:
        df.to_excel(outputFileName, index=False)
        print(f"Data successfully written to {outputFileName}.")
    except Exception as e:
        print(f"Error: Failed to write to {outputFileName}. Details: {e}")
