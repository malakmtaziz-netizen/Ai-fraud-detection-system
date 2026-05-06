import pandas as pd

class FraudEngine:
    def __init__(self):
        self.large_transfer_limit = 10000
        self.high_risk_locations = ['Cayman Islands', 'Panama']

    def run_audit(self, df):
        """
        Analyzes transactions and assigns risk scores.
        0-30: Low Risk | 31-70: Medium Risk | 71-100: High Risk
        """
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['risk_score'] = 0
        df['risk_reasons'] = ""

        # 1. Rule: Large Transfer Detection
        large_mask = df['amount'] >= self.large_transfer_limit
        df.loc[large_mask, 'risk_score'] += 35
        df.loc[large_mask, 'risk_reasons'] += "High Volume Transfer; "

        # 2. Rule: High-Risk Jurisdictions
        loc_mask = df['location'].isin(self.high_risk_locations)
        df.loc[loc_mask, 'risk_score'] += 30
        df.loc[loc_mask, 'risk_reasons'] += "Offshore Jurisdiction; "

        # 3. Rule: Structuring Detection (Transactions just under reporting limits)
        structuring_mask = (df['amount'] >= 9000) & (df['amount'] < 10000)
        df.loc[structuring_mask, 'risk_score'] += 25
        df.loc[structuring_mask, 'risk_reasons'] += "Potential Structuring Pattern; "

        # 4. Rule: Velocity Check (Frequency of transfers from same account)
        # Check for accounts doing more than 3 transactions in 1 hour
        df = df.sort_values(['sender_id', 'timestamp'])
        df['txn_count_1h'] = df.groupby('sender_id')['timestamp'].transform(
            lambda x: x.rolling('1H', on=x).count()
        )
        velocity_mask = df['txn_count_1h'] > 3
        df.loc[velocity_mask, 'risk_score'] += 40
        df.loc[velocity_mask, 'risk_reasons'] += "High Velocity Activity; "

        # Final Normalization and Categorization
        df['risk_score'] = df['risk_score'].clip(0, 100)
        
        def categorize_risk(score):
            if score >= 70: return "CRITICAL"
            if score >= 40: return "ELEVATED"
            return "STABLE"
        
        df['risk_level'] = df['risk_score'].apply(categorize_risk)
        
        # Clean up empty reasons
        df.loc[df['risk_reasons'] == "", 'risk_reasons'] = "Routine Transaction"
        
        return df.sort_values(by='risk_score', ascending=False)