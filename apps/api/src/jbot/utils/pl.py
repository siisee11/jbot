def get_language_from_filename(filename):
    # Extract the file extension
    extension = filename.split(".")[-1].lower()

    # Mapping of common file extensions to programming languages
    language_map = {
        "py": "python",
        "js": "javascript",
        "jsx": "javascript",
        "ts": "typescript",
        "tsx": "typescript",
        "java": "java",
        "cpp": "c++",
        "c": "c",
        "html": "html",
        "css": "css",
        "rb": "ruby",
        "php": "php",
        "rs": "rust",
        # Add more file extensions and their corresponding languages as needed
    }

    # Lookup the language based on the extension
    language = language_map.get(extension, "txt")

    return language
