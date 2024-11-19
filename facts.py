import requests

def get_random_fact():
    api_url = "https://api.api-ninjas.com/v1/facts"
    headers = {
        "X-Api-Key": "O8WSPd/oN3TDARLbASakUQ==ze6CfymldxzB65lH"  # Replace with your API key
    }
    
    response = requests.get(api_url, headers=headers)
    if response.status_code == 200:
        fact_data = response.json()
        return fact_data[0].get("fact", "No fact found!") if fact_data else "No fact found!"
    else:
        return "Failed to fetch a fact."

