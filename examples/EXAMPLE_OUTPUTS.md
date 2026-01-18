# Example Outputs

This document describes what the output files look like after processing trip leader preferences.

## Output Files

After running TRiP-Light, three Excel files are generated in the `output` folder:

### 1. prefsOutput.xlsx - Color-Coded Preferences

This file shows all trip leader preferences in a grid format with color coding based on guide status.

**Structure:**
- **Column A:** Trip dates
- **Column B:** Trip names
- **Column C:** Trip categories
- **Columns D onward:** One column per trip leader with their preference rankings

**Color Coding:**
- **Purple cells:** Trip leader is a Lead Guide (LG) for this trip category
- **Pink cells:** Trip leader is an Assistant Guide (AG) for this trip category
- **Black cells:** Trip leader is unavailable for this trip (marked as unavailable in their preference file)
- **White cells:** No special status

**Example:**

| Dates | Trip Name | Category | John Doe | Jane Smith |
|-------|-----------|----------|----------|------------|
| Oct 12-14 | Backpacking: White Mountains | Backpacking | 1 (Purple) | 3 (Pink) |
| Oct 19-21 | Rock Climbing: Rumney | Climbing | 4 (Pink) | 1 (Purple) |
| Oct 26-28 | Paddling: Connecticut River | Paddling | (Black) | 2 (Purple) |
| Nov 2-4 | Backpacking: Presidential Range | Backpacking | 2 (Purple) | (Black) |
| Nov 9-11 | Ice Climbing: Frankenstein Cliff | Climbing | 3 (Pink) | 4 (Purple) |

**How to Use This File:**
1. Sort by category or dates to group similar trips
2. Look for trips where you need Lead Guides (purple cells)
3. Consider preferences (lower numbers = higher preference)
4. Black cells indicate absolute unavailability
5. Use this to make initial trip assignments

---

### 2. numericalQuestionsOutput.xlsx - Numerical Data

This file contains all numerical responses from trip leader questionnaires in a table format.

**Structure:**
- **Column A:** Trip leader name
- **Column B:** Semesters left at institution
- **Column C:** Trip satisfaction (1-5 scale from previous semester)
- **Column D:** Number of trips assigned last semester
- **Column E:** Number of trips dropped last semester
- **Column F:** Number of trips picked up last semester
- **Column G:** Number of trips cancelled last semester

**Example:**

| Name | Semesters Left | Trip Satisfaction | Trips Assigned | Trip Dropped | Trip Picked Up | Trip Cancelled |
|------|----------------|-------------------|----------------|--------------|----------------|----------------|
| john doe | 3 | 5 | 2 | 0 | 1 | 0 |
| jane smith | 4 | 5 | 3 | 0 | 0 | 0 |

**How to Use This File:**
1. Identify leaders with limited time remaining (fewer semesters left)
2. Consider satisfaction scores when making assignments
3. Note leaders who dropped trips (may indicate overcommitment)
4. Note leaders who picked up trips (shows reliability)
5. Use this data to balance workload across leaders

---

### 3. shortAnswerQuestionsOutput.xlsx - Text Responses

This file contains all text responses from trip leader questionnaires.

**Structure:**
- **Column A:** Trip leader name
- **Column B:** Trip involvement (historical context)
- **Column C:** Main goal for the semester
- **Column D:** Interested categories
- **Column E:** Three leaders they'd like to work with
- **Column F:** Additional notes

**Example:**

| Name | Trip Involvement | Main Goal | Interested Categories | Three Leaders | Additional Notes |
|------|------------------|-----------|----------------------|---------------|------------------|
| john doe | (historical field, may be empty) | Gain more experience leading technical climbs | Climbing, Backpacking | Alice Johnson, Bob Wilson, Carol Davis | Excited for the semester! |
| jane smith | (historical field, may be empty) | Develop paddling skills | Paddling, Climbing | Emily Brown, Frank Miller, Grace Lee | Available for any weekend trips |

**How to Use This File:**
1. Read main goals to understand each leader's priorities
2. Match leaders with trips in categories they're interested in
3. Consider pairing leaders who want to work together
4. Read additional notes for special considerations (availability, skills, etc.)
5. Use this qualitative data alongside the quantitative preference data

---

## Tips for Using the Outputs

### Making Assignments

1. **Start with the Color-Coded File (prefsOutput.xlsx):**
   - Open in Excel and freeze the first row and first 3 columns for easy navigation
   - Sort by date to work through trips chronologically
   - Look for trips that need Lead Guides (purple cells)

2. **Consider Multiple Factors:**
   - Preference ranking (1 = first choice, higher numbers = lower preference)
   - Guide status (purple = LG, pink = AG)
   - Availability (avoid black cells - these are hard no's)
   - Goals and interests from text responses
   - Workload balance from numerical data

3. **Document Your Decisions:**
   - Add a new column to prefsOutput.xlsx for assignments
   - Mark each trip with assigned leaders
   - Note any special considerations

### Common Workflows

**Scenario 1: Assign a Backpacking Trip**
1. Look at the backpacking trip row in prefsOutput.xlsx
2. Identify leaders with purple cells (Lead Guides for Backpacking)
3. Among those, find the lowest preference number (highest interest)
4. Check numericalQuestionsOutput.xlsx to ensure not overloaded
5. Check shortAnswerQuestionsOutput.xlsx for any relevant notes

**Scenario 2: Find Leaders to Pair**
1. Open shortAnswerQuestionsOutput.xlsx
2. Look at the "Three Leaders" column
3. Find mutual preferences (Leader A wants to work with Leader B, and vice versa)
4. Check prefsOutput.xlsx to find trips they both ranked highly
5. Verify compatible guide status (need at least one Lead Guide)

**Scenario 3: Balance Workload**
1. Open numericalQuestionsOutput.xlsx
2. Note how many trips each leader was assigned last semester
3. Prioritize leaders with fewer assignments (distribute opportunities)
4. Consider semesters left (give more trips to leaders leaving soon)
5. Check satisfaction scores (happy leaders are more likely to stay engaged)

---

## Understanding the Color Codes

The color coding in prefsOutput.xlsx is based on guide status:

- **Purple (Lead Guide):** This leader is qualified to lead trips in this category
  - Can be the primary trip leader
  - Has demonstrated competence and experience
  - Can supervise Assistant Guides

- **Pink (Assistant Guide):** This leader can assist but needs an LG partner
  - Gaining experience in this category
  - Should be paired with a Lead Guide
  - Cannot lead alone in this category

- **Black (Unavailable):** Hard constraint - leader cannot do this trip
  - May have classes, exams, or other commitments
  - Should not be assigned to this trip
  - Marked by the leader in their preference file

- **White (No Special Status):** No guide status for this category
  - May be interested in trying a new activity
  - Would need significant supervision
  - Not recommended as primary leader for this category

---

## Frequently Asked Questions

**Q: Why are some cells empty?**
A: Empty cells typically mean the leader left that field blank in their questionnaire.

**Q: What if everyone marks a trip as unavailable (all black)?**
A: You may need to reach out to leaders individually or adjust the trip date.

**Q: Can I edit the output files?**
A: Yes! The output files are standard Excel files. You can add columns, sort, filter, and annotate as needed. Many users add an "Assigned Leaders" column to track decisions.

**Q: What if two leaders have the same preference number?**
A: Consider their guide status first (prefer LG for leadership positions), then look at their goals and past assignments to make a fair decision.

**Q: How do I handle leaders with no guide status?**
A: They can still participate as co-leaders or in supporting roles. Consider pairing them with experienced LGs for development opportunities.
