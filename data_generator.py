import random
import pandas as pd
from config import *

random.seed(RANDOM_SEED)

PRICE_RANGES = {
    "Smartphone": (100, 1500),
    "Laptop": (300, 3000),
    "Tablet": (100, 1200),
    "TV": (200, 2500),
    "Refrigerator": (400, 2500),
    "Washing Machine": (300, 1800),
    "Camera": (200, 2500),
    "Headphones": (30, 500)
}

def make_record(status):
    category = random.choice(PRODUCT_CATEGORIES)
    warranty = random.choice(WARRANTY_OPTIONS)

    if status == "Valid":
        age = random.randint(1, warranty)
        receipt = 1
        serial = 1
        damage = random.choice([
            "Manufacturing Defect", "Battery Failure",
            "Electrical Failure", "Software Failure"
        ])
        repairs = random.randint(0, 2)

    elif status == "Invalid":
        age = random.randint(warranty + 1, 60)
        receipt = random.choice([0, 0, 1])
        serial = random.choice([0, 0, 1])
        damage = random.choice([
            "Water Damage", "Physical Damage", "Unknown"
        ])
        repairs = random.randint(1, 4)

    else:
        age = random.randint(1, 60)
        receipt = random.randint(0, 1)
        serial = random.randint(0, 1)
        damage = random.choice(DAMAGE_TYPES)
        repairs = random.randint(0, 4)

    low, high = PRICE_RANGES[category]
    purchase_price = random.randint(low, high)

    claim_ratio = random.uniform(0.10, 0.90)
    if status == "Manual Review" and random.random() < 0.35:
        claim_ratio = random.uniform(0.90, 1.10)

    claim_amount = round(purchase_price * claim_ratio, 2)
    days_since_purchase = max(0, age * 30 + random.randint(-10, 10))

    return {
        "product_category": category,
        "product_age_months": age,
        "warranty_period_months": warranty,
        "receipt_available": receipt,
        "serial_number_valid": serial,
        "damage_type": damage,
        "repair_history": repairs,
        "purchase_price": purchase_price,
        "claim_amount": claim_amount,
        "days_since_purchase": days_since_purchase,
        "claim_status": status
    }

def generate_dataset():
    rows = []
    for status in ["Valid", "Invalid", "Manual Review"]:
        for _ in range(TARGET_PER_CLASS):
            rows.append(make_record(status))

    random.shuffle(rows)
    df = pd.DataFrame(rows)
    df.insert(0, "claim_id", range(1, len(df) + 1))
    return df

if __name__ == "__main__":
    df = generate_dataset()
    output = "data/raw/assurex_raw.csv"
    df.to_csv(output, index=False)
    print("Created:", output)
    print(df["claim_status"].value_counts())
