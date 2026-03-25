import subprocess

def run_pytest(test_file: str):
    """
    Runs pytest on the specified file using subprocess.
    Captures and prints pass/fail results.
    """
    print(f"\n--- Running Pytest on {test_file} ---")
    
    try:
        # Run pytest
        result = subprocess.run(
            ['pytest', test_file, '-v'],
            capture_output=True,
            text=True
        )
        
        # Print output stream
        print(result.stdout)
        
        if result.returncode == 0:
            print("\n✅ All tests passed!")
        else:
            print("\n❌ Tests failed.")
            if result.stderr:
                print("Errors:")
                print(result.stderr)
                
    except FileNotFoundError:
        print("\n❌ pytest command not found. Ensure 'pytest' is installed and your virtual environment is activated.")
    except Exception as e:
        print(f"\n❌ Error executing pytests: {e}")
