# Bloodhound CE Upload Tool

A lightweight, robust Python utility for seamlessly uploading Bloodhound JSON/ZIP data to a Bloodhound Community Edition (CE) instance.

Author: PaiN05

## Features
- Full support for Bloodhound CE's HMAC-SHA256 request signing setup for custom scripts.
- Optional database wipe functionality without needing external tools (`-delete`).
- Memory-safe chunked upload for large ZIP files.

## Installation

You can set up a global symlink and configure your credentials via `.zshrc` exports for easy usage from any directory.

1. Clone the repository
```
git clone https://github.com/jaytiwari05/BHCEupload.git
cd BHCEupload
pip install -r requirements.txt
```

2. Create a symlink to the script:
```bash
sudo ln -s $(pwd)/BHCEupload.py /usr/local/bin/BHCEupload.py
```

3. Add your Bloodhound credentials to your shell configuration for automatic integration:
```bash
echo 'export BH_TOKEN_ID=Your_Token_Id' >> ~/.zshrc
echo 'export BH_TOKEN_KEY=Your_Token_Key' >> ~/.zshrc
source ~/.zshrc
```

## Usage

You can use the tool globally once the above installation is complete by referencing `$BH_TOKEN_ID` and `$BH_TOKEN_KEY`.

**Clear the database and upload a file:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -dir /path/to/data.zip
```
<img width="973" height="418" alt="new-upload" src="https://github.com/user-attachments/assets/b1f8839b-05dc-4c5d-bb8a-84e954c04108" />


**Clear the database without uploading any files:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -delete
```
<img width="803" height="430" alt="new-delete" src="https://github.com/user-attachments/assets/e40fd88f-c924-4c5d-a16d-a19d3dbba19f" />

**Upload an entire directory to Bloodhound CE:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -dir /path/to/results/
```

> **Note:** The default target URL is `http://localhost:8080`. If your Bloodhound CE instance is hosted elsewhere, use the `-url` flag to specify the correct endpoint.
