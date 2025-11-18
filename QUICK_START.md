# Quick Start Guide - Fixing "image media type is required" Error

## The Problem
You received this error:
```
Request Failed: 400 {"error":{"message":"image media type is required","code":"invalid_request_body"}}
```

## The Solution
The error occurs when API requests with images don't include the `type` field in the request structure.

## Quick Fix - 3 Steps

### Step 1: Install Requirements (if needed)
```bash
# No external packages required for the example script!
# It uses only Python standard library
```

### Step 2: Test Your Setup
```bash
# See the correct format for image URLs
python fix_image_api_example.py --image-url "https://example.com/your-image.jpg"

# Or test with a local image file
python fix_image_api_example.py --image path/to/your/image.jpg
```

### Step 3: Apply the Fix
The key is to include `"type"` fields in your API request:

```python
# ❌ WRONG - Missing "type" fields
messages = [{
    "role": "user",
    "content": [
        "What's in this image?",  # Missing type!
        {"image_url": "..."}      # Missing type!
    ]
}]

# ✅ CORRECT - With "type" fields
messages = [{
    "role": "user",
    "content": [
        {
            "type": "text",        # ← Added type
            "text": "What's in this image?"
        },
        {
            "type": "image_url",   # ← Added type
            "image_url": {
                "url": "data:image/jpeg;base64,..."
            }
        }
    ]
}]
```

## Resources in This Repository

1. **TROUBLESHOOTING.md** - Complete guide with detailed examples
2. **fix_image_api_example.py** - Interactive script to test your setup
3. **This file** - Quick reference

## Common Use Cases

### Use Case 1: OpenAI Vision API
```python
import base64

# Read and encode image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode('utf-8')

# Correct format
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "Describe this image"},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{image_data}"
                }
            }
        ]
    }]
}
```

### Use Case 2: Using Image URLs
```python
payload = {
    "model": "gpt-4-vision-preview",
    "messages": [{
        "role": "user",
        "content": [
            {"type": "text", "text": "What's in this image?"},
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://example.com/image.jpg"
                }
            }
        ]
    }]
}
```

## Checklist
- [ ] Include `"type": "text"` for text content
- [ ] Include `"type": "image_url"` for images
- [ ] Specify media type in data URI: `data:image/jpeg;base64,...`
- [ ] Verify image file is valid and not corrupted
- [ ] Test with the example script first

## Still Having Issues?
1. Run the example script: `python fix_image_api_example.py --show-incorrect`
2. Read the full guide: `TROUBLESHOOTING.md`
3. Verify your image file: `file your-image.jpg`
4. Check API documentation for specific requirements

## API-Specific Notes

### OpenAI API
- Supported formats: PNG, JPEG, WebP, GIF
- Maximum file size: 20MB
- Use `gpt-4-vision-preview` or newer models

### GitHub Copilot
- Ensure images are properly formatted
- Use correct media types
- Follow the content structure above

---

**Remember:** The key fix is adding `"type"` fields to all content items in your API requests!
