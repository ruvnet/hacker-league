#!/usr/bin/env python3
"""
Medical Knowledge Processing Agent using ReAct Architecture

This agent processes medical documents and knowledge using a ReAct approach:
1. Observation: Extract information from medical documents
2. Thought: Analyze and validate against medical knowledge
3. Action: Update knowledge base or request clarification
"""

import json
import yaml
from pathlib import Path

# ANSI color codes for clinical formatting
class Colors:
    HEADER = '\033[95m'      # Purple for headers
    ALERT = '\033[91m'       # Red for alerts/warnings
    SUCCESS = '\033[92m'     # Green for success
    INFO = '\033[94m'        # Blue for info
    EMPHASIS = '\033[93m'    # Yellow for emphasis
    ENDC = '\033[0m'         # End color
    BOLD = '\033[1m'         # Bold text
    UNDERLINE = '\033[4m'    # Underlined text

# Clinical emojis
class Emojis:
    DOCUMENT = "📄"          # Medical document
    WARNING = "⚠️"           # Warning/Alert
    SUCCESS = "✅"           # Success/Validated
    ERROR = "❌"             # Error/Failed
    INFO = "i️"             # Information
    DRUG = "💊"             # Medication
    LAB = "🔬"              # Laboratory/Research
    CLOCK = "⏱️"            # Time/Duration
    CHART = "📊"            # Data/Statistics
    LINK = "🔗"             # Reference/Link

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MedicalEntity:
    """Medical concept with standardized coding"""
    id: str
    name: str
    type: str  # disease, drug, gene, etc.
    codes: Dict[str, str]  # SNOMED, ICD, etc.
    evidence: List[str]  # references supporting this entity

@dataclass
class ClinicalGuideline:
    """Represents a clinical guideline or rule"""
    id: str
    condition: str
    recommendation: str
    evidence_level: str  # A, B, C, etc.
    source: str
    last_updated: datetime

class Tool:
    """Base class for medical knowledge tools"""
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
    
    def __call__(self, *args, **kwargs) -> Dict[str, Any]:
        raise NotImplementedError

