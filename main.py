# Adobe India Hackathon - Connecting the Dots
# Complete Solution for Round 1A and 1B

import os
import json
import re
import time
from datetime import datetime
from typing import List, Dict, Any, Tuple
import fitz  # PyMuPDF
from dataclasses import dataclass
import argparse
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class HeadingInfo:
    level: str
    text: str
    page: int
    font_size: float = 0.0
    font_flags: int = 0
    bbox: Tuple[float, float, float, float] = None

@dataclass
class Section:
    document: str
    page_number: int
    section_title: str
    importance_rank: int
    content: str = ""

@dataclass
class SubSection:
    document: str
    refined_text: str
    page_number: int

class PersonaDocumentAnalyzer:
    """Round 1B: Persona-driven document intelligence"""
    
    def __init__(self):
        self.section_keywords = {
            "methodology": ["method", "approach", "technique", "procedure", "algorithm"],
            "results": ["result", "finding", "outcome", "performance", "evaluation"],
            "introduction": ["introduction", "background", "overview", "summary"],
            "conclusion": ["conclusion", "summary", "discussion", "implication"],
            "analysis": ["analysis", "examination", "study", "investigation"],
            "data": ["data", "dataset", "statistics", "metrics", "numbers"]
        }
    
    def extract_document_sections(self, pdf_path: str) -> List[Dict]:
        """Extract sections from a single PDF"""
        doc = fitz.open(pdf_path)
        sections = []
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            
            # Split by potential section breaks
            paragraphs = text.split('\n\n')
            
            for i, paragraph in enumerate(paragraphs):
                paragraph = paragraph.strip()
                if len(paragraph) > 50:  # Meaningful content
                    # Try to identify section title
                    lines = paragraph.split('\n')
                    potential_title = lines[0].strip()
                    
                    if len(potential_title) < 100 and len(lines) > 1:
                        sections.append({
                            "document": os.path.basename(pdf_path),
                            "page_number": page_num + 1,
                            "section_title": potential_title,
                            "content": paragraph,
                            "importance_rank": 0  # Will be calculated later
                        })
        
        doc.close()
        return sections
    
    def calculate_relevance_score(self, section: Dict, persona: str, job: str) -> float:
        """Calculate how relevant a section is to the persona and job"""
        content = (section["content"] + " " + section["section_title"]).lower()
        persona_lower = persona.lower()
        job_lower = job.lower()
        
        score = 0.0
        
        # Check for persona-related keywords
        persona_keywords = persona_lower.split()
        for keyword in persona_keywords:
            if keyword in content:
                score += 2.0
        
        # Check for job-related keywords
        job_keywords = job_lower.split()
        for keyword in job_keywords:
            if keyword in content:
                score += 3.0
        
        # Check for section type relevance
        for section_type, keywords in self.section_keywords.items():
            for keyword in keywords:
                if keyword in content:
                    score += 1.0
        
        # Bonus for longer, more substantial content
        score += min(len(section["content"]) / 1000, 2.0)
        
        return score
    
    def analyze_documents(self, document_paths: List[str], persona: str, job: str) -> Dict:
        """Main analysis function for Round 1B"""
        all_sections = []
        
        # Extract sections from all documents
        for doc_path in document_paths:
            sections = self.extract_document_sections(doc_path)
            all_sections.extend(sections)
        
        # Calculate relevance scores
        for i, section in enumerate(all_sections):
            score = self.calculate_relevance_score(section, persona, job)
            all_sections[i]["relevance_score"] = score
        
        # Sort by relevance and assign importance ranks
        all_sections.sort(key=lambda x: x["relevance_score"], reverse=True)
        
        # Take top 10 most relevant sections
        top_sections = all_sections[:10]
        
        for i, section in enumerate(top_sections):
            section["importance_rank"] = i + 1
            del section["relevance_score"]  # Remove internal scoring
        
        # Create subsections (extract key parts from top sections)
        subsections = []
        for section in top_sections[:5]:  # Top 5 for subsections
            content_lines = section["content"].split('\n')
            # Take first few meaningful lines as refined text
            refined_lines = [line.strip() for line in content_lines if len(line.strip()) > 20]
            refined_text = ' '.join(refined_lines[:3])  # First 3 substantial lines
            
            if refined_text:
                subsections.append({
                    "document": section["document"],
                    "refined_text": refined_text[:500],  # Limit length
                    "page_number": section["page_number"]
                })
        
        # Prepare output
        result = {
            "metadata": {
                "input_documents": [os.path.basename(path) for path in document_paths],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": [
                {
                    "document": section["document"],
                    "page_number": section["page_number"],
                    "section_title": section["section_title"],
                    "importance_rank": section["importance_rank"]
                }
                for section in top_sections
            ],
            "subsection_analysis": subsections
        }
        
        return result

def main():
    input_dir = Path("/app/input")
    output_dir = Path("/app/output")

    os.makedirs(output_dir, exist_ok=True)

    analyzer = PersonaDocumentAnalyzer()

    if not input_dir.exists():
        logger.error(f"Input directory {input_dir} does not exist.")
        return

    for test_case_folder in input_dir.iterdir():
        if not test_case_folder.is_dir():
            continue

        logger.info(f"Processing test case folder: {test_case_folder.name}")

        # Find the JSON metadata file
        json_files = list(test_case_folder.glob("*.json"))
        if not json_files:
            logger.warning(f"No JSON metadata file found in {test_case_folder}")
            continue

        metadata_path = json_files[0]
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)

        persona = metadata.get("persona", {}).get("role", "")
        job = metadata.get("job_to_be_done", {}).get("task", "")

        if not persona or not job:
            logger.warning(f"Missing persona or job in metadata for {test_case_folder.name}")
            continue

        pdf_dir = test_case_folder / "PDFs"
        if not pdf_dir.exists():
            logger.warning(f"No PDFs directory found in {test_case_folder}")
            continue

        pdf_files = list(pdf_dir.glob("*.pdf"))
        if not pdf_files:
            logger.warning(f"No PDF files found in {pdf_dir}")
            continue

        # Analyze
        try:
            result = analyzer.analyze_documents([str(pdf) for pdf in pdf_files], persona, job)

            output_subdir = output_dir / test_case_folder.name
            output_subdir.mkdir(parents=True, exist_ok=True)

            output_filename = metadata_path.stem + "_output.json"
            output_path = output_subdir / output_filename

            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)

            logger.info(f"Saved output to {output_path}")
        except Exception as e:
            logger.error(f"Error processing {test_case_folder.name}: {str(e)}")

if __name__ == "__main__":
    main()