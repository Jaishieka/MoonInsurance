import requests
import json
from collections import defaultdict

def fetch_data():
    try:
        agents = requests.get("http://agent-service/agents", timeout=5).json()
        sales = requests.get("http://integration-service/sales", timeout=5).json()
        return agents, sales
    except Exception as e:
        print(f"Error fetching data: {e}")
        return {}, []

def analyze_sales(agents, sales):
    team_performance = defaultdict(int)
    product_targets = defaultdict(int)
    branch_sales = defaultdict(int)

    for sale in sales:
        agent_code = sale.get("agent_code")
        product = sale.get("product")
        branch = sale.get("branch")
        amount = sale.get("amount", 0)

        agent = agents.get(agent_code, {})
        team = agent.get("team", "Unknown")

        team_performance[team] += amount
        product_targets[product] += amount
        branch_sales[branch] += amount

    return {
        "best_teams": sorted(team_performance.items(), key=lambda x: x[1], reverse=True),
        "top_products": sorted(product_targets.items(), key=lambda x: x[1], reverse=True),
        "branch_performance": sorted(branch_sales.items(), key=lambda x: x[1], reverse=True)
    }

def main():
    agents, sales = fetch_data()
    if not sales:
        print("No sales data found.")
        return

    insights = analyze_sales(agents, sales)

    print(" Aggregated Sales Insights:")
    print(json.dumps(insights, indent=2))

if __name__ == "__main__":
    main()
