import os
import binascii
import csv

# Define input and output directories
input_dir = "patient_notes_txt"
output_dir_hex = "patient_notes_hex"
os.makedirs(output_dir_hex, exist_ok=True)

# Define asthma classification
no_asthma_patient_nums = {
    "1000000002", "1000000003", "1000000009", "1000000010", "1000000013",
    "1000000023", "1000000036", "1000000040", "1000000047", "1000000048",
    "1000000052", "1000000063", "1000000064", "1000000068", "1000000071",
    "1000000082", "1000000086", "1000000087", "1000000093", "1000000101",
    "1000000103", "1000000107"
}

# Prepare to store consolidated datafiles
consolidated_data = []

# Gather only .txt files and sort them
txt_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])
total = len(txt_files)
count = 0

for filename in txt_files:
    count += 1
    print(f"Working on summary {count} of {total} - {filename}")

    # Parse metadata from filename
    parts = filename.split("-")
    patient_num = parts[0].split(":")[1]
    encounter_num = parts[1].split(':')[1]
    encounter_start_date = parts[3].split(":")[1]
    start_date = f"{encounter_start_date[4:6]}/{encounter_start_date[6:]}/{encounter_start_date[0:4]}"
    has_asthma = patient_num not in no_asthma_patient_nums

    file_path = os.path.join(input_dir, filename)
    with open(file_path, "r") as file:
        narrative_note = file.read()

    # Convert narrative note to binary and then to BinHex format (same as i2b2 Blob)
    binary_text = narrative_note.encode("utf-8")
    hex_text = binascii.hexlify(binary_text).decode("utf-8").upper()

    # Save to hex output
    output_file_hex_path = os.path.join(output_dir_hex, filename)
    with open(output_file_hex_path, "w", encoding="utf-8") as hex_file:
        hex_file.write(hex_text)

    inout_cd = 'O' # assumed 'O' for outpatient.
    if has_asthma:
        location_cd = 'ASTHMA_CLINIC'
        location_path = r'\Hospital\Clinic\Pulmonary\Asthma\\'
    else:
        location_cd = 'GEN_MED_OUTPATIENT'
        location_path = r'\Hospital\Outpatient\GeneralMedicine\\'


    # Append to consolidated list
    consolidated_data.append([
        encounter_num,
        patient_num,
        start_date,
        start_date, # as end_date
        inout_cd,
        location_cd,
        location_path,
        f"0x{hex_text}",
        filename
    ])

    print(f" --> Generated BinHex note for {filename}\n")

# Write consolidated CSV
csv_file_path = os.path.join("../datafiles", "i2b2_visit_dimension.csv")
with open(csv_file_path, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["encounter_num", "patient_num", "start_date", "end_date", "inout_cd", "location_cd", "location_path", "visit_blob", "file_name"])
    writer.writerows(consolidated_data)

print("\n\n------------>  COMPLETED <------------")
