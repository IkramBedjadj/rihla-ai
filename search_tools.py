import os
import xml.etree.ElementTree as ET

# --- Third-party ---
import requests
from dotenv import load_dotenv
from tavily import TavilyClient
#import wikipedia



load_dotenv()



def tavily_search_tool(query: str, max_results: int = 5, include_images: bool = False) -> list[dict]:
    """
    Search Algerian official and news sources using Tavily.
    """

    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        raise ValueError("TAVILY_API_KEY not found in environment variables.")

    

    client = TavilyClient(api_key=api_key)

    # Give priority to Algerian sources
    algeria_query = (
        f"{query}"
        "site:aps.dz OR",
        "site:interieur.gov.dz OR",
        "site:protection-civile.dz OR",
        "site:meteo.dz OR",
        "site:sante.gov.dz OR",
        "site:tourisme.gov.dz OR",
        "site:entv.dz OR",
        "site:radioalgerie.dz OR",
        "site:airalgerie.dz OR",
        "site:sntf.dz OR",
        "site:echoroukonline.com OR",
        "site:ennaharonline.com OR",
        "site:elbilad.net OR",
        "site:elkhabar.com",
    )
    

    try:
        response = client.search(
            query=algeria_query,
            max_results=max_results,
            include_images=include_images
        )

        results = []

        for r in response.get("results", []):
            results.append({
                "title": r.get("title", ""),
                "content": r.get("content", ""),
                "url": r.get("url", "")
            })

        if include_images:
            for img in response.get("images", []):
                results.append({"image_url": img})

        return results

    except Exception as e:
        return [{"error": str(e)}]



tavily_tool_def = {
    "type": "function",
    "function": {
        "name": "tavily_search_tool",
        "description": "Searches Algerian official government websites and trusted Algerian news websites such as APS, Civil Protection, Ministry of Interior, Echorouk, Ennahar, El Bilad, El Khabar, Air Algerie, SNTF, and other official Algerian sources.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query."
                },
                "max_results": {
                    "type": "integer",
                    "default": 5
                },
                "include_images": {
                    "type": "boolean",
                    "default": False
                }
            },
            "required": ["query"]
        }
    }
}






def weather_tool(city: str) -> list[dict]:
    """
    Get the current weather for a city.
    """

    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        raise ValueError("OPENWEATHER_API_KEY not found in environment variables.")

    url = "https://api.openweathermap.org/data/2.5/weather"

    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "en"
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        result = {
            "city": data["name"],
            "country": data["sys"]["country"],
            "temperature": data["main"]["temp"],
            "feels_like": data["main"]["feels_like"],
            "humidity": data["main"]["humidity"],
            "pressure": data["main"]["pressure"],
            "weather": data["weather"][0]["description"],
            "wind_speed": data["wind"]["speed"],
        }

        return [result]

    except Exception as e:
        return [{"error": str(e)}]


weather_tool_def = {
    "type": "function",
    "function": {
        "name": "weather_tool",
        "description":  (
    "Gets the current weather for a city. "
    "The city parameter MUST be written in English "
    "(e.g. Algiers, Oran, Ouargla, Constantine)."
),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "City name (e.g. Algiers, Oran, Constantine)."
                }
            },
            "required": ["city"]
        }
    }
}    















def facebook_page_info_tool(page_id: str) -> list[dict]:
    """
    Get Facebook page transparency information.
    """

    api_key = os.getenv("RAPIDAPI_KEY")
    if not api_key:
        raise ValueError("RAPIDAPI_KEY not found in environment variables.")

    url = "https://facebook-scraper3.p.rapidapi.com/page/transparency"

    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "facebook-scraper3.p.rapidapi.com",
    }

    params = {
        "page_id": page_id
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            params=params,
            timeout=20
        )

        response.raise_for_status()

        data = response.json()

        return [data]

    except Exception as e:
        return [{"error": str(e)}]





facebook_page_info_tool_def = {
    "type": "function",
    "function": {
        "name": "facebook_page_info_tool",
        "description": (
            "Gets transparency information about a Facebook page "
            "using its page ID."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "page_id": {
                    "type": "string",
                    "description": "Facebook Page ID."
                }
            },
            "required": ["page_id"]
        }
    }
}







































