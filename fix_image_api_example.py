#!/usr/bin/env python3
"""
Example script to demonstrate proper image API usage with media types.
This addresses the "image media type is required" error.

Usage:
    python fix_image_api_example.py --image path/to/image.jpg --prompt "Describe this image"
"""

import base64
import argparse
import sys
from pathlib import Path
from typing import Optional


def get_image_media_type(image_path: str) -> str:
    """
    Determine the correct media type based on file extension.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Media type string (e.g., 'image/jpeg')
    """
    extension = Path(image_path).suffix.lower()
    media_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.webp': 'image/webp',
        '.bmp': 'image/bmp',
        '.tiff': 'image/tiff',
        '.tif': 'image/tiff',
    }
    return media_types.get(extension, 'image/jpeg')


def encode_image_to_base64(image_path: str) -> Optional[str]:
    """
    Encode an image file to base64 string.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        Base64 encoded string or None if error occurs
    """
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
    except FileNotFoundError:
        print(f"Error: Image file not found: {image_path}")
        return None
    except Exception as e:
        print(f"Error encoding image: {e}")
        return None


def create_api_payload(image_path: str, prompt: str = "What's in this image?") -> dict:
    """
    Create a properly formatted API payload with image media type.
    
    This is the CORRECT way to structure the request to avoid the
    "image media type is required" error.
    
    Args:
        image_path: Path to the image file
        prompt: Text prompt for the API
        
    Returns:
        Dictionary containing the properly formatted API payload
    """
    # Step 1: Determine the correct media type
    media_type = get_image_media_type(image_path)
    print(f"✓ Detected media type: {media_type}")
    
    # Step 2: Encode the image
    base64_image = encode_image_to_base64(image_path)
    if not base64_image:
        return None
    print(f"✓ Image encoded to base64 ({len(base64_image)} characters)")
    
    # Step 3: Create properly formatted payload
    # This is the KEY: each content item must have a "type" field
    payload = {
        "model": "gpt-4-vision-preview",  # or your preferred model
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",  # ← IMPORTANT: specify type
                        "text": prompt
                    },
                    {
                        "type": "image_url",  # ← IMPORTANT: specify type
                        "image_url": {
                            # Include media type in the data URI
                            "url": f"data:{media_type};base64,{base64_image}"
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    print("✓ Payload created successfully with proper media type")
    return payload


def create_api_payload_with_url(image_url: str, prompt: str = "What's in this image?") -> dict:
    """
    Create API payload using an image URL instead of base64.
    
    Args:
        image_url: URL to the image
        prompt: Text prompt for the API
        
    Returns:
        Dictionary containing the properly formatted API payload
    """
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",  # ← IMPORTANT: specify type
                        "text": prompt
                    },
                    {
                        "type": "image_url",  # ← IMPORTANT: specify type
                        "image_url": {
                            "url": image_url
                        }
                    }
                ]
            }
        ],
        "max_tokens": 300
    }
    
    print("✓ Payload created successfully for image URL")
    return payload


def demonstrate_incorrect_format():
    """
    Show what NOT to do - this will cause the error.
    """
    print("\n❌ INCORRECT FORMAT (will cause error):")
    print("-" * 50)
    
    incorrect_payload = {
        "messages": [
            {
                "role": "user",
                "content": [
                    "What's in this image?",  # Missing "type" field
                    {
                        # Missing "type" field here too!
                        "image_url": "data:image/jpeg;base64,..."
                    }
                ]
            }
        ]
    }
    
    import json
    print(json.dumps(incorrect_payload, indent=2))
    print("\nThis format is missing the 'type' field and will result in:")
    print('{"error":{"message":"image media type is required","code":"invalid_request_body"}}')


def demonstrate_correct_format(image_path: str, prompt: str):
    """
    Show the correct format that will work.
    """
    print("\n✓ CORRECT FORMAT (will work):")
    print("-" * 50)
    
    payload = create_api_payload(image_path, prompt)
    
    if payload:
        # Show a truncated version for readability
        import json
        display_payload = payload.copy()
        if display_payload["messages"][0]["content"][1]["image_url"]["url"].startswith("data:"):
            base64_part = display_payload["messages"][0]["content"][1]["image_url"]["url"]
            # Truncate the base64 string for display
            if len(base64_part) > 100:
                media_type = base64_part.split(';')[0]
                display_payload["messages"][0]["content"][1]["image_url"]["url"] = f"{media_type};base64,...[truncated]..."
        
        print(json.dumps(display_payload, indent=2))
        print("\n✓ This format includes the 'type' field and will work correctly!")
        
        return payload
    return None


def main():
    """Main function to demonstrate proper usage."""
    parser = argparse.ArgumentParser(
        description="Demonstrate proper image API usage with media types"
    )
    parser.add_argument(
        "--image",
        type=str,
        help="Path to image file"
    )
    parser.add_argument(
        "--image-url",
        type=str,
        help="URL to image (alternative to --image)"
    )
    parser.add_argument(
        "--prompt",
        type=str,
        default="What's in this image?",
        help="Prompt to use with the image"
    )
    parser.add_argument(
        "--show-incorrect",
        action="store_true",
        help="Show the incorrect format that causes errors"
    )
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("Image API Media Type Example")
    print("=" * 60)
    
    if args.show_incorrect:
        demonstrate_incorrect_format()
    
    if args.image:
        if not Path(args.image).exists():
            print(f"\n❌ Error: Image file not found: {args.image}")
            sys.exit(1)
        
        payload = demonstrate_correct_format(args.image, args.prompt)
        
        if payload:
            print("\n" + "=" * 60)
            print("Summary:")
            print("=" * 60)
            print("✓ Media type properly specified")
            print("✓ Image properly encoded")
            print("✓ Request structure is correct")
            print("\nYou can now use this payload with your API client!")
            print("\nExample usage:")
            print("  import requests")
            print("  response = requests.post(")
            print("      'https://api.openai.com/v1/chat/completions',")
            print("      headers={'Authorization': f'Bearer {api_key}'},")
            print("      json=payload")
            print("  )")
            
    elif args.image_url:
        payload = create_api_payload_with_url(args.image_url, args.prompt)
        import json
        print(json.dumps(payload, indent=2))
        print("\n✓ Payload created successfully for image URL!")
    else:
        print("\n" + "=" * 60)
        print("No image provided. Showing format examples:")
        print("=" * 60)
        demonstrate_incorrect_format()
        
        print("\n\nFor a complete example with your image, run:")
        print("  python fix_image_api_example.py --image path/to/your/image.jpg")
        print("\nOr with an image URL:")
        print("  python fix_image_api_example.py --image-url https://example.com/image.jpg")


if __name__ == "__main__":
    main()
