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

**Upload an entire directory to Bloodhound CE:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -dir /path/to/results/
```

**Clear the database without uploading any files:**
```bash
BHCEupload.py -tokenid $BH_TOKEN_ID -tokenkey $BH_TOKEN_KEY -delete
```

> **Note:** The default target URL is `http://localhost:8080`. If your Bloodhound CE instance is hosted elsewhere, use the `-url` flag to specify the correct endpoint.