def places_search_tool(
    city: str,
    category: str = "tourism",
    max_results: int = 10
) -> list[dict]:
    """
    Search for places in an Algerian city using OpenStreetMap.

    The city should be provided in English/Latin form,
    for example:
        Bejaia
        Oran
        Algiers
        Constantine
    """

    # --------------------------------------------------
    # 1. Geocode the city using Nominatim
    # --------------------------------------------------

    geocode_url = "https://nominatim.openstreetmap.org/search"

    geocode_params = {
        "q": f"{city}, Algeria",
        "format": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "AlgeriaTourismAgent/1.0"
    }

    try:

        response = requests.get(
            geocode_url,
            params=geocode_params,
            headers=headers,
            timeout=10
        )

        response.raise_for_status()

        locations = response.json()

        if not locations:
            return [{
                "error": f"Could not find location: {city}"
            }]

        latitude = float(locations[0]["lat"])
        longitude = float(locations[0]["lon"])

    except Exception as e:

        return [{
            "error": f"Geocoding error: {str(e)}"
        }]

    # --------------------------------------------------
    # 2. Search nearby places using Overpass
    # --------------------------------------------------

    overpass_url = "https://overpass-api.de/api/interpreter"

    # Tourism-related OSM tags
    if category == "tourism":

        query = f"""
        [out:json];
        (
          node["tourism"](around:15000,{latitude},{longitude});
          way["tourism"](around:15000,{latitude},{longitude});
          relation["tourism"](around:15000,{latitude},{longitude});

          node["historic"](around:15000,{latitude},{longitude});
          way["historic"](around:15000,{latitude},{longitude});
          relation["historic"](around:15000,{latitude},{longitude});
        );
        out center;
        """

    elif category == "restaurant":

        query = f"""
        [out:json];
        (
          node["amenity"="restaurant"]
            (around:10000,{latitude},{longitude});

          way["amenity"="restaurant"]
            (around:10000,{latitude},{longitude});
        );
        out center;
        """

    elif category == "hotel":

        query = f"""
        [out:json];
        (
          node["tourism"="hotel"]
            (around:10000,{latitude},{longitude});

          way["tourism"="hotel"]
            (around:10000,{latitude},{longitude});
        );
        out center;
        """

    elif category == "museum":

        query = f"""
        [out:json];
        (
          node["tourism"="museum"]
            (around:15000,{latitude},{longitude});

          way["tourism"="museum"]
            (around:15000,{latitude},{longitude});
        );
        out center;
        """

    elif category == "beach":

        query = f"""
        [out:json];
        (
          node["natural"="beach"]
            (around:20000,{latitude},{longitude});

          way["natural"="beach"]
            (around:20000,{latitude},{longitude});
        );
        out center;
        """

    else:

        return [{
            "error": f"Unsupported category: {category}"
        }]

    # --------------------------------------------------
    # 3. Execute Overpass query
    # --------------------------------------------------

    try:

        response = requests.post(
            overpass_url,
            data=query,
            headers=headers,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

    except Exception as e:

        return [{
            "error": f"Places search error: {str(e)}"
        }]

    # --------------------------------------------------
    # 4. Format results
    # --------------------------------------------------

    results = []

    for element in data.get("elements", []):

        tags = element.get("tags", {})

        name = tags.get("name")

        # Ignore places without names
        if not name:
            continue

        # Coordinates
        if element["type"] == "node":

            lat = element.get("lat")
            lon = element.get("lon")

        else:

            center = element.get("center", {})

            lat = center.get("lat")
            lon = center.get("lon")

        results.append({
            "name": name,
            "category": (
                tags.get("tourism")
                or tags.get("historic")
                or tags.get("amenity")
                or tags.get("natural")
                or category
            ),
            "latitude": lat,
            "longitude": lon,
            "website": tags.get("website"),
            "phone": tags.get("phone"),
            "address": tags.get("addr:street"),
        })

        if len(results) >= max_results:
            break

    return results





places_search_tool_def = {
    "type": "function",
    "function": {
        "name": "places_search_tool",

        "description": """
Search for real-world places in Algeria.

IMPORTANT:
This tool does NOT accept a general search query.

You MUST extract structured information from the user's request
and provide the arguments separately.

The tool requires:

1. city
2. category
3. max_results

The city must be converted to English/Latin form.

Examples:

بجاية -> Bejaia
وهران -> Oran
قسنطينة -> Constantine
جيجل -> Jijel
عنابة -> Annaba
تلمسان -> Tlemcen
الجزائر العاصمة -> Algiers

Category conversion examples:

"hotels" -> "hotel"
"فنادق" -> "hotel"
"hôtels" -> "hotel"

"restaurants" -> "restaurant"
"مطاعم" -> "restaurant"
"restaurants" -> "restaurant"

"museums" -> "museum"
"متاحف" -> "museum"

"beaches" -> "beach"
"شواطئ" -> "beach"

"tourist attractions" -> "tourism"
"أماكن سياحية" -> "tourism"
"معالم سياحية" -> "tourism"

Examples of correct tool calls:

User:
"give me top 5 hotels in bejaia"

Correct:
{
    "city": "Bejaia",
    "category": "hotel",
    "max_results": 5
}

User:
"عطيني 10 مطاعم في بجاية"

Correct:
{
    "city": "Bejaia",
    "category": "restaurant",
    "max_results": 10
}

User:
"وش كاين من شواطئ في جيجل؟"

Correct:
{
    "city": "Jijel",
    "category": "beach",
    "max_results": 10
}

NEVER send a "query" argument to this tool.
""",

        "parameters": {
            "type": "object",

            "properties": {

                "city": {
                    "type": "string",
                    "description": (
                        "The Algerian city in English/Latin form. "
                        "Example: Bejaia, Oran, Algiers."
                    )
                },

                "category": {
                    "type": "string",
                    "enum": [
                        "tourism",
                        "restaurant",
                        "hotel",
                        "museum",
                        "beach"
                    ],
                    "description": (
                        "The type of place to search for."
                    )
                },

                "max_results": {
                    "type": "integer",
                    "description": (
                        "Number of places requested by the user. "
                        "If the user does not specify a number, use 10."
                    ),
                    "default": 10
                }
            },

            "required": [
                "city",
                "category"
            ]
        }
    }
}




def wikivoyage_search_tool(city: str) -> list[dict]:
    """
    Get travel guide information about a city from Wikivoyage
    (practical tips, culture, safety, getting around, etc.).
    """

    url = "https://en.wikivoyage.org/w/api.php"

    params = {
        "action": "query",
        "prop": "extracts",
        "titles": city,
        "format": "json",
        "explaintext": True,
        "redirects": 1,  # follow redirects (e.g. "Bejaia" -> "Béjaïa")
    }

    headers = {
        "User-Agent": "AlgeriaTourismAgent/1.0"
    }

    try:
        response = requests.get(url, params=params, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()

        pages = data.get("query", {}).get("pages", {})

        results = []

        for page_id, page_data in pages.items():

            if page_id == "-1":
                return [{
                    "error": f"No Wikivoyage page found for: {city}"
                }]

            title = page_data.get("title", city)
            extract = page_data.get("extract", "")

            if not extract:
                return [{
                    "error": f"No content found for: {city}"
                }]

            # Truncate very long extracts to keep tool output manageable
            max_chars = 1500
            if len(extract) > max_chars:
                extract = extract[:max_chars] + "..."

            results.append({
                "title": title,
                "content": extract,
                "source": "Wikivoyage",
                "url": f"https://en.wikivoyage.org/wiki/{title.replace(' ', '_')}"
            })

        return results

    except Exception as e:
        return [{"error": str(e)}]


wikivoyage_tool_def = {
    "type": "function",
    "function": {
        "name": "wikivoyage_search_tool",
        "description": (
            "Gets travel guide information from Wikivoyage about an "
            "Algerian city: practical tips, getting around, safety, "
            "culture, when to visit, and general travel advice. "
            "Use this for local tips and general destination "
            "background — NOT for specific hotel or restaurant names "
            "(use places_search_tool for those)."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": (
                        "The city name in English, e.g. Bejaia, Oran, "
                        "Algiers, Constantine, Tlemcen."
                    )
                }
            },
            "required": ["city"]
        }
    }
}