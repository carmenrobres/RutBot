import gspread
from oauth2client.service_account import ServiceAccountCredentials
import cv2
import numpy as np
import textwrap
import time

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

# Function to open the sheet
def open_sheet():
    try:
        sheet = client.open('TaniaData').sheet1
        return sheet
    except gspread.exceptions.SpreadsheetNotFound:
        print("Spreadsheet 'TaniaData' not found. Please ensure the following:")
        print("1. The spreadsheet name is exactly 'TaniaData'.")
        print("2. The service account has access to the spreadsheet.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit(1)

# Open the Google Sheet
sheet = open_sheet()

# Colors for different columns
colors = [
    (0, 0, 255),  # Red
    (0, 255, 0),  # Green
    (255, 255, 0), # Yellow
    (255, 0, 0),  # Blue
    (255, 0, 255),  # Magenta
    (0, 255, 255)  # Cyan
]

def display_data():
    while True:
        try:
            # Fetch all records
            records = sheet.get_all_records()

            # Create a blank image with black background
            height = 800
            width = 1000
            blank_image = np.zeros((height, width, 3), np.uint8)
            blank_image.fill(0)  # Fill the image with black color

            # Font settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            thickness = 1
            line_height = 20

            y_position = 30  # Starting position

            # Display the MESSAGE and ANSWER columns
            for idx, record in enumerate(records):
                message = record.get('MESSAGE', 'No data')  # Use uppercase 'MESSAGE'
                answer = record.get('ANSWER', '')  # Use uppercase 'ANSWER'

                # Wrap text if it's too long
                wrapped_message = textwrap.wrap(message, width=50)
                wrapped_answer = textwrap.wrap(answer, width=50)

                # Get color for message
                color = colors[idx % len(colors)]
                
                # Display wrapped message
                for i, line in enumerate(wrapped_message):
                    cv2.putText(blank_image, line, (10, y_position + i * line_height), font, font_scale, color, thickness, cv2.LINE_AA)

                # Update y_position for the answer
                y_position += len(wrapped_message) * line_height

                # Display wrapped answer in white
                for i, line in enumerate(wrapped_answer):
                    cv2.putText(blank_image, line, (10, y_position + i * line_height), font, font_scale, (255, 255, 255), thickness, cv2.LINE_AA)

                # Update y_position for the next record
                y_position += len(wrapped_answer) * line_height + 30  # Add some space after each message and answer

            # Show the image
            cv2.imshow('Google Sheet Data', blank_image)

            if cv2.waitKey(5000) & 0xFF == 27:  # Update every 5 seconds, exit on 'Esc' key
                break

        except Exception as e:
            print(f"An error occurred: {e}")
            time.sleep(5)

    cv2.destroyAllWindows()

display_data()
