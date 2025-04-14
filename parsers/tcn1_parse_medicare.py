import json
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class Payer:
    payer_id: str
    deductible: str
    ded_remaining: str
    payer_status: str
    medicare_advantage_payer: Optional[str]
    medicare_advantage_portal: Optional[str]
    secondary_payer: Optional[str]
    crossover_payer: Optional[str]
    qualified_medicare_beneficiary: Optional[str]
    exception_notes: List[str]

def parse_medicare_response(file_path: str) -> Payer:
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Initialize exception notes list
    exception_notes = []
    
    # Get MBI (payer_id)
    payer_id = None
    for ident in data.get('DemographicInfo', {}).get('Subscriber', {}).get('Identification', []):
        if ident.get('Type') == 'Member ID':
            payer_id = ident.get('Code')
            break
    
    # Get deductible information
    deductible = "0.00"
    ded_remaining = "0.00"
    if 'HBPC_Deductible_OOP_Summary' in data:
        ded = data['HBPC_Deductible_OOP_Summary'].get('IndividualDeductibleInNet', {}).get('Value', '0.00')
        ded_rem = data['HBPC_Deductible_OOP_Summary'].get('IndividualDeductibleRemainingInNet', {}).get('Value', '0.00')
        if ded and ded_rem:
            deductible = ded.replace('$', '')
            ded_remaining = ded_rem.replace('$', '')
    
    # Determine payer status
    payer_status = "ineligible"
    if not data.get('ProcessedWithError', True):
        if data.get('PlanCoverageSummary', {}).get('Status') == 'Active':
            payer_status = "eligible"
    
    # Get Medicare Advantage information
    medicare_advantage_payer = None
    medicare_advantage_portal = None
    if data.get('IsHMOPlan', False):
        medicare_advantage_payer = data.get('MedicareInfoSummary', {}).get('AdvantagePayerName')
        # Note: Portal information would need to be mapped from the payer name
        # This is a simplified example - you would need to implement the actual mapping logic
    
    # Get secondary payer information
    secondary_payer = None
    if data.get('OtherPayerInfo', {}).get('SecondaryPayer'):
        secondary_payer = data['OtherPayerInfo']['SecondaryPayer']
    
    # Get crossover payer information
    crossover_payer = None
    if data.get('OtherPayerInfo', {}).get('PrimaryPayer'):
        primary_payer = data['OtherPayerInfo']['PrimaryPayer']
        # Check if it's a crossover payer based on business logic
        if primary_payer and primary_payer != "Medicare Part A and B":
            crossover_payer = primary_payer
    
    # Get QMB status
    qualified_medicare_beneficiary = None
    qmb_type = data.get('MedicareInfoSummary', {}).get('QMBPolicyType')
    if qmb_type and "QMB" in qmb_type.upper():
        qualified_medicare_beneficiary = qmb_type
    
    # Add exception notes for various conditions
    if data.get('ProcessedWithError'):
        exception_notes.append(f"API Error: {data.get('ErrorDescription', 'Unknown error')}")
    
    if not payer_id:
        exception_notes.append("No MBI found in response")
    
    if data.get('IsHMOPlan') and not medicare_advantage_payer:
        exception_notes.append("Medicare Advantage plan indicated but no payer name found")
    
    return Payer(
        payer_id=payer_id or "Unknown",
        deductible=deductible,
        ded_remaining=ded_remaining,
        payer_status=payer_status,
        medicare_advantage_payer=medicare_advantage_payer,
        medicare_advantage_portal=medicare_advantage_portal,
        secondary_payer=secondary_payer,
        crossover_payer=crossover_payer,
        qualified_medicare_beneficiary=qualified_medicare_beneficiary,
        exception_notes=exception_notes
    )

def process_directory(directory_path: str) -> List[Payer]:
    payers = []
    for file in Path(directory_path).glob('eligibility_response_Medical_Medicare Part A and B_*.json'):
        try:
            payer = parse_medicare_response(str(file))
            payers.append(payer)
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
    return payers

def main():
    # Process all JSON files in the output directory
    output_dir = 'data/output'
    payers = process_directory(output_dir)
    
    # Print results
    for payer in payers:
        print("\nPayer Information:")
        print(f"Payer ID: {payer.payer_id}")
        print(f"Deductible: ${payer.deductible}")
        print(f"Deductible Remaining: ${payer.ded_remaining}")
        print(f"Status: {payer.payer_status}")
        print(f"Medicare Advantage Payer: {payer.medicare_advantage_payer or 'None'}")
        print(f"Medicare Advantage Portal: {payer.medicare_advantage_portal or 'None'}")
        print(f"Secondary Payer: {payer.secondary_payer or 'None'}")
        print(f"Crossover Payer: {payer.crossover_payer or 'None'}")
        print(f"QMB Status: {payer.qualified_medicare_beneficiary or 'None'}")
        if payer.exception_notes:
            print("Exception Notes:")
            for note in payer.exception_notes:
                print(f"  - {note}")

if __name__ == "__main__":
    main() 