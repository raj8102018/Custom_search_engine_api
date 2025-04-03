"""
This script defines a workflow that performs a Google search for a given query and then sorts the search results.
"""
import os
import re
import json
import httpx
from langchain.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser

API_KEY = os.getenv("api_key")
SEARCH_ENGINE_ID = os.getenv("search_engine_id")

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


def parse_search_results(response):
    """
    function to parse search results from Google Custom Search API response
    """
    articles = []

    for item in response.get("items", []):
        title = item.get("title", "")
        snippet = item.get("snippet", "")
        link = item.get("link", "")
        published_date = None

        # Try to extract published date from metatags if available
        metatags = item.get("pagemap", {}).get("metatags", [])
        if metatags:
            meta = metatags[0]
            published_date = (
                meta.get("article:published_time")
                or meta.get("article:modified_time")
                or meta.get("datePublished")
                or meta.get("dateCreated")
            )

        if not published_date:

            match = re.search(r"([A-Z][a-z]{2,8} \d{1,2}, \d{4})", snippet)
            if match:
                published_date = match.group(1)

        articles.append(
            {
                "title": title,
                "snippet": snippet,
                "link": link,
                "published_date": published_date,
            }
        )

    return articles


def clean_and_parse_json(json_string):
    """
    function for cleaning and parsing json string with delimiters
    """
    try:
        cleaned = re.sub(r"```json|```", "", json_string).strip()
        return json.loads(cleaned)
    except ValueError:
        return None


def google_search(api_key, search_engine_id, query_location, **params):
    """
    function to perform a Google search using the Custom Search API
    """
    base_url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": api_key,
        "cx": search_engine_id,
        "q": f"groundwater levels in {query_location}",
        **params,
    }
    response = httpx.get(base_url, params=params)
    response.raise_for_status()
    return response.json()


llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", google_api_key=GEMINI_API_KEY, temperature=0
)

sorting_prompt = PromptTemplate(
    input_variables=["response_data"],
    template="""
You are provided with a list of response data entries:

{response_data}

Please filter and sort these entries according to the following criteria:

1. **Relevance**: Include only entries that are clearly related to the following topics:
   - Groundwater
   - Water crisis
   - Water pollution
   - Drinking water
   - Water supply
   - Water management
   - Water sustainability
   - Water conservation
   - Water quality
   - Water resources
   - Water scarcity
   - Water infrastructure
   - Hydrology
   - Aquifers
   - Water treatment
   - Water reuse
   - Water efficiency
   - Water governance
   - Watershed management
   - Integrated water resources management (IWRM)

2. **Exclusion**: Exclude any entries that are related to advertisements, promotions, or sponsored content.

3. **Prioritization**:
   - Entries specifically discussing "groundwater levels" should appear at the top.
   - Within each topic group:
     - Entries with a publication date should be sorted in descending order (most recent first).
     - Entries without a publication date should be placed at the bottom of their respective groups.

**Note**: The publication date for each entry is provided explicitly as a key in the data.

Return the result strictly as a valid JSON array, with no additional text or explanations.
""",
)

chain = sorting_prompt | llm | StrOutputParser()


def sort_groundwater_entries(response_json):
    """
    function to sort groundwater entries based on relevance and publication date
    """
    response_str = json.dumps(response_json)
    # Run the chain
    sorted_original_response = chain.invoke({"response_data": response_str})
    # Ensure valid JSON output
    if isinstance(sorted_original_response, dict):
        return sorted_original_response
    elif isinstance(sorted_original_response, str):
        if sorted_original_response.startswith("```json"):
            sorted_response = clean_and_parse_json(sorted_original_response)
            return sorted_response
        else:
            try:
                sorted_response = json.loads(sorted_original_response)
                return sorted_response
            except json.JSONDecodeError:
                print(
                    "Error: The LLM did not return valid JSON. Returning original data."
                )
                return sorted_original_response


def workflow(query_location, api_key=API_KEY, search_engine_id=SEARCH_ENGINE_ID):
    """
    function defining the entire workflow for searching and sorting groundwater entries
    """
    response = google_search(api_key, search_engine_id, query_location)
    articles = parse_search_results(response)
    sorted_articles = sort_groundwater_entries(articles)
    return sorted_articles


if __name__ == "__main__":
    QUERY = "La Jolla Shores, California"
    results = workflow(QUERY)
    print(results)
