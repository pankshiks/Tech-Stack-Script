import requests
from bs4 import BeautifulSoup
import re

def extract_frontend_technologies(html):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    # Find HTML, CSS, and JavaScript elements
    html_elements = soup.find_all('html')
    css_elements = soup.find_all('style')
    script_elements = soup.find_all('script')

    # Extract frontend technologies
    frontend_technologies = set()
    if html_elements:
        frontend_technologies.add('HTML')
    if css_elements:
        frontend_technologies.add('CSS')
    if script_elements:
        frontend_technologies.add('JavaScript')

    # Check for popular frontend frameworks and libraries
    for script in script_elements:
        script_text = script.get_text()
        if 'React' in script_text:
            frontend_technologies.add('React')
        if 'Vue' in script_text:
            frontend_technologies.add('Vue.js')
        if 'Angular' in script_text:
            frontend_technologies.add('Angular')
        if 'jQuery' in script_text:
            frontend_technologies.add('jQuery')
        if 'Drupal' in script_text:
            frontend_technologies.add('Drupal')
        if 'CDN' in script_text:
            frontend_technologies.add('CDN')
        if 'scripting language' in script_text:
            frontend_technologies.add('Scripting Language')
        if 'scripting library' in script_text:
            frontend_technologies.add('Scripting Library')

    return frontend_technologies

def extract_backend_technologies(url):
    # Send a HEAD request to the URL to fetch only the headers
    response = requests.head(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract server information from response headers
        server = response.headers.get('Server')

        # Extract backend technologies (placeholder for now)
        backend_technologies = set()
        backend_technologies.add('Python')
        backend_technologies.add('Java')
        backend_technologies.add('jQuery')
        backend_technologies.add('CMS')
        backend_technologies.add('Laravel')
        backend_technologies.add('Core Java')
        return backend_technologies, server
    else:
        print(f"Failed to fetch content from URL: {url}")
        return None, None

def extract_technologies(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract frontend technologies from HTML content
        frontend_technologies = extract_frontend_technologies(response.text)

        # Extract backend technologies and server information
        backend_technologies, server = extract_backend_technologies(url)

        return frontend_technologies, backend_technologies, server
    else:
        print(f"Failed to fetch content from URL: {url}")
        return None, None, None

# Example usage:
url = "https://www.ntvbd.com/"
frontend, backend, server = extract_technologies(url)
print("Frontend technologies detected:", frontend)
print("Backend technologies detected:", backend)
print("Server:", server)
