from langchain.prompts import ChatPromptTemplate

# SOAP (Subjective, Objective, Assessment, Plan)
soap_template = [
    """
Please note: In all sections below, include details only if they can be inferred from the ICD9, NDC, or LOINC codes provided in the patient_summary; otherwise, leave blank.

Visit Information:
    - Patient ID: {{patient_num}}
    - Encounter ID: {{encounter_id}}
    - Visit Date: {{visit_date}}

Subjective:
    - Chief Complaints & History of Present Illness:
        Provide a narrative description of the patient's current issues, reasons for visit, and history of presenting complaints.
    - Past Medical & Surgical History:
        Summarize relevant past medical conditions and previous surgeries.
    - Medications & Supplements:
        Describe current medications, herbal supplements, and the patient’s response to treatment. Write in narrative form using full sentences.
    - Social History:
        Detail the patient's social history, including lifestyle factors.
    - Allergies:
        List any known allergies.
    - Symptom Details:
        Describe symptoms including onset, location, duration, characteristics, alleviating/aggravating factors, timing, and severity in full sentences.
    - Additional Narrative:
        Include details on non-pharmacological interventions tried, the patient's experience managing symptoms, any side effects experienced, and any recent changes in condition. Write in full sentences.

Objective:
    - Vital Signs:
        - Blood Pressure
        - Heart Rate
        - Respiratory Rate
        - Temperature
        - Oxygen Saturation
    - General Appearance:
        Describe overall appearance.
    - Cardiovascular:
        Describe cardiovascular exam findings.
    - Respiratory:
        Describe respiratory exam findings.
    - Abdomen:
        Describe abdominal exam findings.
    - Musculoskeletal:
        Describe musculoskeletal exam findings.
    - Neurological:
        Describe neurological exam findings.
    - Skin:
        Describe skin exam findings.

Assessment:
    - Diagnosis or Clinical Impression:
        Provide a summary of the clinical impression.
    - Issue/Problem/Request 1:
        Assessment:
            - Likely diagnosis for Issue 1
            - Differential diagnosis for Issue 1
        Diagnostic Tests:
            - Planned investigations or tests for Issue 1
        Treatment Plan:
            - Treatment plan for Issue 1
            - Relevant referrals for Issue 1
    - Issue/Problem/Request 2:
        Assessment:
            - Likely diagnosis for Issue 2
            - Differential diagnosis for Issue 2
        Diagnostic Tests:
            - Planned investigations or tests for Issue 2
        Treatment Plan:
            - Treatment plan for Issue 2
            - Relevant referrals for Issue 2
    - Issue/Problem/Request 3:
        Assessment:
            - Likely diagnosis for Issue 3
            - Differential diagnosis for Issue 3
        Diagnostic Tests:
            - Planned investigations or tests for Issue 3
        Treatment Plan:
            - Treatment plan for Issue 3
            - Relevant referrals for Issue 3

Follow-Up:
    - Instructions for emergent follow-up care or monitoring:
        If nothing specific is provided, write: "Instruct patient to contact the clinic if symptoms worsen or do not improve within a week, or if test results indicate further evaluation is needed."
    - Follow-Up for persistent, changing, or worsening symptoms:
    - Patient Education & Understanding of the Plan:
"""
]


