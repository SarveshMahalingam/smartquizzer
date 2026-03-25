import io
import re
import requests
from bs4 import BeautifulSoup
from pdfminer.high_level import extract_text

def extract_text_from_pdf(uploaded_file):
    """
    Extracts raw text from a Streamlit UploadedFile object using PDFMiner.
    """
    try:
        # PDFMiner can read directly from the byte stream provided by Streamlit
        raw_text = extract_text(uploaded_file)
        return clean_extracted_text(raw_text)
    except Exception as e:
        return f"Error extracting PDF: {str(e)}"

def extract_text_from_url(url):
    """
    Fetches a webpage and extracts the main text content.
    """
    try:
        # Add a polite User-Agent so websites don't block us as a malicious bot
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Pass the headers into the request
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status() # Check for HTTP errors
        
        # Parse the HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Remove script and style elements that contain code, not text
        for script_or_style in soup(["script", "style", "header", "footer", "nav"]):
            script_or_style.extract()
            
        # Get the clean text
        raw_text = soup.get_text(separator=' ')
        return clean_extracted_text(raw_text)
    except Exception as e:
        return f"Error extracting URL: {str(e)}"

def clean_extracted_text(text):
    """
    Cleans up the raw text by removing excessive whitespace, newlines, 
    and weird formatting artifacts.
    """
    # Replace multiple spaces and newlines with a single space
    cleaned_text = re.sub(r'\s+', ' ', text)
    
    # Remove special characters or unprintable artifacts if necessary
    cleaned_text = re.sub(r'[^\x00-\x7F]+', ' ', cleaned_text)
    
    return cleaned_text.strip()

def segment_into_chunks(text, max_words=500):
    """
    Segments the cleaned text into manageable knowledge chunks[cite: 22, 53].
    This is crucial so we don't overwhelm the LLM's context window later.
    """
    words = text.split()
    chunks = []
    
    for i in range(0, len(words), max_words):
        chunk = " ".join(words[i:i + max_words])
        chunks.append(chunk)
        
    return chunks

# --- Main Entry Point for the Frontend ---
def process_content(source_type, source_data):
    """
    Takes the input from Streamlit and routes it to the correct extractor.
    """
    if source_type == "File Upload":
        # Streamlit passes the file object directly
        text = extract_text_from_pdf(source_data)
    elif source_type == "URL Input":
        # Streamlit passes the URL string
        text = extract_text_from_url(source_data)
    else:
        return None, "Invalid source type."

    if text and not text.startswith("Error"):
        # Segment the text into knowledge chunks
        chunks = segment_into_chunks(text)
        
        # ==========================================
        # --- NEW: Print chunks to the terminal ---
        # ==========================================
        print(f"\n{'='*50}")
        print(f"SUCCESS: Extracted {len(chunks)} chunks from {source_type}")
        print(f"{'='*50}")
        
        for i, chunk in enumerate(chunks):
            print(f"\n--- CHUNK {i+1} ---")
            print(chunk)
            
        print(f"\n{'='*50}\n")
        # ==========================================
        
        return chunks, "Success"
    else:
        # If there's an error, print that to the terminal too
        print(f"\n[ERROR] Text extraction failed: {text}\n")
        return None, text