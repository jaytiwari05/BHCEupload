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
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -delete -dir /path/to/data.zip
```
<img width="1069" height="346" alt="BHCEupload-dir" src="https://github.com/user-attachments/assets/5e1545b1-bb85-4fe7-b153-7ee76ea60b43" />

**Clear the database without uploading any files:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -delete
```
<img width="819" height="320" alt="BHCEupload-delete" src="https://github.com/user-attachments/assets/c73f2429-4f11-4165-9522-0ff72ca36a62" />


**Upload an entire directory to Bloodhound CE:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -dir /path/to/results/
```

> **Note:** The default target URL is `http://localhost:8080`. If your Bloodhound CE instance is hosted elsewhere, use the `-url` flag to specify the correct endpoint.
