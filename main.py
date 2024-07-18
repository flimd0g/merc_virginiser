import re
import tkinter as tk
from tkinter import filedialog, messagebox
from vin_detector import vin_detector  # Correctly import the vin_detector class

def detect_vins():
    # Open a file dialog to select the file
    file_name = filedialog.askopenfilename(title="Select the .bin file",
                                           filetypes=(("BIN files", "*.bin"), ("All files", "*.*")))

    if not file_name:
        return

    # Create an instance of vin_detector
    detective = vin_detector()

    try:
        # Read the file contents
        with open(file_name, 'rb') as file:
            file_content = file.read()

        # Detect VIN codes in the file content
        detected_vins = detective.detect([file_content.decode('latin-1')])
        if not detected_vins:
            messagebox.showinfo("Info", "No VIN codes detected in the file.")
            return

        # Display detected VINs in the listbox
        vin_listbox.delete(0, tk.END)  # Clear previous entries
        for vin in detected_vins:
            vin_listbox.insert(tk.END, vin)

        # Store the detected VINs and file content for later use
        global selected_file_content, selected_file_name, vins_to_replace
        selected_file_content = file_content
        selected_file_name = file_name
        vins_to_replace = detected_vins

    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_name} not found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def virginise_file():
    if not vins_to_replace:
        messagebox.showinfo("Info", "No VIN codes to virginise.")
        return

    # Ask for user confirmation before proceeding
    if not messagebox.askyesno("Confirm", "Do you want to virginise the detected VINs?"):
        return

    try:
        # Replace detected VIN codes with virginised VIN code
        virginised_vin_code = b"AAAAAAAAAAAAAAAAA"
        virgin_file_content = selected_file_content
        for vin in vins_to_replace:
            virgin_file_content = virgin_file_content.replace(vin.encode('latin-1'), virginised_vin_code)

        # Generate new filename for virginised content
        VIN_STR = vins_to_replace[0]
        VIRG_STR = "AAAAAAAAAAAAAAAAA"
        new_file_name = selected_file_name.replace(VIN_STR, VIRG_STR)

        # Write the virginised content to a new file
        with open(new_file_name, 'wb') as new_file:
            new_file.write(virgin_file_content)

        new_file_name = new_file_name.split("/")[-1]

        messagebox.showinfo("Success", f"File virginised successfully. Saved as {new_file_name}")

        root.destroy()

    except FileNotFoundError:
        messagebox.showerror("Error", f"File {selected_file_name} not found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Virginise BIN File")

# Set window size
root.geometry("300x220")

# Add a button to trigger the detect VINs function
detect_button = tk.Button(root, text="Detect VINs", command=detect_vins)
detect_button.pack(pady=10)

# Add a listbox to display detected VINs
vin_listbox = tk.Listbox(root, width=40, height=7)
vin_listbox.pack(pady=10)

# Add a button to trigger the virginise function
virginise_button = tk.Button(root, text="Virginise File", command=virginise_file)
virginise_button.pack(pady=10)

# Run the Tkinter event loop
root.mainloop()
