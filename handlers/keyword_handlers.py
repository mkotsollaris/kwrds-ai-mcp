"""
Keyword Research Handlers
Handles all keyword-related MCP tool calls
"""

from typing import Dict, Any
from utils.http_client import make_api_request
from utils.response_utils import limit_response_size


class KeywordHandlers:
    def __init__(self, api_base_url: str, workflow_base_url: str = None):
        self.api_base_url = api_base_url
        self.workflow_base_url = workflow_base_url or "https://workflow.api.kwrds.ai"

    def handle_keywords(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle keywords tool call"""
        url = f"{self.api_base_url}/keywords"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "search_question": args["search_question"],
            "search_country": args["search_country"],
            "version": args.get("version", "1"),
            "email": api_key  # Using API key as email for compatibility
        }
        response = make_api_request(url, headers, data)
        return limit_response_size(response, max_items=10)

    def handle_keywords_with_volumes(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle keywords with volumes tool call"""
        url = f"{self.api_base_url}/keywords-with-volumes"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "search_question": args["search_question"],
            "search_country": args["search_country"],
            "email": api_key  # Using API key as email for compatibility
        }
        if "limit" in args:
            data["limit"] = min(args["limit"], 10)  # Cap at 10 for MCP
        else:
            data["limit"] = 10  # Default limit for MCP
        if "vendor" in args:
            data["vendor"] = args["vendor"]
        response = make_api_request(url, headers, data)
        return limit_response_size(response, max_items=10)

    def handle_search_volume(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle search volume tool call"""
        url = f"{self.api_base_url}/search-volume"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "keywords": args["keywords"][:10] if isinstance(args["keywords"], list) else args["keywords"],  # Limit input keywords
            "search_country": args["search_country"],
            "version": args.get("version", "1"),
            "email": api_key  # Using API key as email for compatibility
        }
        response = make_api_request(url, headers, data)
        return limit_response_size(response, max_items=10)

    def handle_related_keywords(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle related keywords tool call"""
        url = f"{self.api_base_url}/related-keywords"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "search_question": args["search_question"],
            "search_country": args["search_country"],
            "email": api_key  # Using API key as email for compatibility
        }
        if "limit" in args:
            data["limit"] = min(args["limit"], 10)  # Cap at 10 for MCP
        else:
            data["limit"] = 10  # Default limit for MCP
        response = make_api_request(url, headers, data)
        return limit_response_size(response, max_items=10)

    def handle_lsi(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle LSI tool call"""
        url = f"{self.api_base_url}/lsi"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "search_question": args["search_question"],
            "search_country": args["search_country"],
            "email": api_key  # Using API key as email for compatibility
        }
        response = make_api_request(url, headers, data)
        return limit_response_size(response, max_items=10)

    def handle_topic_research_create(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle topic research create tool call"""
        url = f"{self.workflow_base_url}/topic-research"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        data = {
            "topic": args["topic"],
        }

        # Add optional parameters if provided
        if "search_country" in args:
            data["search_country"] = args["search_country"]
        if "max_children" in args:
            data["max_children"] = args["max_children"]
        if "manual_pages" in args:
            data["manual_pages"] = args["manual_pages"]
        if "traffic_rate" in args:
            data["traffic_rate"] = args["traffic_rate"]
        if "conversion_rate" in args:
            data["conversion_rate"] = args["conversion_rate"]

        response = make_api_request(url, headers, data, method="POST")
        return response

    def handle_topic_research_status(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle topic research status tool call"""
        job_id = args["job_id"]
        url = f"{self.workflow_base_url}/topic-research/{job_id}"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        response = make_api_request(url, headers, method="GET")
        return response

    def handle_topic_research_list(self, args: Dict[str, Any], api_key: str) -> Dict[str, Any]:
        """Handle topic research list tool call"""
        url = f"{self.workflow_base_url}/topic-research/jobs"
        headers = {"X-API-KEY": api_key, "Content-Type": "application/json"}
        response = make_api_request(url, headers, method="GET")
        return response 