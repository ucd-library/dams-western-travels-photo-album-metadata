import json
import requests
import base64
from pathlib import Path

# EZID API configuration
EZID_BASE_URL = "https://ezid.cdlib.org"
SHOULDER = "ark:/87293/d3"  # UC Davis ARK shoulder
USERNAME = "ucd-dams-3"
PASSWORD = "ezid2025!"

def get_auth_header():
    """Create Basic Auth header for EZID API"""
    credentials = base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
    return {"Authorization": f"Basic {credentials}"}

def mint_collection_ark(metadata):
    """Mint a new ARK for the collection using the EZID API"""
    url = f"{EZID_BASE_URL}/shoulder/{SHOULDER}"
    headers = {
        "Content-Type": "text/plain; charset=UTF-8",
        "Accept": "text/plain",
        **get_auth_header()
    }
    
    # Format metadata in ANVL format for collection
    anvl_metadata = []
    anvl_metadata.append(f"_target: {metadata.get('target_url', '')}")
    anvl_metadata.append(f"_profile: erc")
    anvl_metadata.append(f"erc.what: {metadata.get('title', '')}")
    anvl_metadata.append(f"erc.who: Marian and Jerry")  # Original creators
    anvl_metadata.append(f"erc.where: California")  # Geographic location
    
    data = "\n".join(anvl_metadata)
    
    try:
        print(f"🚀 Minting new collection ARK...")
        print(f"Metadata:\n{data}")
        
        response = requests.post(url, headers=headers, data=data)
        print(f"Response status: {response.status_code}")
        print(f"Response: {response.text}")
        
        response.raise_for_status()
        
        if response.text.startswith("success:"):
            return response.text.split("success:")[1].strip()
        else:
            print(f"❌ Error: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Request error: {e}")
        return None

def update_collection_ark():
    """Update the MC-312 collection with a new ARK"""
    collection_file = Path("collection/mc-312.jsonld.json")
    
    if not collection_file.exists():
        print(f"❌ File {collection_file} not found!")
        return
    
    # Read current data
    with open(collection_file, 'r') as f:
        data = json.load(f)
    
    # Get current identifier
    current_identifier = data.get('schema:identifier', [])
    print(f"📋 Current identifier: {current_identifier}")
    
    # Extract metadata
    metadata = {
        'title': data.get('schema:name', ''),
        'creator': 'UC Davis Library, Archives and Special Collections',
        'subjects': [
            'Photograph albums',
            'Travel photography',
            'California history'
        ],
        'target_url': "https://digital.ucdavis.edu/collection/mc-312"
    }
    
    print(f"📝 Title: '{metadata['title']}'")
    print(f"📝 Creator: '{metadata['creator']}'")
    print(f"📝 Subjects: {metadata['subjects']}")
    
    # Confirm
    response = input(f"\n🔄 Mint new ARK for MC-312 collection? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled.")
        return
    
    # Mint new ARK
    new_ark = mint_collection_ark(metadata)
    if new_ark:
        # Update identifier - keep MC312 and OAC link, add new ARK
        new_identifier = [
            "MC312",
            new_ark,
            "https://oac.cdlib.org/findaid/ark:/13030/c8251rdq/"
        ]
        
        data['schema:identifier'] = new_identifier
        
        # Save updated file
        with open(collection_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ SUCCESS!")
        print(f"🆕 New ARK: {new_ark}")
        print(f"📁 Updated: {collection_file}")
        print(f"🔧 Kept MC312 and OAC link identifiers")
        
        # Also update the image reference in the collection
        if 'schema:image' in data:
            data['schema:image']['@id'] = f"info:fedora/item/{new_ark}/media/images/MC-312_0001.tif"
            with open(collection_file, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"🔧 Updated image reference with new ARK")
        
    else:
        print(f"❌ Failed to mint new ARK")

if __name__ == "__main__":
    print("🔧 MINTING NEW COLLECTION ARK FOR MC-312")
    print("="*50)
    update_collection_ark()
