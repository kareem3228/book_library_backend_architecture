search_books_tool_gimini = {
    "type": "function",
    "name": "search_books",
    "description": "searches for books in the database by title or part of the title",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "the title or part of the title of the book being searched for"
            }
        },
        "required": ["name"]
    }
}
