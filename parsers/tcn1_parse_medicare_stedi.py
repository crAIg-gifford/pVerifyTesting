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

def parse_x12_segment(x12: str, segment_type: str) -> Dict[str, str]:
    """Parse X12 segments to extract specific information."""
    segments = x12.split('~')
    for segment in segments:
        if segment.startswith(segment_type):
            elements = segment.split('*')
            return {
                'segment_type': elements[0],
                'elements': elements[1:]
            }
    return {}

def parse_medicare_response(file_path: str) -> Payer:
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # Initialize exception notes list
    exception_notes = []
    
    # Extract MBI from filename
    payer_id = file_path.split('_')[-3]  # Assuming format: ..._MBI_INDEX_TIMESTAMP.json
    
    # Default values for deductible information
    deductible = "0.00"
    ded_remaining = "0.00"
    
    # Determine payer status based on errors
    payer_status = "ineligible"
    if not data.get('errors'):
        payer_status = "eligible"
    else:
        for error in data.get('errors', []):
            exception_notes.append(f"Error: {error.get('description')} - {error.get('followupAction')}")
    
    # Check for Medicare Advantage
    medicare_advantage_payer = None
    medicare_advantage_portal = None
    
    # Check for secondary payer
    secondary_payer = None
    
    # Check for crossover payer
    crossover_payer = None
    
    # Check for QMB status
    qualified_medicare_beneficiary = None
    
    # Parse X12 data for additional information
    x12_data = parse_x12_segment(data.get('x12', ''), 'AAA')
    if x12_data:
        # Add any relevant X12 parsing logic here
        pass
    
    return Payer(
        payer_id=payer_id,
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
    for file in Path(directory_path).glob('stedi_eligibility_response_Medical_Medicare Part A and B_*.json'):
        try:
            payer = parse_medicare_response(str(file))
            payers.append(payer)
        except Exception as e:
            print(f"Error processing {file}: {str(e)}")
    return payers

def main():
    # Process all JSON files in the output directory
    output_dir = 'data/output_stedi'
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