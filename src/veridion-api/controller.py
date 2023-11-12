import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from company_search import *
from company_enrich import *
from googletrans import Translator
import logging
from dotenv import load_dotenv
from copy import deepcopy

search_url = "https://data.veridion.com/search/v2/companies?page_size=200"
match_url = "https://data.veridion.com/match/v4/companies"
process_input_url = "http://172.16.23.239:30500/"

load_dotenv()

search_headers = {"Content-Type": "application/json",
                  "x-api-key": os.environ.get("SEARCH-API-KEY")}
match_headers = {"Content-Type": "application/json",
                 "x-api-key": os.environ.get("MATCH-API-KEY")}

app = FastAPI()

origins = [
    "http://172.16.23.239/",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger = logging.getLogger('smarthack-api')

userRequestBody = {
    "filters": {
        "and": [
            {
                "attribute": "company_location",
                "relation": "equals",
                "value":
                    {
                        "country": "Romania"
                    },
                "strictness": 1
            }
        ]
    }
}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/retrieve-companies")
def retrieve_companies(client_input):
    logger.info("Processing input to retrieve companies")
    curated_semantic_list = curated_json_to_list(semantic_processing_call(os.environ.get("PROCESSING_DOMAIN"), client_input))
    synonym_list = curated_json_to_list(word_synonym_call(os.environ.get("PROCESSING_DOMAIN"), curated_semantic_list[0], 2))
    full_word_list = translate_words(curated_semantic_list + synonym_list)
    company_search_body = deepcopy(userRequestBody)
    company_search_body['filters']['and'].append(build_company_products(full_word_list))
    # company_search_body['filters']['and'].append(build_company_keywords(full_word_list))
    logger.info("Calling Veridion Search API")
    return search_call(search_url, company_search_body, search_headers)


@app.get("/retrieve-enriched-company")
def retrieve_enriched_company(company_input_details):
    logger.info("Processing input to retrieve enriched company")
    formatted_company_details = company_to_be_enriched_call(company_input_details)
    logger.info("Calling Veridion Match API")
    return gather_data(match_call(match_url, match_headers, formatted_company_details))


def curated_json_to_list(input):
    list = []
    for value in input.get("items"):
        list.append(value)
    logger.info("Translated word list")
    return list


def build_company_products(wordlist):
    field = {
        "attribute": "company_products",
        "relation": "match_expression",
        "value": {
            "match": {
                "operator": "OR",
                "operands": wordlist
            }
        }
    }
    return field


def build_company_keywords(wordlist):
    field = {
        "attribute": "company_keywords",
        "relation": "match_expression",
        "value": {
            "match": {
                "operator": "OR",
                "operands": wordlist
            }
        }
    }
    return field


def translate_words(word_list):
    translator = Translator()
    list = []

    for word in word_list:
        translation = translator.translate(word, src="de", dest="ro")
        list.append(translation.text)

    print(list)
    return list


def test():
    retrieve_companies("Hello world")

# test()
