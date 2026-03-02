from googlesearch import search
from config import MAX_RESULTS_GOOGLE

def find_first_linkedin(query: str) -> str:
    try:
        for url in search(query, num_results=MAX_RESULTS_GOOGLE, lang="fr"):
            if "linkedin.com" in url:
                return url
    except Exception as e:
        print(f"  -> Erreur lors de la recherche pour '{query}' : {e}")

    return ""