import os
from exa_py import Exa
from langchain.agents import tool

class ExaSearchToolset:
    def _exa():
        return Exa(api_key=os.environ.get("EXA_API_KEY"))
    
    @tool
    def search(query: str):
        """"Search for a webpage based on the query."""
        return ExaSearchToolset._exa().search(f"{query}", use_autoprompt=True, num_results=3)

    @tool
    def find_similar(url: str):
        """Search for webpages similar to the given URL.
        The url passed should be a URL returned from `search`"""
        return ExaSearchToolset._exa().find_similar(url, num_results=3)
    
    @tool
    def get_contents(ids_dict):
        """Get the contents of a webpage given its ID.
        The ids must be passed in as a dictionary with a key 'ids', a list of ids returned from `search`."""
        if not isinstance(ids_dict, dict) or "ids" not in ids_dict:
            raise ValueError("The ids parameter must be a dictionary with a key 'ids' containing a list of URLs.")

        ids = ids_dict["ids"]
        if not isinstance(ids, list):
            raise ValueError("The 'ids' key must contain a list of URLs.")

        contents = ExaSearchToolset._exa().get_contents(ids)
        contents = str(contents).split("URL:")
        contents = [content[:1000] for content in contents]

        return "\n\n".join(contents)
    
    def tools():
        return [
            ExaSearchToolset.search,
            ExaSearchToolset.find_similar,
            ExaSearchToolset.get_contents
        ]
        