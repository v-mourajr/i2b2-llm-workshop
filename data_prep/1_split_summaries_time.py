import re
import os
from datetime import datetime


# Input CSV file name
input_file = "Summary133forLLM_time_v1.csv"

# Read the entire file content
with open(input_file, "r") as f:
    content = f.read()

# Remove any double quotes from the content
content = content.replace('"', '')

# Split the content on any sequence of 5 or more asterisks
blocks = re.split(r'\*{10,}', content)

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
        match_time = re.search(r'latest fact:\s*([A-Za-z]{3}\s+\d{1,2}\s+\d{4})', block)
        if match_time:
            latest_fact = datetime.strptime((match_time.group(1)), '%b %d %Y')
            latest_fact_str = latest_fact.strftime('%Y%m%d')

            note_id = patient_id + '_' + latest_fact_str

            if note_id in patients:
                patients[note_id] += "\n" + block
            else:
                patients[note_id] = block
    else:
        print("No patient number found in a block; skipping.")

# Create output subfolder if it does not exist
output_dir = "patient_summaries"
os.makedirs(output_dir, exist_ok=True)

# Write each patient's data to a separate file in the subfolder
for note_id, patient_data in patients.items():
    output_filename = os.path.join(output_dir, f"patient_{note_id}.txt")
    with open(output_filename, "w") as out_file:
        out_file.write(patient_data)
    print(f"Wrote data for patient {note_id} to {output_filename}")
