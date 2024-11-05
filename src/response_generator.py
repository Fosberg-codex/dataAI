class ResponseGenerator:
    def format_response(self, response: str) -> str:
        # Add formatting and structure to the response
        formatted_response = response.strip()
        
        # Add line breaks for readability
        formatted_response = formatted_response.replace(". ", ".\n")
        
        return formatted_response