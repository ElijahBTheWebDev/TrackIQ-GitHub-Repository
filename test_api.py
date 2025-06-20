import requests
import json
import sys
import os

def test_process_mp3(file_path):
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"Error: File not found: {file_path}")
        return

    # Check file extension
    _, ext = os.path.splitext(file_path)
    if ext.lower() not in ['.mp3', '.wav', '.ogg', '.flac', '.m4a']:
        print(f"Error: Unsupported file format: {ext}")
        print("Supported formats: .mp3, .wav, .ogg, .flac, .m4a")
        return

    # API endpoint
    url = "http://localhost:8000/process-mp3/"
    
    print(f"Processing file: {file_path}")
    print("Uploading to API...")
    
    try:
        # Open the file in binary mode
        with open(file_path, 'rb') as f:
            # Create the files parameter for the request
            files = {'file': (os.path.basename(file_path), f, 'audio/mpeg')}
            
            # Make the POST request
            response = requests.post(url, files=files)
            
            # Check if the request was successful
            if response.status_code == 200:
                print("\nSuccess! Here are the extracted features:")
                print(json.dumps(response.json(), indent=2))
            else:
                print(f"\nError {response.status_code}:")
                print(response.json().get('detail', 'Unknown error'))
    except requests.exceptions.ConnectionError:
        print("\nError: Could not connect to the server. Make sure it's running at http://localhost:8000")
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python test_api.py <path_to_audio_file>")
        sys.exit(1)
    
    mp3_file = sys.argv[1]
    test_process_mp3(mp3_file) 