class DrugLabelTool(Tool):
    """Process drug labels and package inserts"""
    def __init__(self):
        super().__init__(
            name="drug_label_processor",
            description="Extract structured info from drug labels"
        )
    
    def __call__(self, xml_path: str) -> Dict[str, Any]:
        try:
            # Parse drug label XML
            import xml.etree.ElementTree as ET
            tree = ET.parse(xml_path)
            root = tree.getroot()
            
            # Extract key sections
            data = {
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
                'data': data,
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class GuidelineTool(Tool):
    """Process clinical guidelines"""
    def __init__(self):
        super().__init__(
            name="guideline_processor",
            description="Extract rules from clinical guidelines"
        )
    
    def __call__(self, text: str) -> Dict[str, Any]:
        try:
            # Extract structured info from guideline text
            # In real system: Use NLP to identify conditions, recommendations
            # For demo: Simple rule extraction
            import re
            
            # Look for patterns like "If X, then Y"
            rules = []
            if_then_patterns = re.finditer(
                r"(?i)if\s+([^,\.]+),?\s+then\s+([^\.]+)",
                text
            )
            
            for match in if_then_patterns:
                condition = match.group(1).strip()
                action = match.group(2).strip()
                rules.append({
                    'condition': condition,
                    'recommendation': action
                })
            
            # Look for evidence levels
            evidence_pattern = re.compile(
                r"(?i)evidence\s+(?:level|grade)\s*[:=]?\s*([A-D])",
            )
            evidence_match = evidence_pattern.search(text)
            evidence_level = evidence_match.group(1) if evidence_match else None
            
            return {
                'success': True,
                'data': {
                    'rules': rules,
                    'evidence_level': evidence_level
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class TrialResultsTool(Tool):
    """Process clinical trial results"""
    def __init__(self):
        super().__init__(
            name="trial_processor",
            description="Extract outcomes from trial results"
        )
    
    def __call__(self, data: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # Process trial data
            # Extract p-values, confidence intervals, etc.
            outcomes = []
            for outcome in data.get('outcomes', []):
                processed = {
                    'measure': outcome.get('measure'),
                    'result': outcome.get('result'),
                    'p_value': outcome.get('p_value'),
                    'confidence_interval': outcome.get('ci')
                }
                outcomes.append(processed)
            
            return {
                'success': True,
                'data': {
                    'trial_id': data.get('id'),
                    'outcomes': outcomes,
                    'significance': any(
                        o.get('p_value', 1.0) < 0.05 
                        for o in outcomes
                    )
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }

class KnowledgeValidationTool(Tool):
    """Validate extracted knowledge against existing rules"""
    def __init__(self):
        super().__init__(
            name="knowledge_validator",
            description="Check consistency with medical knowledge"
        )
    
    def __call__(self, 
                 new_knowledge: Dict[str, Any],
                 existing_rules: List[Dict[str, Any]]) -> Dict[str, Any]:
        try:
            conflicts = []
            supports = []
            
            # Check each piece of new knowledge against rules
            for rule in existing_rules:
                if self._conflicts_with_rule(new_knowledge, rule):
                    conflicts.append({
                        'rule': rule,
                        'conflict_reason': 'Contradicts existing knowledge'
                    })
                if self._supports_rule(new_knowledge, rule):
                    supports.append({
                        'rule': rule,
                        'support_type': 'Provides additional evidence'
                    })
            
            return {
                'success': True,
                'data': {
                    'conflicts': conflicts,
                    'supporting_evidence': supports,
                    'is_valid': len(conflicts) == 0
                },
                'error': None
            }
        except Exception as e:
            return {
                'success': False,
                'data': None,
                'error': str(e)
            }
    
    def _conflicts_with_rule(self, 
                           knowledge: Dict[str, Any], 
                           rule: Dict[str, Any]) -> bool:
        """Check if new knowledge conflicts with a rule"""
        # Implement conflict detection logic
        # For example, if knowledge contradicts rule conditions
        return False  # Placeholder
    
    def _supports_rule(self,
                      knowledge: Dict[str, Any],
                      rule: Dict[str, Any]) -> bool:
        """Check if new knowledge supports a rule"""
        # Implement support detection logic
        # For example, if knowledge provides evidence for rule
        return False  # Placeholder

@dataclass
class AgentState:
    """State of the medical knowledge agent"""
    documents_processed: List[str]
    extracted_knowledge: List[Dict[str, Any]]
    validation_results: List[Dict[str, Any]]
    status: str

class MedicalKnowledgeAgent:
    """ReAct-style agent for processing medical knowledge"""
    
    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Initialize tools
        self.tools = {
            'drug_label': DrugLabelTool(),
            'guideline': GuidelineTool(),
            'trial': TrialResultsTool(),
            'validator': KnowledgeValidationTool()
        }
        
        # Initialize state
        self.state = AgentState(
            documents_processed=[],
            extracted_knowledge=[],
            validation_results=[],
            status='initialized'
        )
    
    def process_document(self, doc_path: str, doc_type: str) -> str:
        """Process a medical document"""
        self.state.status = 'processing'
        
        # Step 1: Extract information using appropriate tool
        print(f"\nProcessing {doc_type} document: {doc_path}")
        
        if doc_type == 'drug_label':
            result = self.tools['drug_label'](doc_path)
        elif doc_type == 'guideline':
            with open(doc_path) as f:
                result = self.tools['guideline'](f.read())
        elif doc_type == 'trial':
            with open(doc_path) as f:
                result = self.tools['trial'](json.load(f))
        else:
            return f"Unsupported document type: {doc_type}"
        
        if not result['success']:
            return f"Error processing document: {result['error']}"
        
        # Step 2: Validate against existing knowledge
        print("\nValidating extracted knowledge...")
        validation = self.tools['validator'](
            result['data'],
            self.state.extracted_knowledge
        )
        
        if not validation['success']:
            return f"Error validating knowledge: {validation['error']}"
        
        # Step 3: Update state based on validation
        if validation['data']['is_valid']:
            self.state.documents_processed.append(doc_path)
            self.state.extracted_knowledge.append(result['data'])
            self.state.validation_results.append(validation['data'])
            print("\nKnowledge successfully integrated")
        else:
            conflicts = validation['data']['conflicts']
            print("\nFound conflicts with existing knowledge:")
            for conflict in conflicts:
                print(f"- {conflict['conflict_reason']}")
        
        # Return processing summary
        return self._format_result(result['data'], validation['data'])
    
    def _format_result(self, 
                      extracted: Dict[str, Any],
                      validation: Dict[str, Any]) -> str:
        """Format processing results with clinical styling"""
        header = f"""
{Colors.HEADER}{Colors.BOLD}╔══════════════════════════════════════════════════════════════════╗
║                    CLINICAL DOCUMENT ANALYSIS                     ║
╚══════════════════════════════════════════════════════════════════╝{Colors.ENDC}
"""
        sections = []
        
        # Document Information
        if 'name' in extracted:
            sections.append(f"""
{Colors.INFO}{Emojis.DOCUMENT} Document Type: Drug Label
{Emojis.DRUG} Drug Name: {Colors.EMPHASIS}{extracted['name']}{Colors.ENDC}
{Emojis.CLOCK} Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{Colors.ENDC}
""")
        
        # Clinical Indications
        if 'indications' in extracted:
            sections.append(f"""
{Colors.INFO}{Colors.BOLD}THERAPEUTIC INDICATIONS:{Colors.ENDC}
""" + "\n".join(f"{Colors.SUCCESS}• {ind}{Colors.ENDC}" 
                for ind in extracted['indications']))
        
        # Validation Status
        if validation['is_valid']:
            sections.append(f"""
{Colors.SUCCESS}{Colors.BOLD}VALIDATION STATUS:{Colors.ENDC}
{Emojis.SUCCESS} Document successfully processed and validated
{Emojis.LINK} Knowledge base updated
{Emojis.CHART} Ready for clinical reference""")
            if validation['supporting_evidence']:
                sections.append(f"{Colors.INFO}Supporting Evidence:{Colors.ENDC}")
                for evidence in validation['supporting_evidence']:
                    sections.append(f"{Colors.INFO}• {evidence['support_type']}{Colors.ENDC}")
        else:
            sections.append(f"""
{Colors.ALERT}{Colors.BOLD}VALIDATION STATUS:{Colors.ENDC}
{Emojis.WARNING} Conflicts detected:""")
            for conflict in validation['conflicts']:
                sections.append(f"{Colors.ALERT}• {conflict['conflict_reason']}{Colors.ENDC}")
        
        footer = f"""
{Colors.HEADER}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{Colors.ENDC}
"""
        
        return header + "\n".join(sections) + footer

    
    def export_knowledge_base(self) -> None:
        """Export processed knowledge to files"""
        # Export extracted knowledge
        knowledge_file = self.output_dir / 'knowledge_base.json'
        with knowledge_file.open('w') as f:
            json.dump({
                'documents': self.state.documents_processed,
                'knowledge': self.state.extracted_knowledge,
                'validations': self.state.validation_results,
                'timestamp': datetime.now().isoformat()
            }, f, indent=2)
        
        print(f"\nExported knowledge base to {knowledge_file}")

def main():
    # Initialize agent
    agent = MedicalKnowledgeAgent(Path('data/knowledge_base'))
    
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*70}")
    print(f"Medical Knowledge Processing System")
    print(f"{'='*70}{Colors.ENDC}")
    
    # Process example documents
    docs = [
        ('data/knowledge_base/drug_labels/example_label.xml', 'drug_label'),
    ]
    
    for path, doc_type in docs:
        if Path(path).exists():
            print(f"\n{Colors.INFO}{Emojis.DOCUMENT} Processing {doc_type}...{Colors.ENDC}")
            print(agent.process_document(path, doc_type))
    
    # Export final knowledge base
    print(f"\n{Colors.INFO}{Emojis.CHART} Exporting knowledge base...{Colors.ENDC}")
    agent.export_knowledge_base()

if __name__ == '__main__':
    main()