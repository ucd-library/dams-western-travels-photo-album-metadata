# MC-312: Western Travels of a Newly-Wed Couple Photograph Album

This repository contains the digital collection metadata and structure for the **Western Travels of a Newly-Wed Couple Photograph Album** (MC-312), part of the UC Davis Library Archives and Special Collections.

## 📖 Collection Overview

- **Title**: Western Travels of a Newly-Wed Couple Photograph Album
- **Collection Number**: MC312
- **Dates**: 1937-1941
- **Creators**: Marian and Jerry
- **OAC Finding Aid**: https://oac.cdlib.org/findaid/ark:/13030/c8251rdq/

### Collection Description

This album contains approximately 225 black and white photographs documenting the travels of newlyweds Marian and Jerry throughout California and the Southwest. The collection includes visits to:

**California Locations:**
- Monterey coast, Santa Cruz, San Simeon
- Buck's Lake, Marin County, San Francisco
- Mt. Lassen, Lake Tahoe, Muir Woods
- 1939 San Francisco World's Fair
- Oregon coast and Olympic Peninsula
- Badger Pass in Yosemite National Park

**1940 Colorado Trip:**
- Craig, Central City, Steamboat Springs
- Rocky Mountain National Park, Red Rocks
- Garden of the Gods, Colorado Springs
- Mesa Verde National Park, Royal Gorge
- Grand Canyon, Zion National Park
- Dinosaur National Monument, Salt Lake City

## 🏗️ Project Structure

```
dams_western_travels_photo_album/
├── README.md                           # This file
├── .gitignore                          # Git ignore rules
├── MC-312_COLLECTION_SUMMARY.md        # Collection summary
├── collection/                         # Collection metadata
│   └── mc-312/
│       ├── mc-312.jsonld.json         # Collection metadata
│       └── labels.jsonld.json         # Collection labels
├── items/                             # Item metadata
│   └── mc-312/
│       ├── mc-312.jsonld.json         # Item metadata (entire album)
│       └── media/
│           ├── mc-312.pdf.jsonld.json # PDF metadata
│           ├── images.jsonld.json     # Images container
│           └── images/                # Page-level metadata
│               ├── MC-312_0001.tif.jsonld.json
│               ├── MC-312_0002.tif.jsonld.json
│               └── ... (119 total pages)
├── mint_mc312_collection_ark.py       # Collection ARK minting script
├── mint_mc312_item_ark.py             # Item ARK minting script
├── update_ark_references.py           # ARK reference update script
└── create_page_metadata.py            # Page metadata generation script
```

## 🔑 Minted ARKs

- **Collection ARK**: `ark:/87293/d36m33b9q`
- **Item ARK**: `ark:/87293/d32v2cj5k`

## 📋 Current Status

### ✅ Completed
- [x] Collection metadata structure created
- [x] Item metadata structure created
- [x] Page-level metadata for all 119 images
- [x] Collection ARK minted
- [x] Item ARK minted
- [x] All ARK references updated
- [x] Ready for DAMS import

### 📋 Next Steps
- [ ] Import to DAMS development environment
- [ ] Verify collection display
- [ ] Deploy to production

## 🚀 DAMS Import Instructions

### Prerequisites
- Python 3.7+
- fin CLI tool installed
- EZID account credentials

### Import Process

1. **Configure fin for development:**
   ```bash
   fin config set host https://dev.dams.library.ucdavis.edu
   ```

2. **Authenticate:**
   ```bash
   fin auth login
   ```

3. **Import collection:**
   ```bash
   fin io import .
   ```

4. **Verify import:**
   - Check collection URL
   - Verify all 119 pages display correctly
   - Test ARK resolution

## 📁 Media Files

**Note**: The actual TIFF image files (MC-312_0001.tif through MC-312_0119.tif) are not included in this repository due to their large size (~35-43MB each). These files should be stored separately and referenced during the DAMS import process.

## 🔧 Scripts

### ARK Minting
- `mint_mc312_collection_ark.py`: Mints the collection-level ARK
- `mint_mc312_item_ark.py`: Mints the item-level ARK
- `update_ark_references.py`: Updates all cross-references after ARK minting

### Metadata Generation
- `create_page_metadata.py`: Generates page-level metadata for all 119 images

## 📞 Support

For issues with:
- **DAMS**: Contact UC Davis Library Digital Services
- **EZID**: Contact California Digital Library
- **Collection Content**: Contact UC Davis Archives and Special Collections

## 📄 License

This collection is licensed under [InC-NC](http://rightsstatements.org/vocab/InC-NC/1.0/) (In Copyright - Non-Commercial Use Permitted).

---

**Repository maintained by**: UC Davis Library Digital Services  
**Last updated**: 2025
