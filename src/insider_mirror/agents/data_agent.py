"""Data agent for fetching and validating insider trading data."""

import os
import aiohttp
import asyncio
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

from .base_agent import BaseAgent

class DataAgent(BaseAgent):
    """Agent responsible for data acquisition and validation"""
    
    def __init__(self, agent_config: Dict[str, Any]):
        self.name = "data_agent"  # Set name before super().__init__
        super().__init__(self.name, agent_config)
        self.tasks_config = self.load_config("src/insider_mirror/config/tasks.yaml")
        self.session = None

    async def _init_session(self) -> None:
        """Initialize aiohttp session"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()

    async def _close_session(self) -> None:
        """Close aiohttp session"""
        if self.session and not self.session.closed:
            await self.session.close()

    async def fetch_data(
        self,
        api_key: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Fetch data from API"""
        if not api_key or not endpoint:
            raise ValueError("API key and endpoint are required")
            
        await self._init_session()
        
        headers = {
            "X-Finnhub-Token": api_key,
            "Content-Type": "application/json"
        }
        
        try:
            async with self.session.get(endpoint, headers=headers, params=params) as response:
                response.raise_for_status()
                return await response.json()
                
        except aiohttp.ClientError as e:
            self.log.error(f"API request failed: {str(e)}")
            raise

    def validate_data(self, data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Validate fetched data"""
        if not isinstance(data, list):
            self.log.error("Invalid data format: expected list")
            return []
            
        required_fields = {
            "symbol": str,
            "transaction_type": str,
            "shares": (int, float),
            "price": float,
            "value": float,
            "filing_date": str
        }
        
        valid_records = []
        for record in data:
            try:
                # Check required fields and types
                if not all(
                    field in record and isinstance(record[field], field_type)
                    for field, field_type in required_fields.items()
                ):
                    continue
                    
                # Additional validation rules
                if record["shares"] <= 0 or record["price"] <= 0:
                    continue
                    
                if record["value"] != record["shares"] * record["price"]:
                    continue
                    
                # Validate date format
                try:
                    datetime.fromisoformat(record["filing_date"].replace('Z', '+00:00'))
                except ValueError:
                    continue
                    
                valid_records.append(record)
                
            except Exception as e:
                self.log.error(f"Record validation failed: {str(e)}")
                continue
                
        return valid_records

    async def execute(
        self,
        api_key: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute data agent tasks"""
        try:
            self.track_progress(1, "Initiating API request")
            
            # Fetch data
            data = await self.fetch_data(api_key, endpoint, params)
            self.track_progress(2, f"Retrieved {len(data)} records")
            
            # Validate data
            valid_data = self.validate_data(data)
            self.track_progress(3, f"Validated {len(valid_data)} records")
            
            return {
                "status": "success",
                "data": valid_data,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error executing data agent: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def cleanup(self) -> None:
        """Clean up resources"""
        super().cleanup()
        if self.session:
            asyncio.create_task(self._close_session())