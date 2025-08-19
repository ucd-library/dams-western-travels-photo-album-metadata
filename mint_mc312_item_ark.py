import json
import requests
import base64
from pathlib import Path
import time

# EZID API configuration
EZID_BASE_URL = "https://ezid.cdlib.org"
SHOULDER = "ark:/87293/d3"  # UC Davis ARK shoulder
USERNAME = "ucd-dams-3"
PASSWORD = "ezid2025!"

def get_auth_header():
    """Create Basic Auth header for EZID API"""
    credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}

def mint_ark(metadata):
    """Mint a new ARK using the EZID API"""
    url = f"{EZID_BASE_URL}/shoulder/{SHOULDER}"
    headers = {
        "Content-Type": "text/plain; charset=UTF-8",
        "Accept": "text/plain",
        **get_auth_header()
    }
    
    # Format metadata in ANVL format
    anvl_metadata = []
    anvl_metadata.append(f"_target: {metadata.get('target_url', '')}")
    anvl_metadata.append(f"_profile: erc")
    anvl_metadata.append(f"erc.what: {metadata.get('title', '')}")
    anvl_metadata.append(f"erc.who: {metadata.get('creator', '')}")
    
    # Add subject information
    subjects = metadata.get('subjects', [])
    if subjects:
        subject_names = [subj for subj in subjects if subj]
        if subject_names:
            anvl_metadata.append(f"erc.where: {'; '.join(subject_names[:3])}")
    
    # Join metadata with newlines
    data = "\n".join(anvl_metadata)
    
    try:
        print(f"Sending request to {url}")
        print(f"With metadata:\n{data}")
        
        response = requests.post(url, headers=headers, data=data)
        
        # Print full response for debugging
        print(f"Response status: {response.status_code}")
        print(f"Response text: {response.text}")
        
        response.raise_for_status()
        
        # Extract ARK from response
        if response.text.startswith("success:"):
            return response.text.split("success:")[1].strip()
        else:
            print(f"Error minting ARK: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error making request: {e}")
        if hasattr(e.response, 'text'):
            print(f"Error response: {e.response.text}")
        return None

def update_item_ark():
    """Update the MC-312 item with a new ARK"""
    item_file = Path("items/mc-312.jsonld.json")
    
    if not item_file.exists():
        print(f"❌ File {item_file} not found!")
        return
    
    # Read current data
    with open(item_file, 'r') as f:
        data = json.load(f)
    
    # Get current identifier
    current_identifier = data.get('schema:identifier', [])
    print(f"📋 Current identifier: {current_identifier}")
    
    # Extract metadata
    metadata = {
        'title': data.get('schema:name', ''),
        'creator': data.get('schema:creator', ''),
        'subjects': [
            'Photograph albums',
            'Travel photography', 
            'California history',
            'National parks',
            'Honeymoon travel'
        ],
        'target_url': "https://digital.ucdavis.edu/item/mc-312"
    }
    
    print(f"📝 Title: '{metadata['title']}'")
    print(f"📝 Creator: '{metadata['creator']}'")
    print(f"📝 Subjects: {metadata['subjects']}")
    
    # Confirm
    response = input(f"\n🔄 Mint new ARK for MC-312 item? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled.")
        return
    
    # Mint new ARK
    new_ark = mint_ark(metadata)
    if new_ark:
        # Update identifier - keep MC312, add new ARK
        new_identifier = [
            "MC312",
            new_ark
        ]
        
        data['schema:identifier'] = new_identifier
        
        # Save updated file
        with open(item_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ SUCCESS!")
        print(f"🆕 New ARK: {new_ark}")
        print(f"📁 Updated: {item_file}")
        print(f"🔧 Kept MC312 identifier")
        
        # Also update the image reference in the item
        if 'schema:image' in data:
            data['schema:image']['@id'] = f"@base:/media/images/MC-312_0001.tif"
            with open(item_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"🔧 Updated image reference")
        
    else:
        print(f"❌ Failed to mint new ARK")

if __name__ == "__main__":
    print("🔧 MINTING NEW ITEM ARK FOR MC-312")
    print("="*50)
    update_item_ark()
