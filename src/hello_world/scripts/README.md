# Medical Case Analysis Scripts

This directory contains a collection of example scripts demonstrating the medical analysis capabilities of the system across different complexity levels and specialties.

## General Medical Cases

### 1. Simple Case (`simple_case.sh`)
- Basic headache assessment
- Demonstrates initial triage and basic diagnostic workflow
- Suitable for straightforward, single-symptom presentations

### 2. Moderate Case (`moderate_case.sh`)
- Diabetic patient with multiple symptoms
- Shows management of chronic conditions with acute complications
- Demonstrates integration of multiple diagnostic factors

### 3. Complex Case (`complex_case.sh`)
- Multi-system trauma from motor vehicle accident
- Illustrates handling of critical care scenarios
- Demonstrates coordination across multiple medical specialties

## Oncology Cases

### 4. Oncology Imaging Case (`oncology_image_case.sh`)
- Suspicious lung mass analysis
- Demonstrates radiological assessment and interpretation
- Includes temporal comparison and risk factor analysis

### 5. Genomic Analysis Case (`genomic_analysis_case.sh`)
- Breast cancer molecular profiling
- Shows integration of genetic testing results
- Includes hereditary cancer risk assessment
- Demonstrates precision medicine approach

### 6. Multi-modal Oncology Case (`multimodal_oncology_case.sh`)
- Comprehensive cancer workup
- Integrates imaging, pathology, and genomic data
- Demonstrates advanced staging and treatment planning
- Shows correlation of multiple diagnostic modalities

### 7. Run All Cases (`run_all_cases.sh`)
- Master script to execute all example cases
- Runs both general medical and oncology cases
- Provides comprehensive demonstration of system capabilities
- Useful for testing and validation

## Usage

1. Ensure all scripts have executable permissions:
```bash
chmod +x *.sh
```

2. Run individual cases:
```bash
./simple_case.sh
./moderate_case.sh
./complex_case.sh
./oncology_image_case.sh
./genomic_analysis_case.sh
./multimodal_oncology_case.sh
```

3. Run all cases:
```bash
./run_all_cases.sh
```

## Output

Each script will generate a detailed medical analysis including:
- Emergency triage assessment
- Comprehensive diagnostic evaluation
- Laboratory analysis
- Imaging interpretation
- Specialist consultation
- Treatment planning
- Multi-disciplinary review

### Additional Oncology-Specific Output
- Radiological measurements and temporal comparisons
- Molecular diagnostic interpretations
- Genomic variant analysis
- Cancer staging assessments
- Precision medicine recommendations
- Multi-disciplinary tumor board considerations

## Note

These scripts demonstrate the system's medical analysis capabilities across various scenarios, from basic assessments to complex oncology cases. Each case showcases different aspects of the medical workflow, integrating multiple data sources and specialties for comprehensive patient care.
