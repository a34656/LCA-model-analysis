import pandas as pd

def get_flows_for_process(process_name, exchanges):
    flows = exchanges[exchanges['process_name'].str.lower() == process_name.lower()]
    
    if flows.empty:
        print(f"⚠️ No flows found for process '{process_name}'")
        return pd.DataFrame()
    
    return flows[['process_name', 'input_name_norm', 'amount', 'unit']].reset_index(drop=True)
