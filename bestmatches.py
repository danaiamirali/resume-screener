import requests

def Match():

    api_key = "c7c24d4a2e29cda5e041c25566488f571a48c02e5a9c8e5c5ed75748de4f8350"

    url = "https://www.themuse.com/api/public/jobs"

    

    params = {"api_key": api_key, "level": "Internship", "page": 1}

    response = requests.get(url, params=params)

    if response.status_code == 200:
        # Parse the JSON data from the response
        try:
            data = response.json()

            # Now 'data' contains the information returned by the API
            # You can process and use this data as needed
            for job in data.get('results', []):
                print(f"Job Title: {job.get('name')}")
                print(f"Company: {job.get('company', {}).get('name')}")
                print(f"Location: {job.get('locations', [])[0].get('name')}")
                print("-----")

        except ValueError as e:
            print(f"Error parsing JSON: {e}")



