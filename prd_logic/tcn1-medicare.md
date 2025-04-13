## Macro 2A.0 - Process Medicare NGS

### Macro 2A.1 - Login to Medicare NGS

1. Navigate to the Medicare NGS portal
*Note: URL =* https://www.ngsmedicare.com/NGS_LandingPage/Home
2. In the `Attestation` pop-up, click  `Accept`
3. Navigate to the `Log into NGSConnex` ****section
4. Enter Login Information
    1. Get “TCN Medicare NGS” Credentials from  [Get Bitwarden Credentials](https://www.notion.so/Get-Bitwarden-Credentials-19da01e4ef3f45b89f992a1208675fb4?pvs=21) 
    2. `User ID` = `Username`
    3. `Password` = `Password`
    4. Click the `Enter` button
    5. In the `Multi-Factor Authentication` pop-up, select `Email`
    6. Click the `Send Security Code` button
    7. Retrieve the `access code` from the email associated with `Office 365 - NEHS` account
    8. Enter `access code` into the input
    9. Click the `Verify Code` button
5. Loop over patients:
    1. For each `{patient}` in `{run.patients}`
        1. Go to the next step
6. Loop over payers:
    1. For each `{payer}` in `{patient.payers}`
        1. Go to the next step
7. Check for Medicare NGS
    1. Is `{payer.portal}` = “Medicare NGS Connex”?
        1. Y - Go to the next step
        2. N - Skip to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21) 
