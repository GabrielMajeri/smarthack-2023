import requests


def match_call(url, headers, data):
    return requests.post(url, headers=headers, json=data).json()


def company_to_be_enriched_call(input):
    company_details = {
        "commercial_names": [input],
        "address_txt": "Romania"
    }
    return company_details


def gather_data(company):
    response = {
        "employee_count": company["employee_count"],
        "estimated_revenue": company["estimated_revenue"],
        "naics": company["naics_2022"]["primary"]["label"]
    }
    return response
