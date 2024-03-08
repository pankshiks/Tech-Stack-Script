import pandas as pd
import concurrent.futures
import requests
from bs4 import BeautifulSoup
import gzip
from urllib.parse import urlparse

# Define a function to extract frontend technologies
def extract_frontend_technologies(html):
    soup = BeautifulSoup(html, 'html.parser')
    html_elements = soup.find_all('html')
    css_elements = soup.find_all('style')
    script_elements = soup.find_all('script')
    frontend_technologies = set()
    if html_elements:
        frontend_technologies.add('HTML')
    if css_elements:
        frontend_technologies.add('CSS')
    if script_elements:
        frontend_technologies.add('JavaScript')
    return frontend_technologies

# Define a function to extract backend technologies and server information
def extract_backend_technologies(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            server = response.headers.get('Server')
            content_encoding = response.headers.get('content-encoding', '')
            if 'gzip' in content_encoding:
                try:
                    html = gzip.decompress(response.content).decode('utf-8')
                except Exception as e:
                    print(f"Error decoding gzipped content from URL: {url}")
                    print(e)
                    html = response.text
            else:
                html = response.text
            backend_technologies = set()
            backend_technologies.add('Python')
            backend_technologies.add('Java')
            backend_technologies.add('jQuery')
            backend_technologies.add('CMS')
            backend_technologies.add('Laravel')
            backend_technologies.add('Core Java')
            return backend_technologies, server
        else:
            print(f"Failed to fetch content from URL: {url} (Status Code: {response.status_code})")
            return None, None
    except Exception as e:
        print(f"Error occurred while fetching content from URL: {url}")
        print(e)
        return None, None

# Define a function to extract technologies
def extract_technologies(url):
    if not url.startswith('http'):
        url = 'http://' + url
    try:
        response = requests.get(url)
        if response.status_code == 200:
            frontend_technologies = extract_frontend_technologies(response.text)
            backend_technologies, server = extract_backend_technologies(url)
            return frontend_technologies, backend_technologies, server
        else:
            print(f"Failed to fetch content from URL: {url} (Status Code: {response.status_code})")
            return None, None, None
    except Exception as e:
        print(f"Error occurred while fetching content from URL: {url}")
        print(e)
        return None, None, None

# Define a function to process a chunk of data
def process_chunk(chunk):
    results = []
    for domain in chunk['Domain']:
        frontend, backend, server = extract_technologies(domain)
        results.append((domain, frontend, backend, server))
    return results

# Define the number of threads
num_threads = 10

# Read the CSV file into chunks
csv_file = "/home/lenovo/Music/model-of-layouts/Web-Gov-List-for-Yashraj.csv"
chunk_size = 1000
chunks = pd.read_csv(csv_file, chunksize=chunk_size)

# Create a ThreadPoolExecutor with the specified number of threads
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    results = []
    # Submit each chunk for processing
    futures = [executor.submit(process_chunk, chunk) for chunk in chunks]

    # Wait for all tasks to complete
    for future in concurrent.futures.as_completed(futures):
        try:
            results.extend(future.result())
        except Exception as e:
            print(f"Error occurred while processing chunk: {e}")

# Convert the results to a DataFrame and save to a new CSV file
result_df = pd.DataFrame(results, columns=['Domain', 'Frontend', 'Backend', 'Server'])
result_df.to_csv('output.csv', index=False)

print("All chunks processed and results saved to output.csv.")
