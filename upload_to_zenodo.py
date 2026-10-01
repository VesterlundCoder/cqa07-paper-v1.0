#!/usr/bin/env python3
"""Upload CQA07 paper package to Zenodo and obtain a DOI.

Usage:
    echo "YOUR_TOKEN" > ~/.zenodo_token
    chmod 600 ~/.zenodo_token
    python upload_to_zenodo.py
"""
import os
import sys
import json
import requests
from pathlib import Path

ZENODO_API = "https://zenodo.org/api/deposit/depositions"
REPO_DIR = Path("/tmp/cqa07-paper-v1.0")

def get_token():
    token_file = Path.home() / ".zenodo_token"
    if not token_file.exists():
        print("ERROR: Token file not found at ~/.zenodo_token")
        print("Run: echo 'YOUR_TOKEN' > ~/.zenodo_token && chmod 600 ~/.zenodo_token")
        sys.exit(1)
    token = token_file.read_text().strip()
    if not token:
        print("ERROR: Token file is empty")
        sys.exit(1)
    return token

def create_deposition(token):
    headers = {"Content-Type": "application/json"}
    params = {"access_token": token}
    data = {
        "metadata": {
            "title": "CQA07: Exact Zero-Error Communication Complexity of an Entanglement-Assisted Quantum Learning Task",
            "upload_type": "software",
            "description": (
                "Reproducibility package for the manuscript "
                "'Exact Zero-Error Communication Complexity of an "
                "Entanglement-Assisted Quantum Learning Task' submitted to "
                "npj Quantum Information. "
                "Contains: LaTeX source, compiled PDF, computational scripts "
                "(graph domination verification, protocol verification, "
                "Zhao-Deng sanity checks, figure generation), formal proofs, "
                "proof audit, reference ledger, claim ledger, and JSON result files. "
                "Main theorem: B*(n,1) = ceil(log2 f(n,3)) = ceil(log2 gamma_t(K_3^xn)). "
                "Asymptotic rate: B*(n,1) = n*log2(3/2) + O(1)."
            ),
            "creators": [
                {
                    "name": "Vesterlund, David",
                    "affiliation": "Vesterlund Ventures Holding AB, WestQuant Open",
                    "orcid": "0009-0000-6455-1141",
                }
            ],
            "keywords": [
                "quantum learning",
                "communication complexity",
                "ternary cube covering",
                "total domination",
                "pseudo-telepathy",
                "zero-error communication",
                "quantum advantage",
            ],
            "license": "MIT",
            "access_right": "open",
            "communities": [
                {"identifier": "npj-quantum-information"}
            ],
        }
    }
    print("Creating Zenodo deposition...")
    r = requests.post(ZENODO_API, params=params, json=data, headers=headers)
    r.raise_for_status()
    deposition = r.json()
    print(f"  Deposition ID: {deposition['id']}")
    return deposition

def upload_files(token, deposition_id):
    deposition_url = f"{ZENODO_API}/{deposition_id}"
    params = {"access_token": token}
    
    files_to_upload = []
    for root, dirs, files in os.walk(REPO_DIR):
        # Skip .git
        if ".git" in root:
            continue
        for f in files:
            filepath = Path(root) / f
            rel_path = filepath.relative_to(REPO_DIR)
            files_to_upload.append((filepath, rel_path))
    
    files_to_upload.sort(key=lambda x: str(x[1]))
    
    print(f"Uploading {len(files_to_upload)} files...")
    for i, (filepath, rel_path) in enumerate(files_to_upload, 1):
        # Use forward slashes for Zenodo
        zenodo_name = str(rel_path).replace(os.sep, "/")
        print(f"  [{i}/{len(files_to_upload)}] {zenodo_name} ({filepath.stat().st_size} bytes)")
        
        with open(filepath, "rb") as fh:
            r = requests.post(
                f"{deposition_url}/files",
                params=params,
                data={"name": zenodo_name},
                files={"file": fh},
            )
        if r.status_code not in (200, 201):
            print(f"    WARNING: status {r.status_code}: {r.text[:200]}")
    
    print("  All files uploaded.")

def publish_deposition(token, deposition_id):
    params = {"access_token": token}
    print("Publishing deposition...")
    r = requests.post(f"{ZENODO_API}/{deposition_id}/actions/publish", params=params)
    r.raise_for_status()
    deposition = r.json()
    doi = deposition.get("doi", "UNKNOWN")
    html_url = deposition.get("links", {}).get("html", "UNKNOWN")
    print(f"  DOI: {doi}")
    print(f"  URL: {html_url}")
    return doi, html_url

def main():
    token = get_token()
    deposition = create_deposition(token)
    deposition_id = deposition["id"]
    upload_files(token, deposition_id)
    doi, url = publish_deposition(token, deposition_id)
    
    print("\n" + "=" * 60)
    print("Zenodo upload complete!")
    print(f"  DOI:  {doi}")
    print(f"  URL:  {url}")
    print("=" * 60)
    
    # Save DOI for manuscript update
    doi_file = Path("/tmp/cqa07_zenodo_doi.txt")
    doi_file.write_text(f"DOI: {doi}\nURL: {url}\n")
    print(f"  Saved to: {doi_file}")

if __name__ == "__main__":
    main()
