# Troubleshooting Guide

## Error: "image media type is required"

### Error Details
```
Request Failed: 400 {"error":{"message":"image media type is required","code":"invalid_request_body"}}
```

### What This Error Means
This error occurs when making API requests that include images but the request body doesn't specify the image media type (MIME type). Many APIs, including OpenAI's Vision API, require explicit declaration of the image format.

### Common Causes
1. Missing `type` field in image data objects
2. Missing `media_type` or `mime_type` field for image content
3. Incorrectly formatted image data in API requests

### Solutions

#### Solution 1: Add Media Type to Image Data
When sending images in API requests, ensure you include the media type:

**For base64-encoded images:**
```python
# Incorrect
image_data = {
    "url": "data:image/jpeg;base64,/9j/4AAQ..."
}

# Correct
image_data = {
    "type": "image_url",
    "image_url": {
        "url": "data:image/jpeg;base64,/9j/4AAQ..."
    }
}
```

**For OpenAI API requests with images:**
```python
import base64
import requests

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

# Determine the correct media type
def get_media_type(image_path):
    if image_path.endswith('.png'):
        return 'image/png'
    elif image_path.endswith('.jpg') or image_path.endswith('.jpeg'):
        return 'image/jpeg'
    elif image_path.endswith('.gif'):
        return 'image/gif'
    elif image_path.endswith('.webp'):
        return 'image/webp'
    else:
        return 'image/jpeg'  # default

# Correct way to structure the request
image_path = "path/to/your/image.jpg"
base64_image = encode_image(image_path)
media_type = get_media_type(image_path)

messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{media_type};base64,{base64_image}"
                }
            }
        ]
    }
]
```

#### Solution 2: Using Image URLs
If you're using image URLs instead of base64:

```python
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "What's in this image?"
            },
            {
                "type": "image_url",
                "image_url": {
                    "url": "https://example.com/image.jpg"
                }
            }
        ]
    }
]
```

#### Solution 3: For Copilot Chat with Images
When using GitHub Copilot Chat with images:

1. Ensure images are properly formatted before sending
2. Use the correct media type in the data URI scheme
3. Check that the image file is not corrupted

#### Solution 4: Verify Image Format
```python
from PIL import Image
import io

def verify_and_get_format(image_path):
    """Verify image and get its format"""
    try:
        with Image.open(image_path) as img:
            # Get the format
            format = img.format.lower()
            print(f"Image format: {format}")
            
            # Convert format to media type
            media_types = {
                'jpeg': 'image/jpeg',
                'jpg': 'image/jpeg',
                'png': 'image/png',
                'gif': 'image/gif',
                'webp': 'image/webp'
            }
            return media_types.get(format, 'image/jpeg')
    except Exception as e:
        print(f"Error verifying image: {e}")
        return None
```

### Best Practices

1. **Always specify the media type** when working with images in API requests
2. **Validate image format** before encoding and sending
3. **Use appropriate MIME types**:
   - JPEG: `image/jpeg`
   - PNG: `image/png`
   - GIF: `image/gif`
   - WebP: `image/webp`
4. **Check API documentation** for specific requirements
5. **Handle errors gracefully** with try-catch blocks

### Example: Complete Working Code

```python
import base64
import requests
import os
from pathlib import Path

class ImageAPIClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.openai.com/v1/chat/completions"
    
    def get_image_media_type(self, image_path):
        """Determine media type from file extension"""
        extension = Path(image_path).suffix.lower()
        media_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }
        return media_types.get(extension, 'image/jpeg')
    
    def encode_image(self, image_path):
        """Encode image to base64"""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    
    def analyze_image(self, image_path, prompt="What's in this image?"):
        """Send image to API with proper media type"""
        # Get media type
        media_type = self.get_image_media_type(image_path)
        
        # Encode image
        base64_image = self.encode_image(image_path)
        
        # Construct request with proper structure
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-4-vision-preview",
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{media_type};base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 300
        }
        
        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            print(f"Response: {response.text}")
            raise
        except Exception as e:
            print(f"Error: {e}")
            raise

# Usage
if __name__ == "__main__":
    api_key = os.getenv("OPENAI_API_KEY")
    client = ImageAPIClient(api_key)
    
    try:
        result = client.analyze_image("path/to/image.jpg")
        print(result)
    except Exception as e:
        print(f"Failed to analyze image: {e}")
```

### Quick Checklist
- [ ] Image media type is specified (e.g., `image/jpeg`, `image/png`)
- [ ] Image is properly base64-encoded (if using base64)
- [ ] Request structure matches API requirements
- [ ] Image file is valid and not corrupted
- [ ] API key is valid and has necessary permissions
- [ ] Image size is within API limits

### Additional Resources
- [OpenAI Vision API Documentation](https://platform.openai.com/docs/guides/vision)
- [HTTP Media Types](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/MIME_types)
- [Data URIs](https://developer.mozilla.org/en-US/docs/Web/HTTP/Basics_of_HTTP/Data_URIs)

### Still Having Issues?
If you continue to experience this error:
1. Verify your image file is valid by opening it in an image viewer
2. Check the API documentation for specific requirements
3. Try with a different image format
4. Ensure your API version supports the features you're using
5. Check for any rate limiting or quota issues