8. Go to [Macro 2A.2 - Search for Patient](https://www.notion.so/Macro-2A-2-Search-for-Patient-d0d54be979a04bedaa3ae729f76edc0b?pvs=21)

### Macro 2A.2 - Search for Patient

1. Click the `Eligibility Lookup` button
*Note: URL =* https://www.ngsmedicare.com/NGS_Portal/EligibilitySearch
2. Navigate to the `Provider` table
3. Click the `Select` button in the top row
4. Enter Patient Information
    1. `Medicare Number` = `{payer.policy_id}`
    2. `Last Name` = `{patient.last}`
    3. `First Name` = `{patient.first}`
    4. `Date of Birth` = `{patient.dob}`
    5. Click the `Submit` button
    6. Did additional Filters appear?
        1. Y - Skip to the [Enter Additional Filters](https://www.notion.so/Enter-Additional-Filters-6ca719eb464f4ff690bbd4ff5e3cd0dc?pvs=21) step
        2. N - Go to the next step
    7. Did an error pop-up with text = "The Medicare Number provided isn’t a valid MBI format.” appear?
        1. Y - Go to the next step
        2. N - Take the following actions:
            - `{payer.note}` = “Could not find Patient in Medicare NGS Payer search.”
            - `{payer.payer_status}` = “Error”
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Could not find Patient in Medicare NGS Payer search. ”
                - `{ExceptionNote.type}` = “Client Not Found on Portal”
            - Go back to [Macro 2.8 - Check for Last Payer](https://www.notion.so/Macro-2-8-Check-for-Last-Payer-f4bbad0d532b49ef9c561f1694f67b7d?pvs=21)
    8. Is `{patient.ssn}` = “”?
    *Note: SSN is a required field in the next step. Often patients do not have this provided in Valant. The next step also involves a captcha. So let’s filter out a patient without the required fields before we have to maybe solve a captcha for run-time concerns*
        1. Y - Take the following actions:
            - `{payer.note}` = “Could not find Patient in Medicare NGS Payer search - No SSN provided”
            - `{payer.payer_status}` = “Error”
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Could not find Patient MBI in Medicare NGS Payer search - No SSN provided”
                - `{ExceptionNote.type}` = “Client Not Found on Portal”
            - Go back to [Macro 2.8 - Check for Last Payer](https://www.notion.so/Macro-2-8-Check-for-Last-Payer-f4bbad0d532b49ef9c561f1694f67b7d?pvs=21)
        2. N - Go to the next step
5. Search using MBI Lookup
    1. Click the `MBI Lookup` hyperlink
    2. Did a Captcha Solve Pop-Up appear?
        1. Y - Solve the captcha, go to the next step
        2. N - Go to the next step
    3. Fill In `MBI Lookup` Pop-Up
        1. `Patient First Name` = `{patient.first}`
        2. `Patient Last Name` = `{patient.last}`
        3. `Patient SSN` = `{patient.ssn}`    *Note: no dashes in the value, must be numeric characters only*
        4. `Patient Date of Birth` = `{patient.dob}`    *Note: mm/dd/yyyy format*
        5. Click the `Submit` button
    4. Was the Search Successful?
        1. Y - Go to the next step
        2. N - Take the following actions:
            - `{payer.note}` = “Could not find Patient in Medicare NGS Payer search”
            - `{payer.payer_status}` = “Error”
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Could not find Patient MBI in Medicare NGS Payer search.”
                - `{ExceptionNote.type}` = “Client Not Found on Portal”
            - Go back to [Macro 2.8 - Check for Last Payer](https://www.notion.so/Macro-2-8-Check-for-Last-Payer-f4bbad0d532b49ef9c561f1694f67b7d?pvs=21)
    5. Click the `Use this MBI` button
6. Enter Additional Filters
    1. `Select Years of Data` = `1`
    2. `Include DSMT/MNT information?` = `No`
    3. Click the `Search` button
    4. Did benefits results appear?
        1. Y - Skip to the [Set plan variables](https://www.notion.so/Set-plan-variables-f3f85e17f31e40eebda195966ac16bcf?pvs=21) step
        2. N - Go to the next step
    5. Have you retried 3 times?
        1. Y - Take the following actions:
            - `{payer.note}` = “Could not find Patient in Medicare NGS Payer search - Medicare Portal Error”
            - `{payer.payer_status}` = “Error”
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Could not find Patient MBI in Medicare NGS Payer search.”
                - `{ExceptionNote.type}` = “Client Not Found on Portal”
            - Go back to [Macro 2.8 - Check for Last Payer](https://www.notion.so/Macro-2-8-Check-for-Last-Payer-f4bbad0d532b49ef9c561f1694f67b7d?pvs=21)
        2. N - Loop back to the [Enter Additional Filters](https://www.notion.so/Enter-Additional-Filters-6ca719eb464f4ff690bbd4ff5e3cd0dc?pvs=21) and try again
7. Set plan variables
    1. `{plan.status}` = “Eligible”
    2. `{plan.relationship}` = “”
    3. `{plan.subscriber}` = “”
    4. `{plan.begin_date}` = “”
    5. `{plan.end_date}` = “”
    6. `{plan.ded}` = “”
    7. `{plan.ded_remaining}` = “”
    8. `{plan.oop}` = “”
    9. `{plan.oop_remaining}`= “”
    10. `~~{plan.coinsurance}` = “”~~
    11. `~~{plan.copay}` = “”~~
    12. `{plan.coinsurance}` = 0
    13. `{plan.copay}` = 0
8. Check Patient Name
    1. Navigate to the `Beneficiary Information` section
    2. ~~Does `Last Name` = `{patient.last}` **AND** `First Name` = `{patient.first}`?~~
    Does `Last Name` **CONTAIN** `{patient.last}` **AND** `First Name` **CONTAIN** `{patient.first}`?
    *Note: NOT case sensitive*
        1. Y - Go to the next step
        2. N - Flag for Patient Name Mismatch
            - `{name}` = `First Name` + “ “ + `Last Name`
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Patient Name Mismatched: Valant = `{patient.last}`, `{patient.first}` ; `{payer.portal}` = `{name}`"
                - `{ExceptionNote.type}` = “Patient Name Mismatch Warning”
            - Go to the next step
9. Check for Eligibility Dates 
    1. Navigate to the `Beneficiary Information` section
    2. Is `MBI Term Date` = “”
        1. Y - Go to the next step
        2. N - Skip to the [Flag for Ineligible Patient & Date Error](https://www.notion.so/Flag-for-Ineligible-Patient-Date-Error-107f43a78fa4801bbe9ffca70d66314c?pvs=21) 
    3. Navigate to the `Entitlement Information Section`
    4. Is `Part B Entitlement Date` = “”?
        1. Y - Take the following actions:
            - `{payer.note}` = “Could not find Medicare Part B for Patient.”
            - `{payer.payer_status}` = “Error”
            - Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                - `{ExceptionNote.patid}` = `{patient.id}`
                - `{ExceptionNote.note}` = “Could not find Medicare Part B for Patient”
                - `{ExceptionNote.type}` = “Medicare Part B Missing”
            - Go back to [Macro 2.8 - Check for Last Payer](https://www.notion.so/Macro-2-8-Check-for-Last-Payer-f4bbad0d532b49ef9c561f1694f67b7d?pvs=21)
        2. N - Go to the next step
    5. Is `Part B Entitlement Date` < `{run.dos}`?
        1. Y - Go to the next step
        2. N - `{plan.status}` = “Ineligible”
    6. Is `Part B Termination Date` = “”
        1. Y - Go to the next step
        2. N - Skip to the [Flag for Ineligible Patient & Date Error](https://www.notion.so/Flag-for-Ineligible-Patient-Date-Error-107f43a78fa4801bbe9ffca70d66314c?pvs=21) 
10. Go to [Macro 2A.3 - Get Medicare Deductible](https://www.notion.so/Macro-2A-3-Get-Medicare-Deductible-948feb8485af4e67937233908c65ab83?pvs=21) 
11. Flag for Ineligible Patient & Date Error
    1. `{payer.status}` = “Skipped”
    2. Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
        1. `{ExceptionNote.patid}` = `{patient.id}`
        2. `{ExceptionNote.note}` = “Medicare Eligibility Date Error"
        3. `{ExceptionNote.type}` = “Medicare Eligibility Date Error”
    3. Skip to [Macro Y.0 - Check Last Records](https://www.notion.so/Macro-Y-0-Check-Last-Records-be16f9d1326f476f8cac8c7f0b3c73e5?pvs=21) 

### Macro 2A.3 - Get Medicare Deductible

<aside>
📸 **Medicare Advantage Message Screenshot**

- Screenshot toggle
    
    ![image.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/1eec7df9-d484-4330-b2c6-8078b2cdeb0e/f7de2f09-4a99-4304-8886-4cebe4945d69/image.png)
    
</aside>

1. In the left nav bar, navigate to `Part B Deductibles`
2. Navigate to the `Part B Deductibles` table
3. `{plan.ded}` = `Amount - Year 1`
4. `{plan.ded_remaining}` = `Remaining Amount - Year 1`
5. `~~{patient.coinsurance_text}` = "80/20; $257 Ded"~~
6. Is `{plan.ded_remaining}` = 0?
    1. Y - `{plan.coinsurance}` = 20
    2. N - Go to the next step
7. Go to [Macro 2A.4 - Check for Medicare Advantage](https://www.notion.so/Macro-2A-4-Check-for-Medicare-Advantage-107f43a78fa48048b811f469749da15b?pvs=21) 

### Macro 2A.4 - Check for Medicare Advantage

<aside>
📸 **Medicare Advantage Message Screenshot**

- Screenshot toggle
    
    ![Screenshot 2024-05-13 at 3.58.30 PM.png](https://prod-files-secure.s3.us-west-2.amazonaws.com/1eec7df9-d484-4330-b2c6-8078b2cdeb0e/965f991a-6a07-428e-ae1d-f1026f6b9a09/Screenshot_2024-05-13_at_3.58.30_PM.png)
    
</aside>

1. In the left nav bar, does the `Medicare Advantage` selection have a purple 🚫 next to it?
    1. Y - Skip to [Macro 2A.5 - Check for Medicare Secondary Payer](https://www.notion.so/Macro-2A-5-Check-for-Medicare-Secondary-Payer-0d77c4eade3d49c8b85808ac25eb40cf?pvs=21) 
    2. N - Go to the next step
2. Click the `Medicare Advantage` selection
3. Navigate to the `Medicare Advantage` table
4. Sort the table by `Effective Dt` descending
5. Loop over rows for valid Medicare Advantage Plan
    1. For each `row` in the `Medicare Advantage` table:
        1. Is `row.Effective Dt` < `{run.dos}` **AND** (`row.Termination Dt` > `{run.dos}` **OR** `row.Termination Dt` = “”)?
            - Y - Skip to the [Add Medicare Advantage payer
            *Note: Delivery 1 this is an exception, Delivery 2 this becomes adding a new payer*](https://www.notion.so/Add-Medicare-Advantage-payer-Note-Delivery-1-this-is-an-exception-Delivery-2-this-becomes-adding-a-b0292aabd3aa4e8fbd06225e537d1d7b?pvs=21) step
            - N - Go to the next step
        2. Is this the last row in the `Medicare Advantage` table?
            - Y - Skip to [Macro 2A.5 - Check for Medicare Secondary Payer](https://www.notion.so/Macro-2A-5-Check-for-Medicare-Secondary-Payer-0d77c4eade3d49c8b85808ac25eb40cf?pvs=21)
            - N - Loop back to the [Loop over rows for valid Medicare Advantage Plan](https://www.notion.so/Loop-over-rows-for-valid-Medicare-Advantage-Plan-04ae30cb5b9f4ac58fb9df06c9e073bf?pvs=21) step and the next row in the loop
6. Add Medicare Advantage payer
*Note: Delivery 1 this is an exception, Delivery 2 this becomes adding a new payer*
    1. Select the toggle in `row.Plan Name`
    *Note: “A” in [**Medicare Advantage Message Screenshot**](https://www.notion.so/Medicare-Advantage-Message-Screenshot-e1f688654cac4ddcaa273db28786c29d?pvs=21)* 
    2. `{advantage_plan_name}` = `row.Administering Insurance Company`
    *Note: “B” in [**Medicare Advantage Message Screenshot**](https://www.notion.so/Medicare-Advantage-Message-Screenshot-e1f688654cac4ddcaa273db28786c29d?pvs=21)* 
    3. `{advantage_plan_portal}` = the hyperlinked website in `row.Plan Name`
    *Note: “C” in [**Medicare Advantage Message Screenshot**](https://www.notion.so/Medicare-Advantage-Message-Screenshot-e1f688654cac4ddcaa273db28786c29d?pvs=21)* 
    4. Append “Identified valid Medicare Advantage Plan: `{advantage_plan_name}` at `{advantage_plan_portal}`" to `{payer.note}` on a new line
    5. `{payer.payer_status}` = “Eligible”
    6. Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
        - `{ExceptionNote.patid}` = `{patient.id}`
        - `{ExceptionNote.note}` = “Identified valid Medicare Advantage Plan: `{advantage_plan_name}` at `{advantage_plan_portal}`”
        - `{ExceptionNote.type}` = “Medicare Advantage Found”
7. Go to [Macro 2A.5 - Check for Medicare Secondary Payer](https://www.notion.so/Macro-2A-5-Check-for-Medicare-Secondary-Payer-0d77c4eade3d49c8b85808ac25eb40cf?pvs=21) 

### Macro 2A.5 - Check for Medicare Secondary Payer

1. Check Medicare Secondary Payer
    1. In the left nav bar, does the `Medicare Secondary Payer` selection have a purple 🚫 next to it?
        1. Y - Skip to [Macro 2A.6 - Check for Crossover](https://www.notion.so/Macro-2A-6-Check-for-Crossover-fd7597252fcb4dc2913d8e20b9d83862?pvs=21) 
        2. N - Go to the next step
2. Click the `Medicare Secondary Payer` selection
3. Navigate to the `Medicare Secondary Payer` table
4. Sort the table by `Effective Dt` descending
5. Loop over rows for valid Medicare Secondary Plan
    1. For each `row` in the `Medicare Secondary Payer` table:
        1. Is `row.Effective Dt` < `{run.dos}` **AND** (`row.Termination Dt` > `{run.dos}` **OR** `row.Termination Dt` = “”)?
            - Y - Go to the next step
            - N - Skip to the [Check for last row in table](https://www.notion.so/Check-for-last-row-in-table-53f4b134d40f438bb1e8bf7f45323e0f?pvs=21) step
        2. Does `row.Type` contain “workmen’s comp” **OR** does `row.Type` contain “auto policy”?    *Note: case insensitive*
            - Y - Go to the next step
            - N - Skip to the [Check for last row in table](https://www.notion.so/Check-for-last-row-in-table-53f4b134d40f438bb1e8bf7f45323e0f?pvs=21) step
    2. Check for last row in table
        1. Is this the last row in the `Medicare Secondary Payer` table?
            - Y - Skip to [Macro 2A.6 - Check for Crossover](https://www.notion.so/Macro-2A-6-Check-for-Crossover-fd7597252fcb4dc2913d8e20b9d83862?pvs=21)
            - N - Loop back to the [Loop over rows for valid Medicare Secondary Plan](https://www.notion.so/Loop-over-rows-for-valid-Medicare-Secondary-Plan-6d7d1add58ca4c2d8319b96aaf9f741a?pvs=21) step and the next row in the loop
6. Add Medicare Secondary payer
*Note: Delivery 1 this is an exception, Delivery 2 this becomes adding a new payer*
    1. `{secondary_plan_name}` = `row.Insurance Name`     *Note: Value before expanding the dropdown*
    2. `{secondary_indicator}` = `row.Indicator`
    3. `{secondary_policy_number}` = `row.Policy Number`
    4. `{secondary_group_number}` = `row.Group Number`
    5. Append “Identified valid Medicare Secondary Plan: `{secondary_plan_name}` - `{secondary_indicator}` with Policy ID: `{secondary_policy_number}` and Group Number: `{secondary_group_number}`" to `{payer.note}` on a new line
    6. `{payer.payer_status}` = “Eligible”
    7. Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
        - `{ExceptionNote.patid}` = `{patient.id}`
        - `{ExceptionNote.note}` = “Identified valid Medicare Secondary Plan: `{secondary_plan_name}` - `{secondary_indicator}` with Policy ID: `{secondary_policy_number}` and Group Number: `{secondary_group_number}`”
        - `{ExceptionNote.type}` = “Medicare Secondary Found”
7. Go to [Macro 2A.6 - Check for Crossover](https://www.notion.so/Macro-2A-6-Check-for-Crossover-fd7597252fcb4dc2913d8e20b9d83862?pvs=21) 

### Macro 2A.6 - Check for Crossover

*Note: `SANJOA82` in NEHS*

1. In the left nav bar, does the `Crossover` selection have a purple 🚫 next to it?
    1. Y - Skip to [Macro 2A.7 - Search for QMB](https://www.notion.so/Macro-2A-7-Search-for-QMB-5d9c1137c5084e31997f94ce68b2cc4d?pvs=21) 
    2. N - Go to the next step
2. Click the `Crossover` selection
3. Navigate to the `Crossover` table
4. Sort the table by `Insurer Effective Dt` descending
5. Loop over rows for valid crossover insurance
    1. For each `row` in the `Crossover` table:
        1. Is `row.Insurer Effective Dt` < `{run.dos}` **AND** (`row.Insurer Term Dt` > `{run.dos}` **OR** `row.Insurer Term Dt` = “”)?
            - Y - Skip to the [Add crossover payer
            *Note: Delivery 1 this is an exception, Delivery 2 this becomes adding a new payer*](https://www.notion.so/Add-crossover-payer-Note-Delivery-1-this-is-an-exception-Delivery-2-this-becomes-adding-a-new-paye-b5a29d10f6f4449ebbf379611bde0186?pvs=21) step
            - N - Go to the next step
        2. Is this the last `row` in the `Crossover` table?
            - Y - Skip to [Macro 2A.7 - Search for QMB](https://www.notion.so/Macro-2A-7-Search-for-QMB-5d9c1137c5084e31997f94ce68b2cc4d?pvs=21)
            - N - Loop back to the [Loop over rows for valid crossover insurance](https://www.notion.so/Loop-over-rows-for-valid-crossover-insurance-2c71dabdab1f4355b24ce182800a6121?pvs=21) step and the next `row` in the loop
6. Add crossover payer
*Note: Delivery 1 this is an exception, Delivery 2 this becomes adding a new payer*
    1. `{crossover_plan_name}` = `row.Insurer Name`     *Note: Value before expanding the dropdown*
    2. `{crossover_insurance_code}` = `row.Insurance Code`
    3. Append “Identified valid Crossover Payer: `{crossover_plan_name}` - `{crossover_insurance_code}`" to `{payer.note}` on a new line
    4. `{payer.payer_status}` = “Eligible”
    5. Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
        - `{ExceptionNote.patid}` = `{patient.id}`
        - `{ExceptionNote.note}` = “Identified valid Crossover Payer: `{crossover_plan_name}` - `{crossover_insurance_code}`”
        - `{ExceptionNote.type}` = “Medicare Crossover Found”
7. Go to [Macro 2A.7 - Search for QMB](https://www.notion.so/Macro-2A-7-Search-for-QMB-5d9c1137c5084e31997f94ce68b2cc4d?pvs=21)
- Previous Add Crossover Payer Logic
    1. For the matched `row` in the `Crossover` table, is `row.Insurance Code` = “Medicaid” **AND** `row.Insurer Name` = “MASSACHUSETTS HEALTH”?
        1. Y - Go to the next step
        2. N - Skip to the [Add Other Payer](https://www.notion.so/Add-Other-Payer-026de12e8970470e93ed5f2db23f6f82?pvs=21) step
    2. Add Medicaid Mass Payer
        1. Run the [Add Patient Payer Function](https://www.notion.so/Add-Patient-Payer-Function-0eccc91bc36a48c2ae9ed688921a1bfc?pvs=21) 
            - Inputs:
                - `fn_market_id` = `{market.id}`
                - `fn_payer_name` =   “MEDICAID MASS 4000”
                - `fn_policy_id` = “”
                - `fn_group_id` = “”
                - `fn_payer_order` = 2
            - Output:
                - `Result` = `{new_payer}`
        2. Append `{new_payer}` to `{patient.payers}`
        3. Skip to [Macro 2A.7 - Search for QMB](https://www.notion.so/Macro-2A-7-Search-for-QMB-5d9c1137c5084e31997f94ce68b2cc4d?pvs=21) 
    3. Add Other Payer
        1. Run the [Add Patient Payer Function](https://www.notion.so/Add-Patient-Payer-Function-0eccc91bc36a48c2ae9ed688921a1bfc?pvs=21) 
            - Inputs:
                - `fn_market_id` = `{market.id}`
                - `fn_payer_name` =   `Insurer Name`
                - `fn_policy_id` = “”
                - `fn_group_id` = “”
                - `fn_payer_order` = 2
            - Output:
                - `Result` = `{new_payer}`
        2. Append `{new_payer}` to `{patient.payers}`

### Macro 2A.7 - Search for QMB

1. Create a temporary variable `{has_qmb_notification}` = “N”
2. For each `{notification}` in `{patient.notifications}`
    1. Does `{notification}` = “Medicare QMB”?
        - Y - `{has_qmb_notification}` = “Y”, exit to the loop and go to the next step
        - N - Go to the next `{notification}` in the loop
3. In the left nav bar, does the `Qualified Medicare Beneficiary` selection have a purple 🚫 next to it?
    1. Y - Go to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21) 
    2. N - Go to the next step
4. Click the `Qualified Medicre Beneficiary` selection
5. Navigate to the `Qualified Medicare Beneficiary` table
6. Is there any row where `Effective Dt` < `{run.dos}` **AND** (`Termination Dt` > `{run.dos}` **OR** `Termination Dt` = “”)?
    - Y - Check for QMB notification
        1. Is `{has_qmb_notification}` = “Y”?
            - Y - Go to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21)
            - N - Go to [Flag patient for Medicare QMB](https://www.notion.so/Flag-patient-for-Medicare-QMB-26626d88a87946e391e964a95a879c4e?pvs=21)
    - N - Check for QMB notification
        1. Is `{has_qmb_notification}` = “Y”?
            - Y - Take the following actions
                1. Add an `{ExceptionNote}` to `{run.ExceptionNotes}`
                    - `{ExceptionNote.patid}` = `{patient.id}`
                    - `{ExceptionNote.note}` = “Patient has Medicare QMB in Patient Notifications, but Medicare QMB status was not found in Medicare NGS”
                    - `{ExceptionNote.type}` = “Medicare QMB Not Found”
                2. Go to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21) 
            - N - Go to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21)
7. Flag patient for Medicare QMB
    1. Run the [Add Patient Notification Function](https://www.notion.so/Add-Patient-Notification-Function-60d00008938245a0803508dbcdf0f8d7?pvs=21) 
        1. `fn_notification_key` = “Medicare QMB”
    2. `{patient.patient_type}` = “Do Not Bill”
8. Go to [Macro 2A.8 - Check for Last Records](https://www.notion.so/Macro-2A-8-Check-for-Last-Records-8a96aa2c6306480687b30e8324234863?pvs=21) 

### Macro 2A.8 - Check for Last Records

1. Is this the last `{payer}` in `{patient.payers}`?
    1. Y - Go to the next step
    2. N - Loop back to [Loop over payers:](https://www.notion.so/Loop-over-payers-45ae79d7c1f84668ab65bf94d05cb2f1?pvs=21) and the next `{payer}` in the loop
2. Is this the last `{patient}` in `{run.patients}`?
    1. Y - Go to the next step
    2. N - Loop back to [Loop over patients:](https://www.notion.so/Loop-over-patients-c7e2ee7e0496444e8d4f0cd01cb1ae83?pvs=21) and the next `{patient}` in the loop
3. Go to [Macro 3.0 - Process the Verification Queue](https://www.notion.so/Macro-3-0-Process-the-Verification-Queue-9046c5c4e3fa47cdb8273899e28d8b8c?pvs=21)