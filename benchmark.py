import time
import psutil
import os
from main import PDFOutlineExtractor, PersonaDocumentAnalyzer

class PerformanceBenchmark:
    def __init__(self):
        self.process = psutil.Process(os.getpid())
    
    def get_memory_usage(self):
        """Get current memory usage in MB"""
        return self.process.memory_info().rss / 1024 / 1024
    
    def benchmark_round_1a(self, pdf_path):
        """Benchmark Round 1A performance"""
        print(f"Benchmarking Round 1A with {pdf_path}")
        
        extractor = PDFOutlineExtractor()
        
        # Memory before
        mem_before = self.get_memory_usage()
        
        # Time the extraction
        start_time = time.time()
        result = extractor.extract_outline(pdf_path)
        end_time = time.time()
        
        # Memory after
        mem_after = self.get_memory_usage()
        
        processing_time = end_time - start_time
        memory_used = mem_after - mem_before
        
        print(f"📊 Round 1A Benchmark Results:")
        print(f"   ⏱️  Processing Time: {processing_time:.2f} seconds")
        print(f"   🧠 Memory Usage: {memory_used:.2f} MB")
        print(f"   📄 Headings Found: {len(result['outline'])}")
        print(f"   📋 Document Title: {result['title']}")
        
        # Check constraints
        if processing_time <= 10:
            print("   ✅ Time constraint satisfied (≤10s)")
        else:
            print("   ❌ Time constraint violated (>10s)")
        
        return {
            "processing_time": processing_time,
            "memory_used": memory_used,
            "headings_count": len(result['outline']),
            "title": result['title']
        }
    
    def benchmark_round_1b(self, pdf_paths, persona, job):
        """Benchmark Round 1B performance"""
        print(f"Benchmarking Round 1B with {len(pdf_paths)} documents")
        
        analyzer = PersonaDocumentAnalyzer()
        
        # Memory before
        mem_before = self.get_memory_usage()
        
        # Time the analysis
        start_time = time.time()
        result = analyzer.analyze_documents(pdf_paths, persona, job)
        end_time = time.time()
        
        # Memory after
        mem_after = self.get_memory_usage()
        
        processing_time = end_time - start_time
        memory_used = mem_after - mem_before
        
        print(f"📊 Round 1B Benchmark Results:")
        print(f"   ⏱️  Processing Time: {processing_time:.2f} seconds")
        print(f"   🧠 Memory Usage: {memory_used:.2f} MB")
        print(f"   📑 Documents Processed: {len(result['metadata']['input_documents'])}")
        print(f"   🎯 Sections Extracted: {len(result['extracted_sections'])}")
        print(f"   🔍 Subsections: {len(result['subsection_analysis'])}")
        
        # Check constraints
        if processing_time <= 60:
            print("   ✅ Time constraint satisfied (≤60s)")
        else:
            print("   ❌ Time constraint violated (>60s)")
        
        return {
            "processing_time": processing_time,
            "memory_used": memory_used,
            "sections_count": len(result['extracted_sections']),
            "subsections_count": len(result['subsection_analysis'])
        }

def run_benchmarks():
    """Run performance benchmarks"""
    benchmark = PerformanceBenchmark()
    
    print("🚀 Starting Performance Benchmarks\n")
    
    # Test files (you would replace these with actual test files)
    test_pdf_1a = "sample.pdf"
    test_pdfs_1b = ["doc1.pdf", "doc2.pdf", "doc3.pdf"]
    test_persona = "PhD Researcher in Computational Biology"
    test_job = "Prepare comprehensive literature review focusing on methodologies"
    
    # Benchmark Round 1A
    if os.path.exists(test_pdf_1a):
        print("=" * 50)
        benchmark.benchmark_round_1a(test_pdf_1a)
    else:
        print(f"⚠️  Test file {test_pdf_1a} not found, skipping Round 1A benchmark")
    
    # Benchmark Round 1B
    existing_pdfs = [pdf for pdf in test_pdfs_1b if os.path.exists(pdf)]
    if existing_pdfs:
        print("\n" + "=" * 50)
        benchmark.benchmark_round_1b(existing_pdfs, test_persona, test_job)
    else:
        print("⚠️  No test files found for Round 1B, skipping benchmark")
    
    print("\n🏁 Benchmarking Complete")

if __name__ == "__main__":
    run_benchmarks()