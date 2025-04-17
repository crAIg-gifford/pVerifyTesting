import requests
import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime
from requests.exceptions import RequestException

# Load environment variables
load_dotenv()

API_BASE_URL = os.getenv("pVERIFY_API_BASE_URL")
BEARER_TOKEN = os.getenv("pVERIFY_BEARER_TOKEN")
CLIENT_ID = os.getenv("pVERIFY_CLIENT_ID")
CONTENT_TYPE = os.getenv("pVERIFY_CONTENT_TYPE")

HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}",
    "Client-API-Id": f"{CLIENT_ID}",
    "Content-Type": f"{CONTENT_TYPE}",
}


def make_request(method, eligibility_type, payload):
    """
    Generic function to handle GET and POST requests.
    """
    if eligibility_type == "Dental":
        endpoint = "DentalEligibilitySummary"
    elif eligibility_type == "Medical":
        endpoint = "EligibilitySummary"
    url = f"{API_BASE_URL}{endpoint}"
    print(f"URL: {url}")
    try:
        if method == "GET":
            response = requests.get(url, headers=HEADERS)
        elif method == "POST":
            response = requests.post(
                url,
                headers=HEADERS,
                data=json.dumps(payload)
            )

        response.raise_for_status()
        return response.json()
    except RequestException as error:
        return {"error": str(error)}


def get_data(endpoint):
    return make_request("GET", endpoint)


def post_data(eligibility_type, payload):
    return make_request("POST", eligibility_type, payload)


def format_date(value):
    return value.strftime('%m/%d/%Y') if not pd.isna(value) else None


def export_response(
    response, row_index, eligibility_type, payer_name, subscriber_id
):
    """
    Export API response to a JSON file in the data/output directory.
    """
    if response.get("error"):
        print(f"Error: {response.get('error')}")
        return
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    safe_payer_name = "".join(
        c for c in payer_name if c.isalnum() or c in (' ', '-', '_')
    ).strip()
    filename = os.path.join(
        'data', 'output',
        f"eligibility_response_{eligibility_type}_"
        f"{safe_payer_name}_{subscriber_id}_"
        f"{row_index}_{timestamp}.json"
    )
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, 'w') as f:
        json.dump(response, f, indent=4)
    print(f"Response exported to: {filename}")


def process_patient_data(row):
    """
    Process individual patient row data into required payload format.
    """

    payload = {
        "payerCode": str(row['PayerID']),
        "payerName": str(row['Payer Name']),
        "provider": {
            "lastName": str(row['Provider']),
            "npi": str(row['NPI'])
        },
        "subscriber": {
            "firstName": str(row['Subscriber First']),
            "lastName": str(row['Subscriber Last']),
            "dob": format_date(row['Subscriber DOB']),
            "memberID": str(row['Subscriber ID'])
        },
        "isSubscriberPatient": "true",
        "doS_StartDate": f"{datetime.now().strftime('%m/%d/%Y')}",
        "doS_EndDate": f"{datetime.now().strftime('%m/%d/%Y')}",
        "Location": "TA",
        "IncludeHtmlResponse": True
    }

    # Search the pVerify website and determine the PracticeTypeCode
    payload["PracticeTypeCode"] = "21"

    return payload


def main():
    df = pd.read_excel(
        os.path.join('data', 'input', 'test_patients.xlsx'),
        dtype={"PayerID": str}
    )

    my_results = []
    # Process and submit data
    for index, row in df.iterrows():
        print(
            f"Processing row {index}: {row['Type']}, {row['Payer Name']}, "
            f"{row['Subscriber ID']}"
        )
        payload = process_patient_data(row)
        print("\nProcessed Patient Data:")
        print(json.dumps(payload, indent=4))
        # API call
        response = post_data(row['Type'], payload)
        if response.get("error"):
            my_results.append("Error")
        else:
            my_results.append("Success")
        print("\nAPI Response:")
        print(json.dumps(response, indent=4))
        # Export response to JSON file with payer name and subscriber ID
        export_response(
            response, 
            index, 
            str(row['Type']),
            str(row['Payer Name']),
            str(row['Subscriber ID'])
        )
    print(f"Results: {my_results}")


if __name__ == "__main__":
    main()
