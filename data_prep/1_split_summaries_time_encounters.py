import re
import os
from datetime import datetime

# Input CSV file name
input_file = "Summary133forLLM_encounters_v1.csv"

# Read the entire file content
with open(input_file, "r") as f:
    content = f.read()

# Remove any double quotes from the content
content = content.replace('"', '')

# Split the content on any sequence of 5 or more asterisks
blocks = re.split(r'\*{30,} BEGINNING OF ENCOUNTER', content)

# Dictionary to accumulate datafiles per patient
patients = {}

for block in blocks:
    block = block.strip()
    if not block:
        continue  # Skip empty blocks

    # Extract the patient number from the block
    match = re.search(r'patient_num:\s*(\d+)', block)
    if match:
        patient_id = match.group(1)
        match_time = re.search(r'encounter_start_date:\s*([A-Za-z]{3}\s+\d{1,2}\s+\d{4})', block)
        match_encounter = re.search(r'encounter_num:\s*(\d+)', block)
        if match_time:
            encounter_start_date = datetime.strptime((match_time.group(1)), '%b %d %Y')
            encounter_start_date_str = encounter_start_date.strftime('%Y%m%d')
            encounter_num = match_encounter.group(1)

            note_id = f"PID:{patient_id}-EID:{encounter_num}-CCD:PNote-SDT:{encounter_start_date_str}-PRD"

            if note_id in patients:
                patients[note_id] += "\n" + block
            else:
                patients[note_id] = block
    else:
        print("No patient number found in a block; skipping.")

# Create output subfolder if it does not exist
output_dir = "patient_summaries"
os.makedirs(output_dir, exist_ok=True)

# Write each patient's datafiles to a separate file in the subfolder
for note_id, patient_data in patients.items():
    output_filename = os.path.join(output_dir, f"{note_id}.txt")
    with open(output_filename, "w") as out_file:
        out_file.write(patient_data)
    print(f"Wrote data for patient {note_id} to {output_filename}")
