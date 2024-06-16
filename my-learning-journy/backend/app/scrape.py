import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def scrape_books_from_page(url):
    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}, status code: {response.status_code}")
            return pd.DataFrame()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        books = []
        
        # Find all book elements on the page
        book_sections = soup.find_all('div', class_='book-row')
        
        if not book_sections:
            print(f"No book sections found in {url}")
            return pd.DataFrame()

        for section in book_sections:
            title_element = section.find('h3')
            author_element = section.find('p', class_='authors')
            rating_element = section.find('p', class_='rating')
            category_element = section.find('p', class_='categories')
            description_element = section.find('p', class_='synopsis')
            link_element = section.find('a', class_='book-download')
            
            title = title_element.get_text().strip() if title_element else 'N/A'
            author = author_element.get_text().strip() if author_element else 'N/A'
            rating_info = rating_element.get_text().strip() if rating_element else 'N/A'
            category = category_element.get_text().strip() if category_element else 'N/A'
            description = description_element.get_text().strip() if description_element else 'N/A'
            link = link_element['href'] if link_element else 'N/A'
            
            # Extract rating and rating count
            rating_match = re.search(r'\d+\.\d+', rating_info)
            rating = float(rating_match.group()) if rating_match else 0.0
            rating_count_match = re.search(r'\d+', rating_info)
            rating_count = int(rating_count_match.group()) if rating_count_match else 0
            
            year = 'N/A'  # Year is not provided in this example, set to 'N/A'
            
            if rating_count >= 1000:  # Filter books with at least 1000 ratings
                books.append({
                    'title': title,
                    'author': author,
                    'year': year,
                    'rating': rating,
                    'rating_count': rating_count,
                    'category': category,
                    'description': description,
                    'link': link
                })
        
        if not books:
            print("No valid books found.")
            return pd.DataFrame()
        
        books_df = pd.DataFrame(books)
        top_books = books_df.sort_values(by='rating', ascending=False).head(50)
        
        return top_books
    
    except Exception as e:
        print(f"An error occurred: {e}")
        return pd.DataFrame()
