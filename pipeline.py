import time
from agents import writer_chain , critic_chain
from tools import web_search, scrape_url

def run_research_pipeline(topic : str) -> dict:

    state = {}

    #search agent working 
    print("\n"+" ="*50)
    print("step 1 - search agent is working ...")
    print("="*50)

    # FAST PATH: Instead of using a slow LLM agent that loops to figure out how to search,
    # we directly call the search tool. This takes 1 second instead of 30 seconds.
    search_results_str = web_search.invoke(topic)
    state["search_results"] = search_results_str

    print("\n search result ", state['search_results'][:500])

    #step 2 - reader agent 
    print("\n"+" ="*50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("="*50)

    # FAST PATH: Extract the first URL from search results and scrape it directly.
    # No LLM agent needed for this step either!
    first_url = None
    for line in search_results_str.split('\n'):
        if line.startswith('URL: '):
            first_url = line.replace('URL: ', '').strip()
            break
            
    if first_url:
        scraped = scrape_url.invoke(first_url)
    else:
        scraped = "No URL found to scrape."

    state['scraped_content'] = scraped

    print("\nscraped content: \n", state['scraped_content'][:500])

    #step 3 - writer chain 

    print("\n"+" ="*50)
    print("step 3 - Writer is drafting the report ...")
    print("="*50)

    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results'][:800]} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content'][:800]}"
    )

    state["report"] = writer_chain.invoke({
        "topic" : topic,
        "research" : research_combined
    })

    print("\n Final Report\n",state['report'][:500])

    #critic report 

    print("\n"+" ="*50)
    print("step 4 - critic is reviewing the report ")
    print("="*50)

    state["feedback"] = critic_chain.invoke({
        "report":state['report']
    })

    print("\n critic report \n", state['feedback'][:500])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)
