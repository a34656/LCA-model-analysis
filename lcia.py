# lcia.py
import pandas as pd
from mapper import map_flow_to_substances, substance_cache

def calculate_lcia(flows, traci, model=None):
    """
    Match flows with TRACI characterization factors and calculate LCIA impacts.
    """

    results = []

    for _, row in flows.iterrows():
        flow_name = row["input_name_norm"]
        amount = row["amount"]
        unit = row["unit"]

        # Map to TRACI substances (Gemini + fuzzy matching)
        substances = map_flow_to_substances(flow_name, traci.index, model, substance_cache)

        if not substances:
            print(f"⚠️ No mapping for flow '{flow_name}'")
            continue

        for sub in substances:
            if sub in traci.index:
                factors = traci.loc[sub]
                impacts = factors * amount
                results.append(impacts)
            else:
                print(f"⚠️ '{sub}' not found in TRACI index")

    if results:
        lcia = pd.DataFrame(results)
        lcia_sum = lcia.sum().reset_index()
        lcia_sum.columns = ["impact_category", "impact_value"]
        return lcia_sum
    else:
        print("⚠️ No TRACI matches found for the flows")
        return pd.DataFrame()
