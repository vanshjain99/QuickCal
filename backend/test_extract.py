import os
import sys
import json
import requests

def test_extraction_endpoint(file_path: str):
    """
    Sends a timetable file to the FastAPI extraction endpoint and pretty-prints the output.
    """
    url = "http://127.0.0.1:8000/api/v1/extract"
    
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        print("Please place a sample timetable image, PDF, or Excel file in the directory.")
        return

    print(f"Opening file: {file_path}")
    
    # Determine basic mime type guess (defaulting to image/png if unsure)
    _, ext = os.path.splitext(file_path.lower())
    if ext in ['.png']:
        mime_type = 'image/png'
    elif ext in ['.jpg', '.jpeg']:
        mime_type = 'image/jpeg'
    elif ext in ['.pdf']:
        mime_type = 'application/pdf'
    elif ext in ['.xls']:
        mime_type = 'application/vnd.ms-excel'
    elif ext in ['.xlsx']:
        mime_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    else:
        mime_type = 'image/png' # Default fallback
        
    try:
        with open(file_path, 'rb') as f:
            files = {'file': (os.path.basename(file_path), f, mime_type)}
            print(f"Sending POST request to {url} with Content-Type: {mime_type}...")
            
            response = requests.post(url, files=files)
            
            print(f"\nResponse HTTP Status Code: {response.status_code}")
            
            if response.status_code == 200:
                print("Extraction successful! Parsed JSON response:\n")
                parsed_data = response.json()
                print(json.dumps(parsed_data, indent=2))
            else:
                print("Extraction failed. Error details:")
                try:
                    print(json.dumps(response.json(), indent=2))
                except json.JSONDecodeError:
                    print(response.text)
                    
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the backend server.")
        print("Make sure the FastAPI server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\nAn unexpected error occurred: {str(e)}")

if __name__ == "__main__":
    # You can change this variable to point to any sample timetable image, pdf, or excel sheet
    test_image_path = "sample_timetable.png"
    
    # Allow overriding file path via command line arguments
    if len(sys.argv) > 1:
        test_image_path = sys.argv[1]
        
    test_extraction_endpoint(test_image_path)
