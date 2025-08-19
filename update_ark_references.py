#!/usr/bin/env python3
"""
Update ARK references in all metadata files after minting collection and item ARKs.
This script automatically reads the minted ARKs and updates all references.
"""

import json
import os
from pathlib import Path

def extract_ark_from_identifiers(identifiers):
    """Extract ARK from identifier list"""
    for identifier in identifiers:
        if identifier.startswith('ark:/87293/'):
            return identifier
    return None

def update_ark_references(collection_ark, item_ark):
    """Update ARK references in all metadata files"""
    
    # Files to update
    files_to_update = [
        "collection/mc-312.jsonld.json",
        "items/mc-312.jsonld.json"
    ]
    
    for file_path in files_to_update:
        if not os.path.exists(file_path):
            print(f"⚠️  File {file_path} not found, skipping...")
            continue
            
        print(f"📝 Updating {file_path}...")
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        # Update collection file
        if "collection" in file_path:
            # Update image reference to use the item ARK
            if 'schema:image' in data:
                data['schema:image']['@id'] = f"info:fedora/item/{item_ark}/media/images/MC-312_0001.tif"
                print(f"  ✅ Updated image reference to use item ARK: {item_ark}")
        
        # Update item file
        elif "items" in file_path:
            # Update associatedMedia reference
            if 'schema:associatedMedia' in data:
                data['schema:associatedMedia']['@id'] = f"@base:/media/mc-312.pdf"
                print(f"  ✅ Updated associatedMedia reference")
        
        # Save updated file
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"  ✅ Updated {file_path}")

def main():
    print("🔧 UPDATING ARK REFERENCES IN MC-312 METADATA")
    print("="*50)
    
    # Read collection ARK from collection file
    collection_file = "collection/mc-312.jsonld.json"
    if not os.path.exists(collection_file):
        print(f"❌ Collection file {collection_file} not found!")
        return
    
    with open(collection_file, 'r') as f:
        collection_data = json.load(f)
    
    collection_ark = extract_ark_from_identifiers(collection_data.get('schema:identifier', []))
    
    # Read item ARK from item file
    item_file = "items/mc-312.jsonld.json"
    if not os.path.exists(item_file):
        print(f"❌ Item file {item_file} not found!")
        return
    
    with open(item_file, 'r') as f:
        item_data = json.load(f)
    
    item_ark = extract_ark_from_identifiers(item_data.get('schema:identifier', []))
    
    if not collection_ark or not item_ark:
        print("❌ Could not find ARKs in the files!")
        print(f"Collection ARK found: {collection_ark}")
        print(f"Item ARK found: {item_ark}")
        return
    
    print(f"📋 Collection ARK: {collection_ark}")
    print(f"📋 Item ARK: {item_ark}")
    
    # Confirm
    response = input(f"\n🔄 Update ARK references? (y/N): ")
    if response.lower() != 'y':
        print("❌ Cancelled.")
        return
    
    # Update references
    update_ark_references(collection_ark, item_ark)
    
    print(f"\n✅ ARK references updated successfully!")
    print(f"📁 Ready for DAMS import")

if __name__ == "__main__":
    main()
