import requests
from collections import Counter
from googleapiclient.discovery import build

# Function to get industry from Diffbot
def get_industry_from_diffbot(url):
    api_url = "https://api.diffbot.com/v3/article"
    api_key = "cf4cd0544b4bbae862e8b792c7959881"  # Replace with your Diffbot API key
    params = {
        'token': api_key,
        'url': url,
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        if 'application/json' in response.headers.get('Content-Type', ''):
            data = response.json()
            if 'objects' in data and data['objects']:
                return data['objects'][0]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from Diffbot API: {e}")
    return None

# Function to extract specific industry
def get_specific_industry(data):
    if data:
        tags_list = data.get('tags', [])
        specific_industry = ', '.join([str(tag.get('name', '')) for tag in tags_list]) if tags_list else None
        return specific_industry
    return None

# Function to crawl website and get industries
def crawl_website(start_url):
    current_url = start_url
    industries = []

    while len(set(industries)) < 3:  # Loop until there are at least three distinct industries
        article_data = get_industry_from_diffbot(current_url)

        if article_data:
            general_industries = article_data.get('categories', [])
            specific_industry = get_specific_industry(article_data)

            if specific_industry:
                industries.extend(specific_industry.split(', '))
            elif general_industries:
                general_industries_names = [category.get('name', '') for category in general_industries]
                industries.extend(general_industries_names)

        # Break the loop if three distinct industries have been identified
        if len(set(industries)) >= 4:
            break

    # Calculate the three most common industries
    most_common_industries = Counter(industries).most_common(4)
    return [industry for industry, count in most_common_industries]

# Function to perform Google Custom Search
def google_search(search_terms):
    api_key = "AIzaSyBHKRK8lSx0-V06ftxcccuF4Qo3jsIySK4"  # Your Google API key
    cse_id = "522dadda8ecdf466a"  # Your Custom Search Engine ID
    combined_search_query = ' OR '.join(search_terms)  # Combine industries into one search query
    service = build("customsearch", "v1", developerKey=api_key)
    res = service.cse().list(q=combined_search_query, cx=cse_id).execute()
    links = [item['link'] for item in res['items'][:20]]  # Extract and store the first 5 items
    return links

# New function to extract keywords from articles

# Updated function to extract keywords from articles, aiming for a minimum of 10 unique keywords
def extract_keywords_from_links(links):
    all_keywords = set()  # Using a set to avoid duplicate keywords
    for link in links:
        if len(all_keywords) >= 20:  # Stop if we have gathered at least 20 unique keywords
            break
        article_data = get_industry_from_diffbot(link)  # Reusing the function to get the article data
        if article_data and 'tags' in article_data:
            tags = article_data['tags'][:5]  # Attempt to get up to five tags per article
            for tag in tags:
                if 'label' in tag:
                    all_keywords.add(tag['label'])  # Add unique keywords
                if len(all_keywords) >= 20:  # Break if we have reached 20 unique keywords
                    break
    return list(all_keywords)  # Return the collected unique keywords, aiming for at least 12

def extract_metadata_from_links(links):
    metadata_list = []  # List to hold metadata dictionaries for each link
    for link in links:
        article_data = get_industry_from_diffbot(link)  # Reusing the function to get the article data
        if article_data:
            # Create a dictionary to store relevant metadata from the article
            metadata = {
                'url': link,
                'title': article_data.get('title', 'No title available'),
                'author': article_data.get('author', 'Author unknown'),
                'date': article_data.get('date', 'No date available')
            }
            metadata_list.append(metadata)
    return metadata_list



# Main function to integrate both scrapers and the new keywords extractor


# # Integrate into the main function
# def main():
#     user_link = input("Enter the link to start crawling: ")
#     industries = crawl_website(user_link)
#     if industries:
#         print("The three most common industries are:", ', '.join(industries))
#         print("\nLinks that fit well into all three industries:")
#         links = google_search(industries)
#         for link in links:
#             print(link)

#         print("\nExtracting keywords from the articles...")
#         keywords = extract_keywords_from_links(links)
#         if keywords:
#             print("Unique keywords extracted from the articles:", ', '.join(keywords))
#         else:
#             print("No keywords could be extracted.")

#         print("\nExtracting metadata from the articles...")
#         metadata = extract_metadata_from_links(links)
#         if metadata:
#             for data in metadata:
#                 print(f"Title: {data['title']}, Author: {data['author']}, Date: {data['date']}, URL: {data['url']}")
#         else:
#             print("No metadata could be extracted.")
#     else:
#         print("Failed to identify three distinct industries.")

# if __name__ == "__main__":
#     main()

def main(user_link):
    # No longer need to input inside the function
    categories_str = ""  # Use a string to hold all categories
    keywords = []
    print(user_link)
    # Fetch the article data from Diffbot
    article_data = get_industry_from_diffbot(user_link)

    if article_data:
        # Extract categories (industries)
        general_industries = article_data.get('categories', [])
        categories = [category.get('name', '') for category in general_industries]

        # Extract specific industries from tags, and use tags as keywords
        specific_industry = get_specific_industry(article_data)
        if specific_industry:
            categories.extend(specific_industry.split(', '))

        # Concatenate all categories into a single string
        categories_str = ', '.join(categories)

        # Use tags as keywords
        if 'tags' in article_data and article_data['tags']:
            keywords = [tag.get('label', '') for tag in article_data['tags'] if 'label' in tag]

        print("Categories (Industries) found:", categories_str)
        print("Keywords found:", ', '.join(keywords))
    else:
        print("Failed to fetch data for the provided link.")

    # Return categories string and keywords list
    return categories_str, keywords



