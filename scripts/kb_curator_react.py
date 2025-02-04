#!/usr/bin/env python3
"""
Knowledge Base Curator with ReAct-style Tools

This script uses a ReAct-inspired architecture to curate medical knowledge from:
- Drug labels (FDA structured product labels)
- Clinical guidelines
- Clinical trial results
- Medical publications
"""

import json
import yaml
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MedicalEntity:
    """Represents a medical concept/entity"""
    id: str
    name: str
    type: str  # drug, disease, gene, etc.
    synonyms: List[str]
    codes: Dict[str, str]  # coding system -> code (SNOMED, ICD, etc.)

@dataclass
class ClinicalEvidence:
    """Represents clinical evidence from literature"""
    source_id: str
    source_type: str  # trial, publication, guideline
    evidence_level: str  # A, B, C, etc.
    strength: str  # strong, moderate, weak
    finding: str
    date_added: datetime

class Tool:
    """Base class for curation tools"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __call__(self, *args, **kwargs) -> str:
        raise NotImplementedError

class DrugLabelTool(Tool):
    """Tool for processing drug labels"""
    def __init__(self):
        super().__init__(
            name="drug_label_processor",
            description="Process structured product label XML"
        )
    
    def __call__(self, xml_path: Path) -> Dict[str, Any]:
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract drug information
            drug_info = {
                'name': root.find('name').text,
                'indications': [
                    ind.text for ind in root.findall('.//indication')
                ],
                'contraindications': [
                    contra.text for contra in root.findall('.//contraindication')
                ],
                'adverse_reactions': [
                    {
                        'reaction': react.text,
                        'severity': react.get('severity')
                    }
                    for react in root.findall('.//reaction')
                ]
            }
            
            return {
                'success': True,
                'data': drug_info,
                'error': None
            }
            
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class GuidelineTool(Tool):
    """Tool for processing clinical guidelines"""
    def __init__(self):
        super().__init__(
            name="guideline_processor",
            description="Process clinical guideline documents"
        )
    
    def __call__(self, text: str) -> Dict[str, Any]:
        # In real system: Use NLP to extract recommendations
        # For demo: Return structured format
        return {
            'success': True,
            'data': {
                'recommendations': [
                    {
                        'text': 'Example recommendation',
                        'evidence_level': 'A',
                        'strength': 'strong'
                    }
                ]
            },
            'error': None
        }

class TrialResultsTool(Tool):
    """Tool for processing clinical trial results"""
    def __init__(self):
        super().__init__(
            name="trial_processor",
            description="Process clinical trial results"
        )
    
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # In real system: Process trial data
        # For demo: Return structured format
        return {
            'success': True,
            'data': {
                'outcomes': [
                    {
                        'measure': 'Example outcome',
                        'result': 'Positive',
                        'p_value': 0.001
                    }
                ]
            },
            'error': None
        }

class PublicationTool(Tool):
    """Tool for processing medical publications"""
    def __init__(self):
        super().__init__(
            name="publication_processor",
            description="Process medical publications"
        )
    
    def __call__(self, pubmed_id: str) -> Dict[str, Any]:
        # In real system: Use PubMed API
        # For demo: Return structured format
        return {
            'success': True,
            'data': {
                'findings': [
                    {
                        'text': 'Example finding',
                        'confidence': 'high'
                    }
                ]
            },
            'error': None
        }

class KnowledgeBaseCurator:
    """ReAct-style orchestrator for knowledge curation"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize knowledge stores
        self.entities: Dict[str, MedicalEntity] = {}
        self.relations: List[Dict[str, Any]] = []
        self.evidence: Dict[str, List[ClinicalEvidence]] = {}
        
        # Initialize tools
        self.tools = {
            'drug_label': DrugLabelTool(),
            'guideline': GuidelineTool(),
            'trial': TrialResultsTool(),
            'publication': PublicationTool()
        }
    
    def process_drug_label(self, label_path: Path) -> str:
        """Process drug label XML"""
        print(f"Processing drug label: {label_path}")
        result = self.tools['drug_label'](label_path)
        
        if result['success']:
            drug_info = result['data']
            
            # Create drug entity
            drug = MedicalEntity(
                id=f"DRUG_{len(self.entities)}",
                name=drug_info['name'],
                type='drug',
                synonyms=[],
                codes={}
            )
            self.entities[drug.id] = drug
            
            # Add indications as relations
            for indication in drug_info['indications']:
                self.relations.append({
                    'source': drug.id,
                    'relation': 'treats',
                    'target': indication
                })
            
            return f"Successfully processed drug label: {drug_info['name']}"
        else:
            return f"Error processing drug label: {result['error']}"
    
    def process_guideline(self, guideline_path: Path) -> str:
        """Process clinical guideline"""
        print(f"Processing guideline: {guideline_path}")
        
        # In real system: Read and parse guideline
        # For demo: Use dummy text
        result = self.tools['guideline']("Example guideline text")
        
        if result['success']:
            recommendations = result['data']['recommendations']
            return f"Successfully processed guideline: {len(recommendations)} recommendations"
        else:
            return f"Error processing guideline: {result['error']}"
    
    def process_trial(self, trial_data: Dict[str, Any]) -> str:
        """Process clinical trial results"""
        print(f"Processing trial results")
        result = self.tools['trial'](trial_data)
        
        if result['success']:
            outcomes = result['data']['outcomes']
            return f"Successfully processed trial: {len(outcomes)} outcomes"
        else:
            return f"Error processing trial: {result['error']}"
    
    def process_publication(self, pubmed_id: str) -> str:
        """Process medical publication"""
        print(f"Processing publication: {pubmed_id}")
        result = self.tools['publication'](pubmed_id)
        
        if result['success']:
            findings = result['data']['findings']
            return f"Successfully processed publication: {len(findings)} findings"
        else:
            return f"Error processing publication: {result['error']}"
    
    def export_knowledge_base(self) -> None:
        """Export curated knowledge to files"""
        # Export entities
        entities_file = self.output_dir / 'entities.json'
        with entities_file.open('w') as f:
            json.dump({id: vars(e) for id, e in self.entities.items()}, 
                     f, indent=2, default=str)
        
        # Export relations with evidence
        relations_file = self.output_dir / 'relations.json'
        with relations_file.open('w') as f:
            json.dump(self.relations, f, indent=2, default=str)
            
        print(f"Exported knowledge base to {self.output_dir}")

def main():
    # Initialize curator
    curator = KnowledgeBaseCurator(Path('data/knowledge_base'))
    
    # Process drug label
    label_path = Path('data/knowledge_base/drug_labels/example_label.xml')
    if label_path.exists():
        print("\nProcessing Drug Label:")
        print(curator.process_drug_label(label_path))
    
    # Process guideline
    print("\nProcessing Guideline:")
    print(curator.process_guideline(Path('dummy/path')))
    
    # Process trial
    print("\nProcessing Trial:")
    trial_data = {
        'id': 'TRIAL123',
        'intervention': 'Example Drug',
        'outcome': 'Positive'
    }
    print(curator.process_trial(trial_data))
    
    # Process publication
    print("\nProcessing Publication:")
    print(curator.process_publication('PMID12345'))
    
    # Export knowledge base
    curator.export_knowledge_base()

if __name__ == '__main__':
    main()