import pandas as pd
from collections import Counter

df = pd.read_csv("preprocessed_data.csv")

def recommend_symptoms(gender, age, user_symptoms, top_n=5):
    user_symptoms_set = set(user_symptoms)
    matched_symptoms = []

    for _, row in df.iterrows():
        if not isinstance(row["symptom_list"], str):
            continue
        try:
            patient_symptoms = eval(row["symptom_list"])
        except:
            continue

        if user_symptoms_set & set(patient_symptoms):
            matched_symptoms.extend(patient_symptoms)

    new_symptoms = list(set(matched_symptoms) - user_symptoms_set)
    sorted_symptoms = [s for s, _ in Counter(new_symptoms).most_common(top_n)]
    return sorted_symptoms
