import json
import sys

def validate_round_1a_output(filepath):
    """Validate Round 1A JSON output format"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Check required fields
        if "title" not in data:
            return False, "Missing 'title' field"
        
        if "outline" not in data:
            return False, "Missing 'outline' field"
        
        if not isinstance(data["outline"], list):
            return False, "'outline' must be a list"
        
        # Validate each outline item
        for i, item in enumerate(data["outline"]):
            if not isinstance(item, dict):
                return False, f"Outline item {i} must be a dictionary"
            
            required_fields = ["level", "text", "page"]
            for field in required_fields:
                if field not in item:
                    return False, f"Outline item {i} missing '{field}' field"
            
            # Validate level values
            if item["level"] not in ["H1", "H2", "H3"]:
                return False, f"Invalid level '{item['level']}' in item {i}"
            
            # Validate page number
            if not isinstance(item["page"], int) or item["page"] < 1:
                return False, f"Invalid page number in item {i}"
        
        return True, "Valid Round 1A output format"
        
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except FileNotFoundError:
        return False, "File not found"
    except Exception as e:
        return False, f"Error: {str(e)}"

def validate_round_1b_output(filepath):
    """Validate Round 1B JSON output format"""
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Check top-level structure
        required_sections = ["metadata", "extracted_sections", "subsection_analysis"]
        for section in required_sections:
            if section not in data:
                return False, f"Missing '{section}' section"
        
        # Validate metadata
        metadata = data["metadata"]
        metadata_fields = ["input_documents", "persona", "job_to_be_done", "processing_timestamp"]
        for field in metadata_fields:
            if field not in metadata:
                return False, f"Missing metadata field: {field}"
        
        # Validate extracted_sections
        sections = data["extracted_sections"]
        if not isinstance(sections, list):
            return False, "'extracted_sections' must be a list"
        
        for i, section in enumerate(sections):
            section_fields = ["document", "page_number", "section_title", "importance_rank"]
            for field in section_fields:
                if field not in section:
                    return False, f"Section {i} missing field: {field}"
        
        # Validate subsection_analysis
        subsections = data["subsection_analysis"]
        if not isinstance(subsections, list):
            return False, "'subsection_analysis' must be a list"
        
        for i, subsection in enumerate(subsections):
            subsection_fields = ["document", "refined_text", "page_number"]
            for field in subsection_fields:
                if field not in subsection:
                    return False, f"Subsection {i} missing field: {field}"
        
        return True, "Valid Round 1B output format"
        
    except json.JSONDecodeError:
        return False, "Invalid JSON format"
    except FileNotFoundError:
        return False, "File not found"
    except Exception as e:
        return False, f"Error: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate_output.py [1a|1b] <json_file>")
        sys.exit(1)
    
    round_type = sys.argv[1]
    filepath = sys.argv[2]
    
    if round_type == "1a":
        is_valid, message = validate_round_1a_output(filepath)
    elif round_type == "1b":
        is_valid, message = validate_round_1b_output(filepath)
    else:
        print("Invalid round type. Use '1a' or '1b'")
        sys.exit(1)
    
    print(f"Validation result: {message}")
    sys.exit(0 if is_valid else 1)