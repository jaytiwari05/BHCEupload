#!/usr/bin/env python3
import argparse
import base64
import hashlib
import hmac
import json
import logging
import os
import sys
from datetime import datetime, timezone
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%Y/%m/%d %H:%M:%S')

def sign_request(method, uri, token_key, datetime_formatted, body_data=""):
    key1 = token_key.encode('utf-8')
    mac1 = hmac.new(key1, (method + uri).encode('utf-8'), hashlib.sha256).digest()
    mac2 = hmac.new(mac1, datetime_formatted[:13].encode('utf-8'), hashlib.sha256).digest()
    mac3 = hmac.new(mac2, b"", hashlib.sha256)
    
    if isinstance(body_data, bytes) and body_data:
        mac3.update(body_data)
    elif isinstance(body_data, str) and body_data:
        with open(body_data, 'rb') as f:
            while chunk := f.read(8192):
                mac3.update(chunk)
                
    return base64.b64encode(mac3.digest()).decode('utf-8')

def query_bloodhound_api(url_base, uri, method, token_id, token_key, body_data="", content_type="application/json"):
    now = datetime.now(timezone.utc).astimezone()
    datetime_formatted = now.strftime("%Y-%m-%dT%H:%M:%S.%f")
    
    tz = now.strftime("%z")
    if tz:
        tz = tz[:-2] + ":" + tz[-2:]
    else:
        tz = "+00:00"
    datetime_formatted += tz
    
    signature = sign_request(method, uri, token_key, datetime_formatted, body_data)
    
    headers = {
        "User-Agent": "simple-uploader-v0.1",
        "Authorization": f"bhesignature {token_id}",
        "RequestDate": datetime_formatted,
        "Signature": signature,
        "Content-Type": content_type
    }
    
    full_url = f"{url_base.rstrip('/')}{uri}"
    
    try:
        if isinstance(body_data, bytes) or not body_data:
            resp = requests.request(method, full_url, headers=headers, data=body_data if body_data else None)
        else:
            with open(body_data, 'rb') as f:
                resp = requests.request(method, full_url, headers=headers, data=f)
                
        if resp.status_code not in (200, 201, 202, 204):
            raise Exception(f"unexpected HTTP status code: {resp.status_code} - {resp.text}")
            
        if resp.text:
            return resp.json()
        return {}
    except requests.exceptions.RequestException as e:
        raise Exception(f"{e}")

def clear_database(url_base, token_id, token_key):
    uri = "/api/v2/clear-database"
    payload = {
        "deleteCollectedGraphData": True,
        "deleteFileIngestHistory": True,
        "deleteDataQualityHistory": True,
        "deleteAssetGroupSelectors": [0]
    }
    body_bytes = json.dumps(payload).encode('utf-8')
    logging.info("Initiating database wipe via POST /api/v2/clear-database...")
    try:
        query_bloodhound_api(url_base, uri, "POST", token_id, token_key, body_bytes, "application/json")
        logging.info("Database wiped successfully.")
    except Exception as e:
        logging.error(f"Failed to wipe database: {e}")
        raise e

def upload_data(url_base, file_path, token_id, token_key):
    start_resp = query_bloodhound_api(url_base, "/api/v2/file-upload/start", "POST", token_id, token_key)
    if "data" not in start_resp or "id" not in start_resp["data"]:
        raise Exception(f"Failed to start upload job. Response: {start_resp}")
    
    job_id = start_resp["data"]["id"]
    logging.info(f"Processing job ID: {job_id}")
    
    content_type = "application/zip-compressed" if file_path.endswith(".zip") else "application/json"
    uri = f"/api/v2/file-upload/{job_id}"
    query_bloodhound_api(url_base, uri, "POST", token_id, token_key, file_path, content_type)
    
    end_uri = f"/api/v2/file-upload/{job_id}/end"
    query_bloodhound_api(url_base, end_uri, "POST", token_id, token_key)
    logging.info(f"Data uploaded successfully for job ID: {job_id}")

def process_single_file(file_path, url_base, token_id, token_key):
    if not (file_path.endswith(".json") or file_path.endswith(".zip")):
        return
        
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    logging.info(f"Uploading file {file_path}, size: {size_mb:.2f} MB")
    
    if size_mb > 20000:
        logging.info(f"File {file_path} is quite large, will most likely fail, use chophound to make it smaller or compress it using zip, skipping.")
        return
    
    try:
        upload_data(url_base, file_path, token_id, token_key)
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

def process_path(path_arg, url_base, token_id, token_key):
    if os.path.isfile(path_arg):
        process_single_file(path_arg, url_base, token_id, token_key)
    elif os.path.isdir(path_arg):
        for root, _, files in os.walk(path_arg):
            for file in files:
                file_path = os.path.join(root, file)
                process_single_file(file_path, url_base, token_id, token_key)
    else:
        print(f"Error walking the path {path_arg}: not found")

def banner():
    print('''\033[91m
 ____  _   _  ____ _____   _   _       _                 _ 
| __ )| | | |/ ___| ____| | | | |_ __ | | ___   __ _  __| |
|  _ \\| |_| | |   |  _|   | | | | '_ \\| |/ _ \\ / _` |/ _` |
| |_) |  _  | |___| |___  | |_| | |_) | | (_) | (_| | (_| |
|____/|_| |_|\\____|_____|  \\___/| .__/|_|\\___/ \\__,_|\\__,_|
                                |_|                        \033[0m
                                                       
   \033[96mBloodhound CE Upload\033[0m
   \033[93mAuthor : PaiN05\033[0m
''')

def main():
    parser = argparse.ArgumentParser(
        description="\033[96mBloodhound CE Custom Uploader (Python)\033[0m\n\n"
                    "Uploads JSON/ZIP Bloodhound data to a Bloodhound CE instance.\n"
                    "Optionally clears the database before uploading.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="Examples:\n"
               "  \033[92mUpload a directory:\033[0m\n"
               "  python3 BHCEupload.py -tokenid <ID> -tokenkey <KEY> -dir /path/to/data\n\n"
               "  \033[92mClear database only:\033[0m\n"
               "  python3 BHCEupload.py -tokenid <ID> -tokenkey <KEY> -delete\n\n"
               "  \033[92mClear database and upload a file:\033[0m\n"
               "  python3 BHCEupload.py -tokenid <ID> -tokenkey <KEY> -delete -dir file.zip"
    )
    parser.add_argument("-url", default="http://localhost:8080", help="Bloodhound Target URL (default: http://localhost:8080)")
    parser.add_argument("-tokenid", required=False, help="Bloodhound Token ID")
    parser.add_argument("-tokenkey", required=False, help="Bloodhound Token Key")
    parser.add_argument("-dir", help="Directory or file path to process and upload")
    parser.add_argument("-delete", action="store_true", help="Clear Bloodhound database before processing uploads")
    
    args = parser.parse_args()
    banner()
    
    if not args.tokenid or not args.tokenkey:
        print("\033[91m[!] Please provide all required flags: -tokenid, -tokenkey\033[0m")
        print("\033[93m[i] Use -h or --help for usage details.\033[0m")
        return
    
    if args.delete:
        try:
            clear_database(args.url, args.tokenid, args.tokenkey)
        except Exception as e:
            pass
            
    if args.dir:
        process_path(args.dir, args.url, args.tokenid, args.tokenkey)

if __name__ == "__main__":
    main()
