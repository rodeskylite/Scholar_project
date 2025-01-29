import requests
import pandas as pd

# Configurar la URL base de OpenAlex
BASE_URL = "https://api.openalex.org/works"

# Función para buscar papers
def search_papers(query, limit=50):
    params = {
        "filter": "abstract.search:landslides,publication_year:2020-2025",
        "sort": "citation_count:desc",
        "per_page": 50
    }

    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error {response.status_code}: {response.text}")
        return []

# Buscar papers sobre el tema "machine learning and wildfires"
query = "machine learning and lanslides"
papers = search_papers(query, limit=50)

# Procesar los resultados
if papers:
    data = []
    for paper in papers:
        data.append({
            "Title": paper.get("title"),
            "Authors": ", ".join([author["author"]["display_name"] for author in paper.get("authorships", [])]),
            "Year": paper.get("publication_year"),
            "DOI": paper.get("doi"),
            "URL": paper.get("id"),
            "Abstract": paper.get("abstract_inverted_index"),
        })

    # Crear un DataFrame y guardar los datos en un archivo CSV
    df = pd.DataFrame(data)
    df.to_csv("openalex_papers.csv", index=False)
    print("Base de datos generada exitosamente.")
else:
    print("No se encontraron resultados.")
