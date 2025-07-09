# Google Slides API Testing Setup

## Prerequisites

1. Python 3.8+ installed
2. Google Cloud account
3. Virtual environment activated

## Setup Instructions

### 1. Enable Google Slides API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Navigate to "APIs & Services" > "Enable APIs and Services"
4. Search for "Google Slides API" and enable it

### 2. Create Credentials

1. In the Google Cloud Console, go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - Choose "External" for testing
   - Fill in required fields
   - Add test users if needed
4. For Application type, choose "Desktop app"
5. Name your OAuth client (e.g., "Google Slides API Test")
6. Click "Create"
7. Download the credentials JSON file
8. Rename it to `credentials.json` and place it in the project directory

### 3. Run the Test

```bash
# Activate virtual environment
source venv/bin/activate

# Run the test script
python test_google_slides.py
```

## First Run

On first run, the script will:
1. Open your browser for authentication
2. Ask you to authorize the application
3. Save the authorization token locally for future use

## API Operations Tested

The test script demonstrates:
- Creating a new presentation
- Adding slides
- Inserting text boxes
- Updating text content
- Reading presentation data
- Batch updates

## Troubleshooting

- If you get authentication errors, delete `token.json` and re-authenticate
- Ensure the Google Slides API is enabled in your project
- Check that your OAuth consent screen is properly configured