import pandas as pd
def load_datasets(exchanges_path, traci_path):
    exchanges = pd.read_csv(exchanges_path)
    exchanges.columns = exchanges.columns.str.strip().str.lower()
    # keep core columns, coerce amount to numeric
    exchanges['amount'] = pd.to_numeric(exchanges['amount_harmonized'].fillna(exchanges.get('amount', 0)),
    errors='coerce').fillna(0.0)
    exchanges['input_name_norm'] = exchanges['input_name'].astype(str).str.lower().str.strip()

    traci = pd.read_excel(traci_path, sheet_name='Substances')
    traci.columns = [str(c).strip().lower() for c in traci.columns]
    traci['substance_norm'] = traci['substance name'].astype(str).str.lower().str.strip()

    for col in traci.columns:
        traci[col] = traci[col].astype(str)

    traci = traci.set_index('substance_norm')

    exchanges.to_parquet('exchanges_clean.parquet', index=False)
    traci.to_parquet('traci_clean.parquet')

    exchanges.to_parquet('exchanges_clean.parquet', index=False)
    traci.to_parquet('traci_clean.parquet')
    return exchanges, traci
