def parse_api_input(json_data: dict) -> dict:
    """
    Parse a dictionary containing an API definition.
    Extracts 'method', 'url', and 'body' fields.
    """
    method = json_data.get("method")
    url = json_data.get("url")
    body = json_data.get("body", {})

    if not method or not url:
        raise ValueError("Invalid API JSON: 'method' and 'url' are required.")

    return {
        "method": str(method).upper(),
        "url": url,
        "body": body
    }
