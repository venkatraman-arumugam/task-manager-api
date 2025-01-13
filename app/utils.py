import json

def add_global_filters(app):
    """Add global filters to a Flask app instance."""
    def remove_none_values(data):
        """Recursively remove keys with None values from a dictionary."""
        if isinstance(data, dict):
            return {k: remove_none_values(v) for k, v in data.items() if v is not None}
        elif isinstance(data, list):
            return [remove_none_values(item) for item in data]
        return data

    @app.after_request
    def filter_none_values(response):
        """Filter out None values globally for JSON responses."""
        if response.is_json:
            original_data = response.get_json()
            filtered_data = remove_none_values(original_data)
            response.set_data(json.dumps(filtered_data))
        return response