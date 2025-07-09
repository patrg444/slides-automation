# Google Slides API Testing Project

This project demonstrates how to use the Google Slides API with Python to create, modify, and read presentations programmatically.

## Features

### Basic Operations (`test_google_slides.py`)
- Create new presentations
- Add slides with different layouts
- Insert and update text boxes
- List slides and their content
- Authentication handling

### Advanced Operations (`advanced_examples.py`)
- Formatted text with custom styles
- Tables with data
- Bullet lists
- Shapes with colors
- Slide background customization
- Slide duplication

## Project Structure

```
google-slides-api-test/
├── venv/                    # Virtual environment
├── credentials.json         # OAuth2 credentials (you need to add this)
├── token.json              # Stored authentication token (auto-generated)
├── requirements.txt        # Python dependencies
├── .env.example           # Example environment variables
├── .gitignore            # Git ignore file
├── SETUP.md              # Detailed setup instructions
├── README.md             # This file
├── test_google_slides.py # Basic API operations
└── advanced_examples.py  # Advanced API examples
```

## Quick Start

1. **Clone/Navigate to the project**
   ```bash
   cd /Users/patrickgloria/google-slides-api-test
   ```

2. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

3. **Set up Google Cloud credentials**
   - Follow instructions in `SETUP.md`
   - Download `credentials.json` from Google Cloud Console
   - Place it in the project root

4. **Run the basic test**
   ```bash
   python test_google_slides.py
   ```

5. **Run advanced examples**
   ```bash
   python advanced_examples.py
   ```

## API Operations Overview

### Creating Presentations
```python
api = GoogleSlidesAPI()
presentation_id = api.create_presentation("My Presentation")
```

### Adding Slides
```python
slide_id = api.add_slide(presentation_id, 'BLANK')
```

### Adding Text
```python
api.add_text_box(presentation_id, slide_id, "Hello World!", x=100, y=100)
```

### Formatting Text
```python
api.add_formatted_text(
    presentation_id, slide_id, 
    "Bold Blue Text", 
    font_size=18, bold=True,
    color={'red': 0, 'green': 0, 'blue': 1}
)
```

### Creating Tables
```python
table_id = api.create_table(presentation_id, slide_id, rows=3, columns=3)
api.fill_table_cell(presentation_id, table_id, 0, 0, "Cell Content")
```

## Available Slide Layouts

- `BLANK` - Empty slide
- `TITLE` - Title slide
- `TITLE_AND_BODY` - Title with body content
- `TITLE_AND_TWO_COLUMNS` - Title with two columns
- `TITLE_ONLY` - Only title
- `SECTION_HEADER` - Section divider
- `SECTION_TITLE_AND_DESCRIPTION` - Section with description
- `ONE_COLUMN_TEXT` - Single column text
- `MAIN_POINT` - Main point slide
- `BIG_NUMBER` - Large number display
- `CAPTION_ONLY` - Caption only layout

## Color Format

Colors use RGB values between 0 and 1:
```python
color = {
    'red': 0.5,    # 50% red
    'green': 0.8,  # 80% green
    'blue': 0.2    # 20% blue
}
```

## Error Handling

The scripts include error handling for common issues:
- Missing credentials
- API errors
- Invalid parameters

## Troubleshooting

1. **Authentication Issues**
   - Delete `token.json` and re-authenticate
   - Ensure OAuth consent screen is configured
   - Check that Google Slides API is enabled

2. **Permission Errors**
   - Verify the account has access to Google Slides
   - Check OAuth scopes in the code

3. **API Quota Limits**
   - Google Slides API has usage quotas
   - Check Google Cloud Console for current usage

## Next Steps

- Explore more shape types and formatting options
- Add image insertion capabilities
- Implement slide transitions
- Create presentation templates
- Add batch operations for better performance

## Resources

- [Google Slides API Documentation](https://developers.google.com/slides)
- [Python Client Library](https://github.com/googleapis/google-api-python-client)
- [API Reference](https://developers.google.com/slides/api/reference/rest)

## License

This is a test project for educational purposes.