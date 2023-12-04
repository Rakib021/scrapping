import csv
from bs4 import BeautifulSoup
import requests

def scrape_page(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
        soup = BeautifulSoup(html_content, 'html.parser')

        table = soup.find('table', class_='post-list')
        rows = table.find_all('tr')[1:]  # Skip the header row

        data_list = []

        for row in rows:
            columns = row.find_all('td')
            date = columns[0].get_text(strip=True)
            title_tag = columns[2].find('a', title=True)
            author_tag = columns[2].find('div', class_='author-name')

            if title_tag:
                title = title_tag.get_text(strip=True)
                url = title_tag['href']

                url_p = f"https://www.bangla-kobita.com/{url}"
                response = requests.get(url_p)

                if response.status_code == 200:
                    html_content = response.text
                    soup = BeautifulSoup(html_content, 'html.parser')

                    kobita_tags = soup.find_all(class_='post-content noselect')

                    for tag in kobita_tags:
                        p_tags = tag.find_all('p')
                        author_name = ""

                        if author_tag:
                            author_name_tag = author_tag.find('a')
                            if author_name_tag:
                                author_name = author_name_tag.get_text(strip=True)

                        poem = ""
                        for p_tag in p_tags:
                            text_with_newline = p_tag.get_text(separator='\n')
                            poem += text_with_newline + "\n"

                        data_list.append({'Title': title, 'Author': author_name, 'Poem': poem})

        return data_list
    else:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return []

def main():
    base_url = "https://www.bangla-kobita.com/ashor/dhorrmiyo-kobita/?p="

    total_pages = 10  # Adjust this based on the total number of pages

    all_data = []

    for page_number in range(1, total_pages + 1):
        url = f"{base_url}{page_number}"
        page_data = scrape_page(url)
        all_data.extend(page_data)
        print(page_number)

    # Write the data to a CSV file
    csv_file_path = 'bangla_kobita_Religious_data.csv'
    fields = ['Title', 'Author', 'Poem']

    with open(csv_file_path, mode='w', encoding='utf-8', newline='') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fields)
        
        # Write the header
        writer.writeheader()
        
        # Write the data
        writer.writerows(all_data)

    print(f"Data has been written to {csv_file_path}")

if __name__ == "__main__":
    main()
