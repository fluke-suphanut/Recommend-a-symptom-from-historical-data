# Recommend a symptom from historical data

![Banner: a stethoscope under a network of connected dots that leads to a red starburst](docs/banner.png)

This project suggests more symptoms to a user, based on the symptoms that past patients reported together.

Portfolio: https://suphanut.pages.dev

## What it does

The user gives their gender, age, and current symptoms. The system suggests other symptoms that patients with matching symptoms reported.

### Data preparation (notebook)

`symptom-recommender.ipynb` prepares the data:

- Loads `patient_symptoms.csv`: 1,000 patient records with gender, age, a symptom summary, and search terms.
- Encodes gender: male is `0`, female is `1`.
- Splits the comma-separated `search_term` column into a list of unique symptoms.
- Counts the 10 most common symptoms.
- Saves gender, age, and the symptom list to `preprocessed_data.csv`.

### Basic recommender (API and notebook)

- Finds past patients who share at least one symptom with the user.
- Collects all symptoms from those patients.
- Removes the symptoms the user already gave.
- Returns up to 5 of the remaining symptoms.

### Advanced recommender (notebook only)

- Turns each symptom list into a binary vector with `MultiLabelBinarizer`, and adds gender and age.
- Groups the patients into 5 clusters with `KMeans`.
- Puts the user into a cluster and suggests symptoms from patients in the same cluster.

The API does not include this recommender.

### API

`api_main.py` is a FastAPI app with one endpoint:

| Method | Path | Body | Response |
| --- | --- | --- | --- |
| POST | `/recommend` | `gender` (text), `age` (number), `symptoms` (list of text) | `{"recommendations": [...]}` with up to 5 symptoms |

The API maps `"male"` to `0` and any other gender value to `1`. Symptom names must match the names in the dataset exactly. Most names are in Thai.

## Why

The goal is a symptom recommender built from historical patient data. When a user enters personal details and their symptoms, the system shows symptoms that similar past patients also reported.

## Tech stack

- Python 3.9 or later
- FastAPI (REST API) and Uvicorn (API server)
- pandas (data handling)
- scikit-learn (`MultiLabelBinarizer` and `KMeans`, in the notebook)
- Jupyter Notebook

## How to run

1. Install the packages:

   ```bash
   pip install -r requirements.txt
   ```

2. Start the API server from the repository root. `recommender.py` loads `preprocessed_data.csv` from the current folder:

   ```bash
   uvicorn api_main:app --reload
   ```

3. Open http://127.0.0.1:8000/docs in your browser. Swagger UI lets you send test requests: select **Try it out**, enter the JSON body, and select **Execute**.

To run the data preparation and the advanced recommender, open the notebook:

```bash
jupyter notebook symptom-recommender.ipynb
```

The project uses no environment variables.

## Example

`POST /recommend` request:

```json
{
  "gender": "female",
  "age": 30,
  "symptoms": ["ไอ", "มีเสมหะ"]
}
```

Response. The symptoms come from the dataset, but this list is made up. The real list and its order can change. See [Limits](#limits).

```json
{
  "recommendations": ["เจ็บคอ", "น้ำมูกไหล", "ไข้", "คัดจมูก", "เสมหะไหลลงคอ"]
}
```

Translations of the symptom names:

| Symptom | English |
| --- | --- |
| `ไอ` | cough |
| `มีเสมหะ` | has phlegm |
| `เจ็บคอ` | sore throat |
| `น้ำมูกไหล` | runny nose |
| `ไข้` | fever |
| `คัดจมูก` | stuffy nose |
| `เสมหะไหลลงคอ` | phlegm running down the throat |

## Project structure

```text
api_main.py                  FastAPI app with POST /recommend
recommender.py               Basic recommender used by the API
symptom-recommender.ipynb    Data preparation, basic and advanced recommenders
patient_symptoms.csv         Raw patient data (1,000 rows)
preprocessed_data.csv        Gender, age, and symptom list (1,000 rows)
requirements.txt             Python packages
output.pdf                   Screenshots of the API running in Swagger UI
```

## Limits

- The API ignores gender and age. `recommend_symptoms()` accepts them but matches on symptoms only.
- The results are not sorted by how often symptoms occur together. The code removes duplicates before it counts, so every symptom has a count of 1. The 5 symptoms returned are an arbitrary subset, and they can change after a server restart.
- The advanced recommender in the notebook has the same counting problem. It also uses raw age next to 0 and 1 symptom values, so age has a large effect on the clusters.
- A user who shares one common symptom, such as a cough, matches many patients. The suggestions can then include unrelated symptoms.
- Symptom names must match exactly. Some dataset entries join two symptoms without a separator.
- `recommender.py` and the notebook call `eval()` on CSV content. Use only CSV files you trust.
- The API does not validate input. An empty symptom list returns an empty list.
- This project is not a medical tool. Do not use it to make health decisions.

## Licence

This repository has no licence file, so default copyright applies.

`patient_symptoms.csv` and `preprocessed_data.csv` contain patient symptom records. The repository does not say where this data comes from or under what terms you can use it.
