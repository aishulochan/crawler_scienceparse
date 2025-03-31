import requests
import pandas as pd
import re
import pdfplumber
import io
import json

def is_doi(value):
    """Check if the value is a DOI (not a direct URL)."""
    return bool(re.match(r'^10\.\d{4,9}/[-._;()/:A-Z0-9]+$', value, re.IGNORECASE))

def extract_pdf_links(doi):
    """Fetch pdf_link using the Semantic Scholar API for a given DOI."""
    api_url = f'https://api.semanticscholar.org/v1/paper/{doi}'
    response = requests.get(api_url)
    
    if response.status_code == 200:
        data = response.json()
        return data.get('pdfUrls', [])
    else:
        print(f"Error fetching DOI {doi}: {response.status_code}")
        return []

def extract_text_from_pdf_from_url(pdf_url):
    """Extract text from a PDF directly from a URL using pdfplumber."""
    try:
        response = requests.get(pdf_url)
        response.raise_for_status()  # Ensure valid response
        
        with io.BytesIO(response.content) as pdf_file:
            with pdfplumber.open(pdf_file) as pdf:
                text = [page.extract_text() for page in pdf.pages if page.extract_text()]
        
        return text
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_url}: {e}")
        return []

def split_sections(text):
    """Attempt to split text into meaningful sections based on simple heuristics."""
    sections = []
    current_section = {"heading": "Introduction", "text": ""}
    
    for page_text in text:
        lines = page_text.split("\n")
        
        for line in lines:
            if re.match(r"^\d+\.\s[A-Z]", line):  # Detecting section headings (e.g., "1. Introduction")
                sections.append(current_section)
                current_section = {"heading": line, "text": ""}
            else:
                current_section["text"] += line + " "
    
    sections.append(current_section)  # Append last section
    return sections

def process_csv(file_path, output_file):
    """Reads a CSV file containing DOIs or direct pdf_link, processes them, and extracts structured content."""
    try:
        df = pd.read_csv(file_path)
        if 'pdf_link' not in df.columns:
            print("Error: 'pdf_link' column not found in CSV file.")
            return
        
        df = df.head(5)  # Process only the first 5 research papers
        
        results = []
        for entry in df['pdf_link'].dropna():
            extracted_text = []
            pdf_urls = [entry] if not is_doi(entry) else extract_pdf_links(entry)
            
            for url in pdf_urls:
                extracted_text = extract_text_from_pdf_from_url(url)
                if extracted_text:
                    break  # Use the first successful extraction
            
            sections = split_sections(extracted_text)
            
            paper_data = {
                "title": "Unknown Title",  # Placeholder
                "authors": [{"affiliations": [], "name": "Unknown Author"}],  # Placeholder
                "year": 2021,  # Placeholder
                "id": entry,  # Using DOI/URL as the ID
                "abstractText": sections[0]["text"] if sections else "",  # Use first section as abstract if available
                "sections": sections[1:]  # Exclude abstract from main sections
            }
            
            results.append(paper_data)
        
        # Write the results to a JSON file
        with open(output_file, 'w', encoding='utf-8') as output_json:
            json.dump(results, output_json, ensure_ascii=False, indent=4)
        
        print(f"Extraction complete. Results saved to {output_file}")
        
    except Exception as e:
        print(f"Error processing CSV file: {e}")

# Example usage
if __name__ == "__main__":
    input_csv = r"C:\Users\KIIT\Downloads\Project\modified_acl_papers.csv"
    output_json = r"C:\Users\KIIT\Downloads\Project\extracted_textsfinal.txt"
    process_csv(input_csv, output_json)
