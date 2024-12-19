#!/usr/bin/env python3
# stations.md-create.py

import requests
import json
import sys
import os

def main():
    output_file = "stations.md"

    print(f"Creating {output_file} by requesting list at https://www.padersprinter.de/internetservice/geoserviceDispatcher/services/stopinfo/stops")

    # Define the URL and payload
    url = "https://www.padersprinter.de/internetservice/geoserviceDispatcher/services/stopinfo/stops"
    payload = {
        "left": -648000000,
        "bottom": -324000000,
        "right": 648000000,
        "top": 324000000
    }

    # Make the POST request
    try:
        response = requests.post(url, data=payload)
        response.raise_for_status()
        response_json = response.text
    except requests.RequestException as e:
        print("Error occurred while making the request:", e)
        exit(1)

    # Debugging: Inspect the response content if JSON decoding fails
    try:
        data = json.loads(response_json)
        stops = data.get("stops", [])
    except json.JSONDecodeError as e:
        print("Error decoding JSON response:", e)
        print("Response content:", response_json)  # Print raw response for debugging
        exit(1)

    # Generate the Markdown table
    markdown_lines = ["| stop name                                | id   | category |", "|------------------------------------------|------|----------|"]

    # Sort the stops alphabetically by 'name'
    stops_sorted = sorted(stops, key=lambda stop: stop.get("name", ""))
    print(f"Total {len(stops_sorted)} Padersprinter stops.")

    for stop in stops_sorted:
        name = stop.get("name", "")
        short_name = stop.get("shortName", "")
        category = stop.get("category", "")
        markdown_lines.append(f"| {name:<40} | {short_name} | {category:<8} |")

    # Join the lines into a single Markdown string
    markdown_content = "\n".join(markdown_lines)

    # Write the Markdown content to a file
    try:
        with open(output_file, "w") as file:
            file.write(markdown_content)
        print(f"Bus stations table has been successfully written to {output_file}.")
    except IOError as e:
        print("Error writing to file:", e)

if __name__ == "__main__":
    main()
