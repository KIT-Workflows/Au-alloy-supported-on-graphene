import os
import shutil
import re
import pandas as pd

# Base directory where the folders are located
base_dir = os.path.dirname(os.path.abspath(__file__)) the correct path

# Output file
output_file = os.path.join(base_dir, "raw_data.txt")

# Function to extract energy from the line "energy  without entropy"
def extract_energy(outcar_path):
    with open(outcar_path, "r") as file:
        for line in file:
            if "energy  without entropy" in line:
                # Extracts the second number from the line
                energy = float(line.split()[6])  # The second number is at index 6
                return energy
    return None

# Open the output file for writing
with open(output_file, "w") as f_out:
    # Write the header
    f_out.write("isomer      tot_energy\n")

    # Iterate through all folders in base_dir
    for root, dirs, files in os.walk(base_dir):
        if "OUTCAR" in files:
            outcar_path = os.path.join(root, "OUTCAR")
            isomer = os.path.basename(root)  # Folder name (isomer)
            energy = extract_energy(outcar_path)

            if energy is not None:
                # Write to the output file
                f_out.write(f"{isomer}      {energy}\n")

# Input file path
input_file = "raw_data.txt"
# Output file path (can be the same as input to overwrite)
output_file = "raw_data_sorted.txt"

# Read the file and store the lines in a list
with open(input_file, "r") as file:
    lines = file.readlines()

# Separate the header from the data
header = lines[0]
data = lines[1:]

# Sort the data based on the "isomer" column (first column)
data_sorted = sorted(data, key=lambda x: x.split()[0])

# Write the sorted data to the output file
with open(output_file, "w") as file:
    file.write(header)  # Write the header
    for line in data_sorted:
        file.write(line)

print(f"Sorted file saved as: {output_file}")

shutil.move("raw_data_sorted.txt", "raw_data.txt")

# Input file path
input_file = "raw_data.txt"
# Output file path
output_file = "raw_data_with_columns.txt"

# Function to extract atomicity
def get_atomicity(isomer):
    if isomer == 'layer':
        pass  # Or any other value that makes sense for 'layer' case
    else:
        # Find all numbers in the isomer name
        cluster = isomer.split("_")[1]
        numbers = re.findall(r"\d+", cluster)
        # Sum the numbers to obtain atomicity
        return sum(int(num) for num in numbers)

# Function to extract composition (number after "au")
def get_composition(isomer):
    # Search for "au" followed by numbers
    match = re.search(r"au(\d+)", isomer)
    if match:
        return int(match.group(1))  # Return the number after "au"
    return 0  # If "au" is not found, return 0

# Open the input file and read the lines
with open(input_file, "r") as file:
    lines = file.readlines()

# Process the lines and add new columns
new_lines = []
header = lines[0].strip()  # Remove newline from header
new_lines.append(f"isomer                          tot_energy    condition    cluster        atomicity    composition\n")  # New header

# Iterate over the lines, starting from the second line
for line in lines[1:]:
    isomer, energy = line.strip().split()  # Separate isomer and energy
    if isomer == 'layer':
        condition = 'none'
        cluster = 'layer'
        atomicity = 'none'  # Atomicity does not apply to 'layer'
        composition = 'none'  # Composition does not apply to 'layer'
    else:
        condition = isomer.split("_")[0]  # Extract condition (ads or vac)
        cluster = isomer.split("_")[1]
        atomicity = get_atomicity(isomer)  # Calculate atomicity
        composition = get_composition(isomer)  # Calculate composition

    # Add the new line with additional columns
    new_lines.append(f"{isomer:<30} {energy:>15} {condition:^10} {cluster:<10} {atomicity:^10} {composition:^10}\n")

# Write the output file
with open(output_file, "w") as file:
    file.writelines(new_lines)

print(f"File with additional columns saved as: {output_file}")

# Load the data
file_path = f"{output_file}"  # Replace with the correct file path
df = pd.read_csv(file_path, delim_whitespace=True)

# Separate data into "vac" and "ads"
df_ads = df[df["condition"] == "ads"].copy()
df_vac = df[df["condition"] == "vac"].copy()
layer_energy = df[df["condition"] == "none"]["tot_energy"].values[0]  # Layer energy

# Create dictionary for quick access to vacuum cluster energies
vac_energy_dict = df_vac.set_index("cluster")["tot_energy"].to_dict()

# Calculate E_ads
df_ads["E_ads"] = df_ads["tot_energy"] - df_ads["cluster"].map(vac_energy_dict).fillna(0) - layer_energy

# Save formatted results
with open("df_ads.txt", "w") as f:
    f.write(f"isomer                          tot_energy    condition    cluster        atomicity    composition    E_ads\n")
    for _, row in df_ads.iterrows():
        f.write(f"{row['isomer']:<30} {row['tot_energy']:>15.8f} {row['condition']:^10} {row['cluster']:<10} {row['atomicity']:^10} {row['composition']:^10} {row['E_ads']:>15.8f}\n")

# Display results
print(df_ads)

