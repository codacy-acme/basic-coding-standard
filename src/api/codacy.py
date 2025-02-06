"""Codacy API client for managing coding standards."""
import requests
import time
from typing import Dict, List
from src.config.settings import settings
from src.utils.logger import get_logger

logger = get_logger()

class CodacyAPI:
    """Client for interacting with the Codacy API."""
    
    def __init__(self):
        """Initialize the Codacy API client."""
        self.base_url = settings.api_url.rstrip('/')
        authority = self.base_url.replace('https://', '').replace('http://', '')
        self.headers = {
            'authority': authority,
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'api-token': settings.api_token,
            'x-requested-with': 'XMLHttpRequest'
        }
        self.provider = settings.provider
        self.org_name = settings.org_name

    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        json: Dict = None,
        data: str = None,
        params: Dict = None
    ) -> Dict:
        """
        Make an HTTP request to the Codacy API.
        
        Args:
            method: HTTP method (GET, POST, PUT, PATCH etc.)
            endpoint: API endpoint
            json: Optional JSON payload (for structured data)
            data: Optional string payload (for raw data)
            params: Optional query parameters
            
        Returns:
            API response as dictionary
            
        Raises:
            requests.exceptions.RequestException: If the API request fails
        """
        url = f"{self.base_url}/{endpoint.lstrip('/')}"
        logger.debug(f"Making {method} request to {url}")
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=json,
                data=data,
                params=params
            )
            response.raise_for_status()
            return response.json() if response.text else {}
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {str(e)}")
            if hasattr(e.response, 'json'):
                logger.error(f"Response: {e.response.json()}")
            raise

    def create_coding_standard(self, name: str) -> Dict:
        """
        Create a new coding standard.
        
        Args:
            name: Name of the coding standard
            
        Returns:
            Created coding standard details
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards"
        data = {
            "name": name,
            "languages": [
                "CSharp", "Java", "Go", "Kotlin", "Ruby", "Scala", "Python", "TypeScript", 
                "Javascript", "CoffeeScript", "Swift", "JSP", "VisualBasic", "PHP", "PLSQL", 
                "SQL", "TSQL", "Crystal", "Haskell", "Elixir", "Groovy", "Apex", "VisualForce", 
                "Velocity", "CSS", "HTML", "LESS", "SASS", "Dockerfile", "Terraform", "Shell", 
                "JSON", "XML", "Perl", "Lua", "Powershell", "YAML", "Cobol", "Rust", "Erlang", 
                "ABAP", "Objective C", "Markdown", "Julia", "Scratch", "FSharp", "Lisp", 
                "Prolog", "R", "Solidity", "Elm", "Fortran", "Dart", "OCaml", "Clojure", 
                "C", "CPP"
            ]
        }
        return self._make_request("POST", endpoint, json=data)

    def get_coding_standards(self) -> List[Dict]:
        """
        Get list of coding standards.
        
        Returns:
            List of coding standards
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards"
        response = self._make_request("GET", endpoint)
        return response.get('data', [])

    def get_available_tools(self) -> List[Dict]:
        """
        Get list of all available tools.
        
        Returns:
            List of tools
        """
        endpoint = "api/v3/tools"
        response = self._make_request("GET", endpoint)
        return response.get('data', [])

    def enable_tool(self, coding_standard_id: str, tool_uuid: str) -> Dict:
        """
        Enable a tool in the coding standard.
        
        Args:
            coding_standard_id: ID of the coding standard
            tool_uuid: UUID of the tool to enable
            
        Returns:
            Updated tool configuration
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards/{coding_standard_id}/tools/{tool_uuid}"
        data = {
            "enabled": True,
            "patterns": []
        }
        response = self._make_request("PATCH", endpoint, json=data)
        time.sleep(2)  # Rate limiting precaution
        return response

    def get_patterns(
        self,
        coding_standard_id: str,
        tool_uuid: str,
        limit: int = 100
    ) -> List[Dict]:
        """
        Get patterns for a specific tool.
        
        Args:
            coding_standard_id: ID of the coding standard
            tool_uuid: UUID of the tool
            limit: Number of patterns to fetch per page
            
        Returns:
            List of patterns
        """
        patterns = []
        cursor = ''
        has_next_page = True
        
        while has_next_page:
            endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards/{coding_standard_id}/tools/{tool_uuid}/patterns"
            params = {'limit': limit}
            if cursor:
                params['cursor'] = cursor
                
            response = self._make_request("GET", endpoint, params=params)
            patterns.extend(response.get('data', []))
            
            pagination = response.get('pagination', {})
            has_next_page = 'cursor' in pagination
            if has_next_page:
                cursor = pagination['cursor']
        
        return patterns

    def update_patterns(
        self,
        coding_standard_id: str,
        tool_uuid: str,
        patterns: List[Dict]
    ) -> Dict:
        """
        Update patterns for a tool.
        
        Args:
            coding_standard_id: ID of the coding standard
            tool_uuid: UUID of the tool
            patterns: List of pattern configurations to update
            
        Returns:
            Updated tool configuration
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards/{coding_standard_id}/tools/{tool_uuid}"
        data = {
            "enabled": True,
            "patterns": patterns
        }
        response = self._make_request("PATCH", endpoint, json=data)
        time.sleep(2)  # Rate limiting precaution
        return response

    def promote_draft(self, coding_standard_id: str) -> Dict:
        """
        Promote a draft coding standard.
        
        Args:
            coding_standard_id: ID of the coding standard
            
        Returns:
            Response data
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards/{coding_standard_id}/promote"
        return self._make_request("POST", endpoint)

    def set_default(self, coding_standard_id: str) -> Dict:
        """
        Set a coding standard as default.
        
        Args:
            coding_standard_id: ID of the coding standard
            
        Returns:
            Response data
        """
        endpoint = f"api/v3/organizations/{self.provider}/{self.org_name}/coding-standards/{coding_standard_id}/setDefault"
        data = {"isDefault": True}
        return self._make_request("POST", endpoint, json=data)
