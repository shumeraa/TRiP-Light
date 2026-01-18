"""TRiP-Light GUI Application

A simple graphical user interface for non-technical users to process trip
leader preferences without using the command line.

This application provides:
- Simple button-based interface
- Progress indicators
- Clear error messages
- Automatic output folder opening
"""

import os
import sys
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import traceback

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

import config
from functions import (
    outputNumericalQuestions,
    outputPrefsHighlightOnLeader,
    outputShortAnswerQuestions,
    process_all_pref_files,
    process_leader_status_file,
    process_trip_status_file,
)
from tripLeaderManager import TripLeaderManager
from tripManager import TripManager


class TripLightGUI:
    """Main GUI application for TRiP-Light."""

    def __init__(self, root):
        self.root = root
        self.root.title("TRiP-Light - Trip Leader Preference Processor")
        self.root.geometry("700x600")
        self.root.resizable(False, False)

        # Configure styles
        self.setup_styles()

        # Create main container
        main_frame = ttk.Frame(root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(
            main_frame,
            text="TRiP-Light Preference Processor",
            font=('Arial', 18, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Instructions
        instructions = (
            "This tool processes trip leader preference files and generates assignment reports.\n\n"
            "Before you start, please ensure:\n"
            "  1. All preference files (.xlsx) are in the 'Data' folder\n"
            "  2. TripStatusInfo.xlsx is in the 'Data' folder\n"
            "  3. TLPromotionStatus.xlsx is in the 'Data' folder\n"
            "  4. Each preference file has exactly 1 empty row at the top\n\n"
            "Click 'Process Files' to begin."
        )

        inst_frame = ttk.LabelFrame(main_frame, text="Instructions", padding="10")
        inst_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        inst_label = ttk.Label(inst_frame, text=instructions, justify=tk.LEFT)
        inst_label.grid(row=0, column=0, sticky=(tk.W, tk.E))

        # Status section
        status_frame = ttk.LabelFrame(main_frame, text="Status", padding="10")
        status_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(0, 20))

        # Status text area
        self.status_text = scrolledtext.ScrolledText(
            status_frame,
            height=12,
            width=70,
            state='disabled',
            font=('Courier', 9)
        )
        self.status_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Progress bar
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=3, column=0, columnspan=2, pady=(0, 20))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=4, column=0, columnspan=2)

        self.process_button = ttk.Button(
            button_frame,
            text="Process Files",
            command=self.start_processing,
            style='Action.TButton'
        )
        self.process_button.grid(row=0, column=0, padx=5)

        self.open_output_button = ttk.Button(
            button_frame,
            text="Open Output Folder",
            command=self.open_output_folder,
            state='disabled'
        )
        self.open_output_button.grid(row=0, column=1, padx=5)

        self.quit_button = ttk.Button(
            button_frame,
            text="Exit",
            command=self.root.quit
        )
        self.quit_button.grid(row=0, column=2, padx=5)

        # Initial status message
        self.log_message("Ready to process files.")
        self.log_message("Please ensure all required files are in the 'Data' folder.")

    def setup_styles(self):
        """Configure custom styles for the GUI."""
        style = ttk.Style()
        style.configure('Action.TButton', font=('Arial', 10, 'bold'))

    def log_message(self, message):
        """Add a message to the status text area."""
        self.status_text.config(state='normal')
        self.status_text.insert(tk.END, message + '\n')
        self.status_text.see(tk.END)
        self.status_text.config(state='disabled')
        self.root.update_idletasks()

    def clear_log(self):
        """Clear the status text area."""
        self.status_text.config(state='normal')
        self.status_text.delete(1.0, tk.END)
        self.status_text.config(state='disabled')

    def validate_setup(self):
        """Validate that all required files and folders exist."""
        errors = []

        # Check if Data folder exists
        if not os.path.exists('Data'):
            errors.append("Error: 'Data' folder not found. Please create it and add your files.")

        # Check if output folder exists, create if not
        if not os.path.exists('output'):
            try:
                os.makedirs('output')
                self.log_message("Created 'output' folder.")
            except Exception as e:
                errors.append(f"Error: Could not create 'output' folder: {str(e)}")

        # Check for required files
        if os.path.exists('Data'):
            required_files = ['TripStatusInfo.xlsx', 'TLPromotionStatus.xlsx']
            for file in required_files:
                file_path = os.path.join('Data', file)
                if not os.path.exists(file_path):
                    errors.append(f"Error: Required file '{file}' not found in 'Data' folder.")

            # Check for at least one preference file
            pref_files = [
                f for f in os.listdir('Data')
                if f.endswith('.xlsx')
                and not f.startswith('~')
                and f not in required_files
            ]

            if not pref_files:
                errors.append(
                    "Error: No preference files (.xlsx) found in 'Data' folder.\n"
                    "       Please add at least one trip leader preference file."
                )

        # Check config.yaml
        if not os.path.exists('config.yaml'):
            errors.append("Error: 'config.yaml' file not found. This file is required for configuration.")

        return errors

    def start_processing(self):
        """Start the file processing in a separate thread."""
        # Validate setup first
        errors = self.validate_setup()
        if errors:
            error_message = '\n'.join(errors)
            messagebox.showerror("Setup Error", error_message)
            for error in errors:
                self.log_message(error)
            return

        # Disable button and start processing
        self.process_button.config(state='disabled')
        self.open_output_button.config(state='disabled')
        self.clear_log()
        self.progress.start(10)

        # Run processing in separate thread to keep GUI responsive
        thread = threading.Thread(target=self.process_files, daemon=True)
        thread.start()

    def process_files(self):
        """Process all preference files and generate outputs."""
        try:
            self.log_message("=" * 70)
            self.log_message("Starting TRiP-Light processing...")
            self.log_message("=" * 70)

            # Load configuration
            self.log_message("\nStep 1: Loading configuration from config.yaml...")
            prefsSheetIndex = config.prefsSheetIndex
            tripLeaderInfoIndex = config.tripLeaderInfoIndex
            folderPath = config.folderPath
            self.log_message(f"  Configuration loaded successfully.")
            self.log_message(f"  Number of trips: {config.numTrips}")
            self.log_message(f"  Data folder: {folderPath}")

            # Initialize managers
            self.log_message("\nStep 2: Initializing data managers...")
            trip_leader_manager = TripLeaderManager(config.leaderInfoDict)
            trip_manager = TripManager(config.tripInfoDict)
            self.log_message("  Managers initialized successfully.")

            # Extract file paths
            tripStatusFileName = trip_manager.cell_mappings["tripStatusFileName"]
            leaderGuideStatusFileName = trip_leader_manager.cell_mappings["leaderGuideStatusFileName"]

            # Process preference files
            self.log_message("\nStep 3: Processing trip leader preference files...")
            process_all_pref_files(
                trip_leader_manager,
                prefsSheetIndex,
                tripLeaderInfoIndex,
                leaderGuideStatusFileName,
                tripStatusFileName,
                folderPath,
            )
            num_leaders = len(trip_leader_manager.get_all_trip_leaders())
            self.log_message(f"  Processed {num_leaders} trip leader(s) successfully.")

            # Load trip information
            self.log_message("\nStep 4: Loading trip information from TripStatusInfo.xlsx...")
            process_trip_status_file(trip_manager)
            num_trips = len(trip_manager.get_trips())
            self.log_message(f"  Loaded {num_trips} trip(s) successfully.")

            # Load leader guide status
            self.log_message("\nStep 5: Loading leader guide status from TLPromotionStatus.xlsx...")
            process_leader_status_file(trip_leader_manager, trip_manager)
            self.log_message("  Guide status loaded successfully.")

            # Generate output files
            self.log_message("\nStep 6: Generating output files...")

            self.log_message("  Creating prefsOutput.xlsx...")
            outputPrefsHighlightOnLeader(trip_leader_manager, trip_manager)

            self.log_message("  Creating numericalQuestionsOutput.xlsx...")
            outputNumericalQuestions(trip_leader_manager)

            self.log_message("  Creating shortAnswerQuestionsOutput.xlsx...")
            outputShortAnswerQuestions(trip_leader_manager)

            self.log_message("\n" + "=" * 70)
            self.log_message("SUCCESS! All files processed successfully.")
            self.log_message("=" * 70)
            self.log_message("\nOutput files created in 'output' folder:")
            self.log_message("  - prefsOutput.xlsx")
            self.log_message("  - numericalQuestionsOutput.xlsx")
            self.log_message("  - shortAnswerQuestionsOutput.xlsx")

            # Show success dialog
            self.root.after(0, lambda: messagebox.showinfo(
                "Success",
                f"Processing complete!\n\n"
                f"Processed {num_leaders} trip leaders and {num_trips} trips.\n\n"
                f"Output files have been created in the 'output' folder."
            ))

            # Enable open output button
            self.root.after(0, lambda: self.open_output_button.config(state='normal'))

        except FileNotFoundError as e:
            error_msg = f"File Not Found Error:\n\n{str(e)}\n\nPlease make sure all required files are in the 'Data' folder."
            self.log_message(f"\nERROR: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("File Not Found", error_msg))

        except ValueError as e:
            error_msg = f"Data Validation Error:\n\n{str(e)}\n\nPlease check your input files for errors."
            self.log_message(f"\nERROR: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Validation Error", error_msg))

        except PermissionError as e:
            error_msg = (
                f"Permission Error:\n\n"
                f"Could not write to output files. Please make sure:\n"
                f"1. The output folder is not read-only\n"
                f"2. Output files are not currently open in Excel\n\n"
                f"Details: {str(e)}"
            )
            self.log_message(f"\nERROR: {error_msg}")
            self.root.after(0, lambda: messagebox.showerror("Permission Error", error_msg))

        except Exception as e:
            error_msg = f"An unexpected error occurred:\n\n{str(e)}\n\nPlease check the status log for details."
            self.log_message(f"\nERROR: Unexpected error occurred:")
            self.log_message(f"{traceback.format_exc()}")
            self.root.after(0, lambda: messagebox.showerror("Error", error_msg))

        finally:
            # Re-enable button and stop progress bar
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.process_button.config(state='normal'))

    def open_output_folder(self):
        """Open the output folder in the system file explorer."""
        output_path = os.path.abspath('output')

        try:
            if sys.platform == 'win32':
                os.startfile(output_path)
            elif sys.platform == 'darwin':  # macOS
                os.system(f'open "{output_path}"')
            else:  # Linux and other Unix-like
                os.system(f'xdg-open "{output_path}"')
        except Exception as e:
            messagebox.showerror(
                "Error",
                f"Could not open output folder:\n{str(e)}\n\nFolder location: {output_path}"
            )


def main():
    """Main entry point for the GUI application."""
    root = tk.Tk()
    app = TripLightGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
