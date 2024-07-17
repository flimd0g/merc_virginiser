import tkinter as tk
from tkinter import filedialog, messagebox

def virginise_file():
    # Open a file dialog to select the file
    file_name = filedialog.askopenfilename(title="Select the .bin file",
                                           filetypes=(("BIN files", "*.bin"), ("All files", "*.*")))

    if not file_name:
        return

    # get VIN code from file name
    vin_code = file_name.split("/")[-1].split("_")[0].encode()
    virginised_vin_code = b"AAAAAAAAAAAAAAAAA"

    try:
        # Read the file contents
        with open(file_name, 'rb') as file:
            file_content = file.read()

        # replace vin_code with virginised_vin_code
        virgin_file_content = file_content.replace(vin_code, virginised_vin_code)

        # Generate new filename for virginised content
        VIN_STR = vin_code.decode()
        VIRG_STR = "AAAAAAAAAAAAAAAAA"
        new_file_name = file_name.replace(VIN_STR, VIRG_STR)

        # Write the virginised content to a new file
        with open(new_file_name, 'wb') as new_file:
            new_file.write(virgin_file_content)

        new_file_name = new_file_name.split("/")[-1]

        messagebox.showinfo("Success",f"File virginised successfully. Saved as {new_file_name}")

        root.destroy()

    except FileNotFoundError:
        messagebox.showerror("Error", f"File {file_name} not found.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Create the main window
root = tk.Tk()
root.title("Virginise BIN File")

# Set window size
root.geometry("150x75")

# Add a button to trigger the virginise function
virginise_button = tk.Button(root, text="Virginise File", command=virginise_file)
virginise_button.pack(pady=20)

# Run the Tkinter event loop
root.mainloop()