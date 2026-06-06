import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def generate_sample_data(n=500):
    """Generates a synthetic dataset of banking transactions."""
    locations = [
        'New York', 'London', 'Tokyo', 'Cayman Islands', 'Panama', 
        'Zurich', 'Dubai', 'Singapore', 'Turkey', 'UAE', 'Egypt', 
        'Switzerland'
    ]
    tx_types = ['Wire Transfer', 'ACH', 'ATM Withdrawal', 'Internal Transfer', 'Crypto Gateway']
    
    # Fixed pool of accounts to simulate repeated interactions
    senders = [f"ACC-{random.randint(1000, 1080)}" for _ in range(29)] # Reduced by 1 to make space
    senders.append("ACC-USER-001") # Explicitly add a user-defined sender ID
    receivers = [f"ACC-{random.randint(5000, 5080)}" for _ in range(29)] # Reduced by 1 to make space
    receivers.append("ACC-USER-002") # Explicitly add a user-defined receiver ID
    
    data = []
    base_time = datetime.now()

    for i in range(n):
        # Randomly decide if this transaction should be part of a "Money Laundering" simulation
        is_suspicious_location = random.random() < 0.15
        loc = random.choice(['Cayman Islands', 'Panama']) if is_suspicious_location else random.choice(locations)
        
        amount = round(random.uniform(50.0, 25000.0), 2)
        
        # Occasionally create very specific amounts (e.g., just under $10k to simulate 'structuring')
        if random.random() < 0.05:
            amount = round(random.uniform(9800.0, 9999.0), 2)

        data.append({
            'transaction_id': f"TXN-{10000 + i}",
            'timestamp': base_time - timedelta(minutes=random.randint(1, 10000)),
            'sender_id': random.choice(senders),
            'receiver_id': random.choice(receivers),
            'amount': amount,
            'location': loc,
            'type': random.choice(tx_types),
            'status': 'Completed'
        })
    
    df = pd.DataFrame(data)
    
    # Simulate "Velocity Fraud" - Force a few accounts to have many transactions in a short time
    velocity_sender = "ACC-1010"
    for i in range(5):
        extra_row = df.iloc[0].copy()
        extra_row['sender_id'] = velocity_sender
        extra_row['timestamp'] = base_time - timedelta(minutes=i*2)
        df = pd.concat([df, pd.DataFrame([extra_row])], ignore_index=True)

    return df.sort_values(by='timestamp', ascending=False)
