"""
AgentMind API Client - handles communication with hosted service
"""
import os
import time
import requests
from typing import Optional, Dict, Any
from urllib.parse import urljoin


class APIClient:
    """Internal API client for AgentMind hosted service"""
    
    def __init__(self, api_key: str, base_url: str = "https://api.agentmind.ai/v1"):
        self.api_key = api_key
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "agentmind-python/0.1.0"
        })
        
        # Track usage for client-side rate limiting
        self._last_request_time = 0
        self._request_count = 0
    
    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict[str, Any]] = None,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make API request with retries and error handling"""
        
        # Simple client-side rate limiting
        current_time = time.time()
        if current_time - self._last_request_time < 0.1:  # Max 10 req/sec
            time.sleep(0.1 - (current_time - self._last_request_time))
        
        url = urljoin(self.base_url, endpoint)
        
        try:
            response = self.session.request(
                method=method,
                url=url,
                json=data,
                params=params,
                timeout=30
            )
            
            # Track for rate limiting
            self._last_request_time = time.time()
            self._request_count += 1
            
            # Handle errors
            if response.status_code == 401:
                raise AuthenticationError("Invalid API key")
            elif response.status_code == 429:
                raise RateLimitError("Rate limit exceeded")
            elif response.status_code == 402:
                raise PaymentRequiredError("Payment required - upgrade your plan")
            elif response.status_code >= 500:
                raise ServerError(f"Server error: {response.status_code}")
            
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.Timeout:
            raise TimeoutError("Request timed out")
        except requests.exceptions.ConnectionError:
            raise ConnectionError("Could not connect to AgentMind API")
    
    def store_memory(self, memory_data: Dict[str, Any]) -> Dict[str, Any]:
        """Store a memory via API"""
        return self._make_request("POST", "/memories", data=memory_data)
    
    def recall_memories(self, recall_params: Dict[str, Any]) -> Dict[str, Any]:
        """Recall memories via API"""
        return self._make_request("POST", "/recall", data=recall_params)
    
    def get_memory(self, memory_id: str) -> Dict[str, Any]:
        """Get specific memory"""
        return self._make_request("GET", f"/memories/{memory_id}")
    
    def delete_memory(self, memory_id: str) -> Dict[str, Any]:
        """Delete specific memory"""
        return self._make_request("DELETE", f"/memories/{memory_id}")
    
    def get_usage(self) -> Dict[str, Any]:
        """Get current usage stats"""
        return self._make_request("GET", "/usage")
    
    def health_check(self) -> bool:
        """Check if API is healthy"""
        try:
            response = self._make_request("GET", "/health")
            return response.get("status") == "healthy"
        except:
            return False


# Custom exceptions
class AgentMindError(Exception):
    """Base exception for AgentMind"""
    pass

class AuthenticationError(AgentMindError):
    """Invalid API key"""
    pass

class RateLimitError(AgentMindError):
    """Rate limit exceeded"""
    pass

class PaymentRequiredError(AgentMindError):
    """Payment required - need to upgrade plan"""
    pass

class ServerError(AgentMindError):
    """Server-side error"""
    pass