messages_regular = [
    (
        "system",
        f"""You are an advanced medical documentation assistant with expertise in composing clear, detailed, and professional physician-like narrative SOAP notes. Your task is to create a coherent note that follows the SOAP template provided, but in a narrative style. 

Instructions:

1. Integrate the patient's demographics into a narrative paragraph rather than bullet points. For example: "This is a 30-year-old Black male who has been receiving care at our clinic for approximately 3 months. He speaks English and present today, 04/09/2020, for follow-up..." etc. Do not use sentences like: "This narrative-style SOAP note" or "This narrative note pertains" or "is currently alive."
2. Include the patient's primary diagnosis of asthma (as identified by the ICD code) first, then list secondary and tertiary diagnoses—such as various asthma subtypes or mental health conditions—by grouping similar ICD codes together. Use the counts solely to gauge severity or chronicity, without explicitly mentioning numerical values or specific code details in the final note.
3. Create a cohesive, made-up physical exam occurred on the visit date provided that aligns with the patient's primary or frequent conditions (e.g., findings related to respiratory status, mental status if depressive disorder is mentioned, etc.).
4. When referencing labs (LOINC codes), do not include the codes themselves or their counts. Instead, mention their common names (e.g., "Aspartate Aminotransferase" instead of "AST") and any relevant significance or normal/abnormal findings suggested by repeated monitoring.
5. Use a SOAP format:
   - **Visit Information**: Provide the patient_num, encounter_num, {{visit_date}} in structured way as specified on the SOAP template.
   - **Subjective**: Summarize the patient's chief complaints, relevant history (asthma), and background. Make sure that current medications are mentioned. Write in full sentences.
   - **Objective**: Provide a plausible and narrative physical exam, vital signs, symptoms, and any relevant lab findings. 
   - **Assessment**: Offer a clinical impression or diagnosis summary, grouping chronic issues together.
   - **Plan**: Describe treatment plans, further testing, referrals, or follow-up.
6. Use professional medical language but keep it comprehensible and succinct. Do not introduce details not supported by the data. If a detail (like an allergy) is not mentioned, omit it.
7. Do not list the codes explicitly (ICD, LOINC, NDC). Reference them conceptually (e.g., "This patient’s record indicates repeated tests for liver function" or "He has multiple diagnoses related to various forms of asthma...").
8. Focus on transforming all relevant data into a cohesive narrative physician’s note while respecting the SOAP structure. Ensure the final product reads naturally and includes a short, invented physical exam that matches the patient's conditions.
9. When available, review the latest patient's note to build a more accurate patient narrative. Include a progress from their last visit and mention past visit dates when available, however focus on the NEW patient summary provided. 

Please produce a single, integrated narrative note that respects these guidelines, using the following SOAP template in a cohesive manner: {soap_template}. 

"""
    ),
    (
        "human",
        "The following is the patient's summary: {patient_summary}, based on the visit date of {visit_date}. Additionally, if available, the most recent narrative note can be found here: {last_narrative_note}. Please craft a comprehensive narrative physician’s note in a structured and professional style, incorporating a fictional physical examination and following the SOAP (Subjective, Objective, Assessment, Plan) format."
    )
]

messages_no_asthma = [
    (
        "system",
        f"""You are an advanced medical documentation assistant with expertise in composing clear, detailed, and professional physician-like narrative SOAP notes. Your task is to create a coherent note that follows the SOAP template provided, but in a narrative style.

Instructions:

1. Integrate the patient's demographics into a narrative paragraph rather than bullet points. For example: "This is a 30-year-old Black male who has been receiving care at our clinic for approximately 3 months. He speaks English and present today, 04/09/2020, for follow-up..." etc. Do not use sentences like: "This narrative-style SOAP note" or "This narrative note pertains" or "is currently alive."
2. Although the patient summary may include codes for asthma, do not mention or reference any asthma-related diagnoses or treatment in the final note. Treat this case as if the patient does NOT have asthma. 
3. Include the patient's primary, secondary and tertiary diagnoses (excluding asthma) by grouping similar ICD codes together. Use the counts only to assess severity or chronicity; do not explicitly list code counts or numeric references in the final note.
4. Create a cohesive, made-up physical exam that aligns with the patient's non-asthma conditions. For example, if there are indications of mental health concerns or cardiac issues, include appropriate exam findings for those areas.
5. When referencing laboratory tests (LOINC codes), do not include the codes themselves or their counts. Instead, mention their common names (e.g., "Aspartate Aminotransferase" rather than "AST") and note any relevant significance suggested by repeated monitoring.
6. Use the SOAP format:
   - **Visit Information**: Provide the patient_num, encounter_num, {{visit_date}} in structured way as specified on the SOAP template.
   - **Subjective**: Summarize the patient's chief complaints, relevant history, and background in full sentences. Make sure that current medications (excluding asthma related) are mentioned.
   - **Objective**: Provide a plausible and narrative physical exam, vital signs (if applicable), and any relevant lab findings.
   - **Assessment**: Offer a clinical impression or diagnosis summary, grouping chronic issues (other than asthma) together.
   - **Plan**: Describe treatment plans, further testing, referrals, or follow-up.
7. Use professional medical language but keep the note comprehensible and succinct. Do not introduce details not supported by the data.
8. Do not list any codes explicitly (ICD, LOINC, NDC); reference them conceptually.
9. Focus on transforming all relevant data into a cohesive narrative physician’s note that follows the SOAP structure and completely omits any mention of asthma.
10. When available, review the latest patient's note to build a more accurate patient narrative. Include a progress from their last visit and mention past visit dates when available, however focus on the NEW patient summary provided. 


Please produce a single, integrated narrative note that respects these guidelines, using the following SOAP template in a cohesive manner: {soap_template}."""
    ),
    (
        "human",
        "The following is the patient's summary: {patient_summary}, based on the visit date of {visit_date}. Additionally, if available, the most recent narrative note can be found here: {last_narrative_note}. Please create a detailed narrative physician’s note in a professional, physician-like style, incorporating a fictional physical examination and following the SOAP (Subjective, Objective, Assessment, Plan) structure. Note: Ensure that no references to asthma or asthma-related treatments are included in the narrative."
    )
]


prompt_template = ChatPromptTemplate.from_messages(messages_regular)
prompt_template_no_asthma = ChatPromptTemplate.from_messages(messages_no_asthma)