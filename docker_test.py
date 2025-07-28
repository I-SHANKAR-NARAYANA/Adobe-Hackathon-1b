import subprocess
import os
import tempfile
import shutil

def test_docker_build():
    """Test Docker image building"""
    print("Testing Docker build...")
    
    try:
        result = subprocess.run([
            "docker", "build", "--platform", "linux/amd64", 
            "-t", "adobe-hackathon-test:latest", "."
        ], capture_output=True, text=True, check=True)
        
        print("✅ Docker build successful")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Docker build failed: {e}")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False

def test_docker_run_1a():
    """Test Docker run for Round 1A"""
    print("Testing Docker run for Round 1A...")
    
    # Create temporary directories
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(input_dir)
        os.makedirs(output_dir)
        
        # You would copy test PDFs to input_dir here
        # For now, we'll just test the container startup
        
        try:
            result = subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{input_dir}:/app/input",
                "-v", f"{output_dir}:/app/output",
                "--network", "none",
                "adobe-hackathon-test:latest"
            ], capture_output=True, text=True, timeout=30)
            
            print("✅ Docker run completed")
            print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Docker run timed out")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker run failed: {e}")
            return False

def test_docker_run_1b():
    """Test Docker run for Round 1B"""
    print("Testing Docker run for Round 1B...")
    
    with tempfile.TemporaryDirectory() as temp_dir:
        input_dir = os.path.join(temp_dir, "input")
        output_dir = os.path.join(temp_dir, "output")
        os.makedirs(input_dir)
        os.makedirs(output_dir)
        
        try:
            result = subprocess.run([
                "docker", "run", "--rm",
                "-v", f"{input_dir}:/app/input",
                "-v", f"{output_dir}:/app/output",
                "--network", "none",
                "-e", "PERSONA=PhD Researcher in Computational Biology",
                "-e", "JOB=Prepare comprehensive literature review",
                "adobe-hackathon-test:latest"
            ], capture_output=True, text=True, timeout=60)
            
            print("✅ Docker run for Round 1B completed")
            print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return True
            
        except subprocess.TimeoutExpired:
            print("❌ Docker run timed out")
            return False
        except subprocess.CalledProcessError as e:
            print(f"❌ Docker run failed: {e}")
            return False

if __name__ == "__main__":
    print("=== Docker Testing Suite ===\n")
    
    # Test build
    build_success = test_docker_build()
    
    if build_success:
        print("\n" + "="*40 + "\n")
        
        # Test Round 1A
        test_docker_run_1a()
        
        print("\n" + "="*40 + "\n")
        
        # Test Round 1B
        test_docker_run_1b()
    
    print("\n=== Testing Complete ===")