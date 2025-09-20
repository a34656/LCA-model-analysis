from rag import search_process
from flows import get_flows_for_process
from datap import load_datasets
from lcia import calculate_lcia

if __name__ == "__main__":
    exchanges, traci = load_datasets("detailed_exchanges_harmonized.csv", "traci_2_2.xlsx")
    user_input = input("Enter process: ")
    match = search_process(user_input)
    print(f"✅ Selected process: {match['process_name']} ({match['similarity']}%)")

    flows = get_flows_for_process(match['process_name'], exchanges)

    if not flows.empty:
        print("📊 Flows linked to this process:\n")
        print(flows.to_string(index=False))
    else:
        print("⚠️ No flows found for this process.")

    results = calculate_lcia(flows, traci)
    print(f"LCIA results:- {results}")