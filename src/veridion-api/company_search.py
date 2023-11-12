import requests

def search_call(url, data, headers):
    print(data)
    next_page = requests.post(url, headers=headers, json=data)
    return gather_data(next_page.json())

def semantic_processing_call(url, input):
    return requests.post(url + "extract-product", headers={"Content-Type": "application/json"},
                         params={"prompt": input}).json()


def word_synonym_call(url, word, number_of_synonyms):
    return requests.post(url + "synonym", headers={"Content-Type": "application/json"},
                         params={"prompt": word, "n": number_of_synonyms}).json()

def gather_data(page):
    company_list = []
    for company in page["result"]:
        response = {
            "company_name": company["company_name"],
            "company_description": company["short_description"],
            "main_region": company["main_region"],
            "main_city": company["main_city"],
            "website_url": company["website_url"],
            "primary_phone": company["primary_phone"],
            "primary_email": company["primary_email"],
        }
        company_list.append(response)
        if len(company_list) == 10:
            return company_list
    return company_list
