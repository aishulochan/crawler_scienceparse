This repository contains two main components:  
📂 crawler_scienceparse

- **`crawler/`**  
  - Contains scripts for extracting research papers from the **ACL (Association for Computational Linguistics) website** for the years **2020-2024**.  
  - The extracted data includes metadata, abstracts, and other relevant details of research papers.  
  - Each year has a separate output file storing the extracted information.  

- **`science_parse/`**
  - Processes the output generated by the crawler.  
  - Utilizes **Science Parse** to convert the extracted data into a simplified text format for easier analysis.  
  - Performs additional preprocessing, such as text normalization and structuring of paper contents.  

## 🚀 Features  
- **Automated Research Paper Extraction**: Fetches research papers from ACL for the specified years.  
- **Structured Output Generation**: Organizes extracted data in a systematic format for easy access.  
- **Text Processing & Simplification**: Converts raw extracted content into a readable and structured format.  

## 🛠️ How to Use  
1. **Run the Crawler**:  
   - Navigate to the `crawler/` folder and execute the script to extract research papers.  
   - The output will be stored in corresponding year-wise files.  

2. **Process with Science Parse**:  
   - Navigate to the `science_parse/` folder and run the script to process the extracted papers.  
   - The output will be converted into a simplified text format.  

## 📌 Future Enhancements  

- Extend the crawler to support additional conferences and journals.  
- Improve text processing for better readability and structure.  
- Integrate machine learning techniques for automatic summarization of research papers.  
