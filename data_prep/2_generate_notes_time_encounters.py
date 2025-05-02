import os
import csv
import json
import struct
import binascii
from dotenv import load_dotenv
from datetime import datetime
from langchain_openai import AzureChatOpenAI, AzureOpenAIEmbeddings
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from prompt_data import soap_template, prompt_template, prompt_template_no_asthma

load_dotenv()

# Set up Azure credentials and token provider
azure_credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
    azure_credential, "https://cognitiveservices.azure.com/.default"
)

# Initialize the AzureChatOpenAI model using environment variables
model = AzureChatOpenAI(
    openai_api_version=os.getenv("AZURE_OPENAI_VERSION"),
    azure_deployment=os.getenv("AZURE_OPENAI_DEPLOYMENT"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    azure_ad_token_provider=token_provider
)

# Initialize the AzureOpenAIEmbeddings model using environment variables
embedding_model = AzureOpenAIEmbeddings(
    model=os.getenv("AZURE_EMBEDDING_MODEL"),
    azure_deployment=os.getenv("AZURE_EMBEDDING_DEPLOYMENT"),
    api_version=os.getenv("AZURE_EMBEDDING_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_EMBEDDING_ENDPOINT"),
    azure_ad_token_provider=token_provider,
    timeout=None,  # never timeout
    max_retries=2,  # try again twice
)

# Define input and output directories
input_dir = "patient_summaries"
output_dir_txt = "patient_notes_txt"
output_dir_hex = "patient_notes_hex"
os.makedirs(output_dir_txt, exist_ok=True)
os.makedirs(output_dir_hex, exist_ok=True)

# List of patient numbers for which to use the "no asthma" prompt
no_asthma_patient_nums = {
    "1000000002", "1000000003", "1000000009", "1000000010", "1000000013",
    "1000000023", "1000000036", "1000000040", "1000000047", "1000000048",
    "1000000052", "1000000063", "1000000064", "1000000068", "1000000071",
    "1000000082", "1000000086", "1000000087", "1000000093", "1000000101",
    "1000000103", "1000000107"
}

# Flag: If set to True, process only files for patients in the no-asthma list.
process_only_no_asthma = False  # Set to True to process only the specified patient numbers

# Gather only .txt files and sort them
txt_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])
total = len(txt_files)
count = 0

# Loop over each patient summary file in the input directory
last_narrative_note = {}
last_patient_num = {}
consolidated_rows = []

for filename in txt_files:
    parts = filename.split("-")
    patient_num = parts[0].split(':')[1]
    encounter_id = parts[1].split(':')[1]
    encounter_start_date = parts[3].split(':')[1]

    visit_date = datetime.strptime(encounter_start_date, '%Y%m%d').strftime('%m/%d/%Y')

    # If the flag is set, skip files not in the no_asthma list
    if process_only_no_asthma and patient_num not in no_asthma_patient_nums:
        continue

    if patient_num != last_patient_num:
        last_narrative_note = {}

    count += 1
    print(f"Working on summary {count} of {total} - {filename}")


    file_path = os.path.join(input_dir, filename)
    with open(file_path, "r") as file:
        patient_summary = file.read()

    # Select the appropriate prompt based on the patient number
    if patient_num in no_asthma_patient_nums:
        current_prompt = prompt_template_no_asthma.invoke({
            "patient_summary": patient_summary,
            "soap_template": soap_template,
            "last_narrative_note": last_narrative_note,
            "visit_date": visit_date
        })
    else:
        current_prompt = prompt_template.invoke({
            "patient_summary": patient_summary,
            "soap_template": soap_template,
            "last_narrative_note": last_narrative_note,
            "visit_date": visit_date
        })

    # Use the model to generate the narrative note
    result = model.invoke(current_prompt)
    narrative_note = result.content

    # Save last patient/note to include in the next narrative if needed
    last_narrative_note = narrative_note
    last_patient_num = patient_num

    # Save narrative note in a text file
    output_file_path = os.path.join(output_dir_txt, filename)

    with open(output_file_path, "w") as output_file:
        output_file.write(narrative_note)

    print(f"Generated narrative note for {filename} and saved to {output_file_path}\n")

    # Create BixHex version of the narrative
    note_embedded = embedding_model.embed_documents([narrative_note])[0]

    # 1. Convert embedding list of floats to binary
    binary_embedding = struct.pack(f'{len(note_embedded)}f', *note_embedded)

    # 2. Hexlify the binary
    hex_embedding = binascii.hexlify(binary_embedding).decode('utf-8').upper()

    # 3. Format the output line
    row = [
        patient_num,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "my_collection",
        f"doc_{patient_num}",
        f"embedding_{patient_num}",
        f"0x{hex_embedding}",
        "FLOAT32",
        json.dumps({
            "patient_num": patient_num,
            "encounter_id": encounter_id,
            "visit_date": visit_date,
            "chroma:document": narrative_note
        })
    ]
    # 4. Join to a CSV line
    output_line = ",".join(row)

    # 5. Save this to the `output_dir_hex`
    output_file_hex_path = os.path.join(output_dir_hex, filename)

    with open(output_file_hex_path, "w", encoding="utf-8") as hex_file:
        hex_file.write(output_line)

    consolidated_rows.append(row)

    print(f"Generated embeddings and BinHex note for {filename} and saved to {output_file_path}\n")

# Save all rows into one consolidated file
consolidated_file_path = os.path.join(output_dir_hex, "consolidated_table.csv")

with open(consolidated_file_path, "w", newline='', encoding="utf-8") as f:
    writer = csv.writer(f, quoting=csv.QUOTE_ALL)
    writer.writerow(["patient_num", "timestamp", "collection_name", "doc_id", "embedding_id", "embedding", "embedding_format", "metadata"])
    writer.writerows(consolidated_rows)

print(f"------------>  Consolidated CSV saved at {consolidated_file_path}")
