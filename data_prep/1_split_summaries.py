import re
import os

# Input CSV file name
input_file = "Summary133forLLM2.csv"

# Read the entire file content
with open(input_file, "r") as f:
    content = f.read()

# Remove any double quotes from the content
content = content.replace('"', '')

# Split the content on any sequence of 5 or more asterisks
blocks = re.split(r'\*{5,}', content)

# Dictionary to accumulate data per patient
patients = {}

for block in blocks:
    block = block.strip()
    if not block:
        continue  # Skip empty blocks

    # Extract the patient number from the block
    match = re.search(r'patient_num:\s*(\d+)', block)
    if match:
        patient_id = match.group(1)
        # If this patient already has data, append the current block; otherwise, start new.
        if patient_id in patients:
            patients[patient_id] += "\n" + block
        else:
            patients[patient_id] = block
    else:
        print("No patient number found in a block; skipping.")

# Create output subfolder if it does not exist
output_dir = "patient_summaries_old"
os.makedirs(output_dir, exist_ok=True)

# Write each patient's data to a separate file in the subfolder
for patient_id, patient_data in patients.items():
    output_filename = os.path.join(output_dir, f"patient_{patient_id}.txt")
    with open(output_filename, "w") as out_file:
        out_file.write(patient_data)
    print(f"Wrote data for patient {patient_id} to {output_filename}")
