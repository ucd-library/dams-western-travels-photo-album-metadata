#!/usr/bin/env python3
"""
Generate metadata files for all page images in the MC-312 book collection.
This script creates individual JSON-LD metadata files for each TIFF page.
"""

import os
import json

def create_page_metadata(page_number):
    """Create metadata for a single page image."""
    
    # Format page number with leading zeros (4 digits)
    page_num_str = f"{page_number:04d}"
    filename = f"MC-312_{page_num_str}.tif"
    
    metadata = {
        "@context": {
            "ldp": "http://www.w3.org/ns/ldp#",
            "schema": "http://schema.org/",
            "fedora": "http://fedora.info/definitions/v4/repository#",
            "webac": "http://fedora.info/definitions/v4/webac#",
            "acl": "http://www.w3.org/ns/auth/acl#",
            "ucdlib": "http://digital.ucdavis.edu/schema#",
            "ebucore": "http://www.ebu.ch/metadata/ontologies/ebucore/ebucore#"
        },
        "@id": "",
        "@type": [
            "schema:ImageObject",
            "schema:MediaObject",
            "schema:CreativeWork"
        ],
        "schema:position": page_num_str,
        "ebucore:filename": filename,
        "ebucore:hasMimeType": "image/tiff"
    }
    
    return metadata, filename

def main():
    """Generate metadata files for all 119 pages."""
    
    # Create the images directory if it doesn't exist
    images_dir = "items/mc-312/media/images"
    os.makedirs(images_dir, exist_ok=True)
    
    # Generate metadata for pages 1-119
    for page_num in range(1, 120):
        metadata, filename = create_page_metadata(page_num)
        
        # Create the metadata file
        metadata_filename = f"{filename}.jsonld.json"
        metadata_path = os.path.join(images_dir, metadata_filename)
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        print(f"Created metadata for {filename}")
    
    print(f"\nGenerated metadata for {119} page images in {images_dir}/")

if __name__ == "__main__":
    main()
