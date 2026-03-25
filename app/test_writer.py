import os

def save_test_code(code: str, url: str) -> str:
    """
    Saves the generated pytest code to tests/test_<endpoint_name>.py
    Returns the path to the saved file.
    """
    # Define absolute paths
    app_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.dirname(app_dir)
    tests_dir = os.path.join(base_dir, 'tests')
    
    # Ensure tests directory exists
    os.makedirs(tests_dir, exist_ok=True)
    
    # Extract endpoint name from URL (e.g. /create-user -> create_user)
    endpoint_name = url.strip('/').replace('/', '_').replace('-', '_')
    if not endpoint_name:
        endpoint_name = "root"
        
    filename = f"test_{endpoint_name}.py"
    filepath = os.path.join(tests_dir, filename)
    
    # Write the code to the file
    with open(filepath, 'w') as f:
        f.write(code)
        
    return filepath
