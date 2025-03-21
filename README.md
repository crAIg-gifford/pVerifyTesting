## Overview
This tool automates the process of verifying insurance eligibility for patients by interfacing with pVerify's API. It processes patient data from Excel files and generates detailed eligibility responses.

## Features
- Processes patient data from Excel spreadsheets
- Supports both subscriber and dependent verification
- Handles multiple insurance payers
- Exports responses as JSON files
- Maintains organized data structure

## Links
- [pVerify API Documentation](https://pverify.com/api-documentation/)
- [pVerify Payer List](https://pverify.com/payer-list/)
- [pVerify Cost Calculator](https://docs.google.com/spreadsheets/d/1YNJ-GKqILvrFeaFD969Txb1CK0GqmyCgpg2xWQFXIK0/edit?gid=0#gid=0)

## Steps
1. Create a .env file in the root directory and cp the data found in [Bitwarden -> Portal Aggregator -> pVerify -> notes]
2. Download the [test_patients.xlsx](https://docs.google.com/spreadsheets/d/1keBz9R08m72Ox0506GAJUlb8zeGlcOy_/edit?gid=1356734240#gid=1356734240) file from Google Drive
3. Modify the file to include the patient data you want to verify (make sure to reference the correct payer code via pVerify's payer list)
4. Place the test_patients.xlsx in the data/input folder
5. Generate a token with the generate_token.py script
6. Update the BEARER_TOKEN in the .env file with the new access token
7. Run the main.py script
8. Output will be in the data/output folder# pVerifyTesting
