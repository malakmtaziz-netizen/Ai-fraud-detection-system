import pandas as pd

class FraudEngine: 
    def __init__(self):
        self.large_transfer_limit = 10000 
        self.high_risk_locations = ['Cayman Islands', 'Panama', 'Turkey', 'Egypt']

    def run_audit(self, df):
        df = df.copy()
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['risk_score'] = 0
        df['risk_reasons'] = ""

        # 1. Large Transfer
        large_mask = df['amount'] >= self.large_transfer_limit
        df.loc[large_mask, 'risk_score'] += 35
        df.loc[large_mask, 'risk_reasons'] += "High Volume Transfer; "

        # 2. High-Risk Location
        loc_mask = df['location'].isin(self.high_risk_locations)
        df.loc[loc_mask, 'risk_score'] += 40
        df.loc[loc_mask, 'risk_reasons'] += "Offshore Jurisdiction; "

        # 3. Structuring
        structuring_mask = (df['amount'] >= 9000) & (df['amount'] < 10000)
        df.loc[structuring_mask, 'risk_score'] += 25
        df.loc[structuring_mask, 'risk_reasons'] += "Potential Structuring Pattern; "

        # 4. Velocity Check: more than 3 transactions in 1 hour
        # Sort by sender and timestamp to ensure rolling count aligns with the dataframe
        df = df.sort_values(['sender_id', 'timestamp'])
        df['txn_count_1h'] = df.groupby('sender_id').rolling('1h', on='timestamp')['transaction_id'].count().values

        velocity_mask = df['txn_count_1h'] > 3
        df.loc[velocity_mask, 'risk_score'] += 40
        df.loc[velocity_mask, 'risk_reasons'] += "High Velocity Activity; "

        # Final Risk Score
        df['risk_score'] = df['risk_score'].clip(0, 100)

        def categorize_risk(score):
            if score >= 70:
                return "CRITICAL"
            elif score >= 40:
                return "ELEVATED"
            else:
                return "STABLE"

        df['risk_level'] = df['risk_score'].apply(categorize_risk)

        df.loc[df['risk_reasons'] == "", 'risk_reasons'] = "Routine Transaction"

        return df.sort_values(by='risk_score', ascending=False)
