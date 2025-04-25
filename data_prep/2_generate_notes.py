import os
from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
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

# Define input and output directories
input_dir = "patient_summaries_old"
output_dir = "patient_notes_old"
os.makedirs(output_dir, exist_ok=True)

# List of patient numbers for which to use the "no asthma" prompt
no_asthma_patient_nums = {
    "1000000071", "1000000003", "1000000047", "1000000068", "1000000048",
    "1000000093", "1000000103", "1000000009", "1000000002", "1000000087",
    "1000000101", "1000000107", "1000000040", "1000000036", "1000000052",
    "1000000086", "1000000023", "1000000010", "1000000063", "1000000082",
    "1000000064", "1000000013"
}

# Flag: If set to True, process only files for patients in the no-asthma list.
process_only_no_asthma = False  # Set to True to process only the specified patient numbers

# Gather only .txt files and sort them
txt_files = sorted([f for f in os.listdir(input_dir) if f.endswith(".txt")])
total = len(txt_files)
count = 0

# Loop over each patient summary file in the input directory
for filename in txt_files:
    # Extract patient number from filename assuming format "patient_{patient_num}.txt"
    patient_num = filename.replace("patient_", "").replace(".txt", "")

    # If the flag is set, skip files not in the no_asthma list
    if process_only_no_asthma and patient_num not in no_asthma_patient_nums:
        continue

    count += 1
    print(f"Working on summary {count} of {total} - {filename}")

    file_path = os.path.join(input_dir, filename)
    with open(file_path, "r") as file:
        patient_summary = file.read()

    # Select the appropriate prompt based on the patient number
    if patient_num in no_asthma_patient_nums:
        current_prompt = prompt_template_no_asthma.invoke({
            "patient_summary": patient_summary,
            "soap_template": soap_template  # if your prompt references this variable
        })
    else:
        current_prompt = prompt_template.invoke({
            "patient_summary": patient_summary,
            "soap_template": soap_template
        })

    # Use the model to generate the narrative note
    result = model.invoke(current_prompt)
    narrative_note = result.content  # Assuming result has an attribute 'content'

    # Replace 'patient_' with 'note_' in the output filename
    output_filename = filename.replace("patient_", "note_")
    output_file_path = os.path.join(output_dir, output_filename)

    with open(output_file_path, "w") as output_file:
        output_file.write(narrative_note)

    print(f"Generated narrative note for {filename} and saved to {output_file_path}\n")
