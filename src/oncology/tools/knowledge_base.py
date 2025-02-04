"""
Knowledge Base Tool for Oncology System

This module provides tools for accessing and querying medical knowledge bases,
including clinical guidelines, literature, and drug information.
"""

import os
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional, List, Set
from dataclasses import dataclass
from datetime import datetime, timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class Evidence:
    """Data class for evidence information."""
    source: str
    citation: str
    level: str  # e.g., "1A", "2B"
    relevance: float
    timestamp: str

@dataclass
class Guideline:
    """Data class for clinical guidelines."""
    organization: str
    recommendation: str
    strength: str
    evidence_level: str
    last_updated: str

class KnowledgeBaseTool:
    """Tool for accessing medical knowledge bases."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize the knowledge base tool."""
        self.config = config
        self.sources = config.get('sources', ['medical_literature', 'clinical_guidelines', 'drug_database'])
        self.max_age_months = config.get('validation', {}).get('max_age_months', 12)
        
        # Initialize knowledge bases
        self._init_databases()
        logger.info("Knowledge base tool initialized")
    
    def _init_databases(self):
        """Initialize connections to knowledge bases."""
        # TODO: Initialize actual database connections
        # For now, we'll simulate database access
        self.databases = {
            'literature': self._mock_literature_db,
            'guidelines': self._mock_guidelines_db,
            'drugs': self._mock_drug_db
        }
    
    def __call__(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Query knowledge bases and return relevant information."""
        try:
            query_text = inputs.get('query')
            if not query_text:
                raise ValueError("Query text not provided")
            
            # Get context from inputs
            context = {
                'findings': inputs.get('findings', []),
                'measurements': inputs.get('measurements', {}),
                'conditions': inputs.get('conditions', [])
            }
            
            # Search knowledge bases
            results = self._search_knowledge_bases(query_text, context)
            
            # Validate results
            if not self._validate_results(results):
                raise ValueError("Search results failed validation")
            
            return results
            
        except Exception as e:
            logger.error(f"Knowledge base query failed: {str(e)}")
            raise
    
    def _search_knowledge_bases(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Search across multiple knowledge bases."""
        # Search literature
        literature = self.databases['literature'](query, context)
        
        # Search guidelines
        guidelines = self.databases['guidelines'](query, context)
        
        # Search drug database
        drug_info = self.databases['drugs'](query, context)
        
        # Combine and rank results
        evidence = self._combine_evidence(literature, guidelines)
        
        return {
            'evidence': evidence,
            'guidelines': guidelines.get('guidelines', []),
            'drug_interactions': drug_info.get('interactions', []),
            'references': literature.get('references', []),
            'validation_passed': True
        }
    
    def _combine_evidence(self, literature: Dict[str, Any], guidelines: Dict[str, Any]) -> List[Evidence]:
        """Combine and rank evidence from multiple sources."""
        evidence_list = []
        
        # Add literature evidence
        for ref in literature.get('references', []):
            evidence_list.append(Evidence(
                source="literature",
                citation=ref['citation'],
                level=ref['evidence_level'],
                relevance=ref['relevance'],
                timestamp=ref['publication_date']
            ))
        
        # Add guideline evidence
        for guide in guidelines.get('guidelines', []):
            evidence_list.append(Evidence(
                source="guideline",
                citation=f"{guide['organization']} Guidelines",
                level=guide['evidence_level'],
                relevance=guide['relevance'],
                timestamp=guide['last_updated']
            ))
        
        # Sort by relevance and evidence level
        evidence_list.sort(key=lambda x: (x.relevance, x.level), reverse=True)
        
        return evidence_list
    
    def _validate_results(self, results: Dict[str, Any]) -> bool:
        """Validate search results."""
        if not results.get('evidence'):
            return False
        
        # Check evidence age
        for evidence in results['evidence']:
            evidence_date = datetime.fromisoformat(evidence.timestamp.split('T')[0])
            age_months = (datetime.now() - evidence_date).days / 30
            if age_months > self.max_age_months:
                logger.warning(f"Evidence too old: {evidence.citation}")
                return False
        
        return True
    
    # Mock database methods for testing
    def _mock_literature_db(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock literature database."""
        return {
            'references': [
                {
                    'citation': 'Smith et al. (2023) Lung Cancer Detection',
                    'evidence_level': '1A',
                    'relevance': 0.95,
                    'publication_date': '2023-12-01'
                },
                {
                    'citation': 'Johnson et al. (2023) Imaging Biomarkers',
                    'evidence_level': '2B',
                    'relevance': 0.85,
                    'publication_date': '2023-10-15'
                }
            ]
        }
    
    def _mock_guidelines_db(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock guidelines database."""
        return {
            'guidelines': [
                {
                    'organization': 'NCCN',
                    'recommendation': 'PET/CT recommended for staging',
                    'strength': 'Strong',
                    'evidence_level': '1',
                    'last_updated': '2024-01-15',
                    'relevance': 0.92
                }
            ]
        }
    
    def _mock_drug_db(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Mock drug database."""
        return {
            'interactions': [
                {
                    'drug_name': 'Example Drug',
                    'mechanism': 'Example mechanism',
                    'severity': 'moderate',
                    'evidence_level': '2B'
                }
            ]
        }

if __name__ == '__main__':
    # Example usage
    config = {
        'sources': ['medical_literature', 'clinical_guidelines', 'drug_database'],
        'validation': {
            'max_age_months': 12
        }
    }
    
    kb = KnowledgeBaseTool(config)
    
    test_input = {
        'query': 'lung mass treatment guidelines',
        'findings': ['spiculated mass', 'right upper lobe'],
        'measurements': {'size': '2.5cm'},
        'conditions': ['suspicious for malignancy']
    }
    
    try:
        result = kb(test_input)
        print(f"Search result: {json.dumps(result, default=str, indent=2)}")
    except Exception as e:
        print(f"Search failed: {str(e)}")