import gspread
from oauth2client.service_account import ServiceAccountCredentials
import openai
from dotenv import load_dotenv
import os

load_dotenv()

# Replace with your actual API key
api_key = os.getenv("OPENAI_API_KEY")

# Define the scope
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# Path to your service account key file
file_name = 'client_key.json'

# Create a ServiceAccountCredentials object from the JSON key file
creds = ServiceAccountCredentials.from_json_keyfile_name(file_name, scope)

# Authorize the gspread client with the credentials
client = gspread.authorize(creds)

# Open the Google Sheet
sheet = client.open('TaniaData')
sheet1 = sheet.get_worksheet(0)  # Get the first sheet
sheet2 = sheet.get_worksheet(1)  # Get the second sheet


def append_to_sheet1(values):
    try:
        sheet1.append_row(values)
        print("Data appended to Sheet1 successfully.")
    except gspread.exceptions.SpreadsheetNotFound as e:
        print(f"Spreadsheet not found: {e}")
        print("Ensure the spreadsheet name is correct and the service account has access.")
    except gspread.exceptions.APIError as e:
        print(f"An API error occurred: {e}")
        print("Ensure the Google Drive API is enabled and the service account has access to the sheet.")

def is_content_appropriate(content):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a content moderation assistant. Please determine if the following information is appropriate and relevant for general public use, filtering out any inappropriate, offensive, or nonsensical content."},
                {"role": "user", "content": content}
            ]
        )
        result = response.choices[0].message['content'].strip().lower()
        return "appropriate" in result
    except Exception as e:
        print(f"Se produjo un error al verificar la idoneidad del contenido: {e}")
        return False

def read_database():
    try:
        records = sheet2.get_all_records()
        filtered_records = [record for record in records if is_content_appropriate(record['INFORMACIÓN'])]
        return filtered_records
    except Exception as e:
        print(f"An error occurred: {e}")
        return []
