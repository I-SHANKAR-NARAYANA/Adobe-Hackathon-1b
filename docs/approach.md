# Adobe India Hackathon - Connecting the Dots

## Solution Overview

This solution addresses both Round 1A and Round 1B of the Adobe India Hackathon challenge.

### Round 1A: PDF Outline Extraction
- Extracts structured outlines (Title, H1, H2, H3) from PDF documents
- Uses PyMuPDF for fast, accurate text extraction with font information
- Implements intelligent heading detection using multiple strategies:
  - Font size analysis
  - Pattern matching (numbered sections, chapters, etc.)
  - Font formatting (bold, etc.)
- Outputs clean JSON format as specified

### Round 1B: Persona-Driven Document Intelligence
- Analyzes multiple PDF documents based on user persona and job requirements
- Extracts relevant sections and ranks them by importance
- Provides subsection analysis with refined text extraction
- Supports diverse domains (research papers, financial reports, textbooks, etc.)

## Technical Approach

### Round 1A Implementation
1. **Text Extraction**: Uses PyMuPDF to extract text with font metadata
2. **Title Detection**: Identifies largest font text on first page
3. **Heading Classification**: Multi-factor approach:
   - Regex patterns for common heading formats
   - Font size relative to document average
   - Font formatting flags (bold, italic)
   - Position and context analysis
4. **Level Determination**: Maps headings to H1/H2/H3 based on:
   - Numbering patterns (1., 1.1, 1.1.1)
   - Font size ratios
   - Chapter/section indicators

### Round 1B Implementation
1. **Section Extraction**: Identifies meaningful content blocks
2. **Relevance Scoring**: Multi-criteria scoring system:
   - Persona keyword matching
   - Job requirement alignment  
   - Section type identification
   - Content length and quality
3. **Ranking**: Sorts sections by relevance score
4. **Subsection Analysis**: Extracts key parts from top sections

## Libraries Used
- **PyMuPDF (fitz)**: PDF processing and text extraction
- **Standard Python**: json, re, os, datetime, logging, argparse

## Model Information
- No external ML models used
- All processing done with rule-based algorithms
- Optimized for speed and accuracy

## Build and Run Instructions

### Round 1A (PDF Outline Extraction)
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-extractor:latest .

# Run for outline extraction
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none pdf-extractor:latest
```

### Round 1B (Persona Analysis)
```bash
# Build the Docker image
docker build --platform linux/amd64 -t pdf-analyzer:latest .

# Run with persona and job parameters
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none -e PERSONA="PhD Researcher in Computational Biology" -e JOB="Prepare comprehensive literature review" pdf-analyzer:latest
```

## Performance Characteristics
- **Round 1A**: <5 seconds for 50-page PDF
- **Round 1B**: <30 seconds for 5 documents
- **Memory**: <500MB RAM usage
- **Model Size**: <50MB (no external models)
- **CPU Only**: Optimized for amd64 architecture

## Key Features
- **Multilingual Support**: Handles various languages including Japanese
- **Robust Parsing**: Multiple fallback strategies for heading detection
- **Scalable**: Processes multiple documents efficiently
- **Offline**: No internet connectivity required
- **Modular**: Clean separation between Round 1A and 1B functionality

## Error Handling
- Graceful handling of corrupted PDFs
- Fallback mechanisms for edge cases
- Comprehensive logging for debugging
- Input validation and sanitization

## Testing
- Tested on diverse PDF types (academic papers, reports, textbooks)
- Validated against sample inputs and expected outputs
- Performance tested on various document sizes
- Cross-platform compatibility verified