"""
Fraud Scenarios:
TODO 1. Account Takeover Fraud (ATO)
Common Findings:
    Sudden high-value withdrawals
    Login from new_device (simulated via "unusual transaction patter")
    Multiple withdrawals in small time window
TODO 2. Money Mule/ Money laundering
Common Findings:
    Large inbound transfer from unknown source
    Immediate outbound transfer to another account
    Often cross institution (A->B->C)
TODO 3. Structuring
Common Findings:
    Many Small deposits just below CTR thresholds of $10,000.01(Exp. $9800, $9900, $9999)
TODO 4. Synthetic Identity Theft
Common Findings:
    New Customer -> immediate multiple accounts -> immediate large transactions
TODO 5. Rapid-Fire Fraud (Velocity Fraud)
Common Findings:
    10+ withdrawals in a short time window
TODO 6. Stolen Card/ Unauthorized Card Use
Common Finding:
    Unusual merchant types
    Odd hours (Exp. 2AM to 5AN)
TODO 7. Fraud Rings
Common Findings:
    Multiple accounts transferring in loops

"""