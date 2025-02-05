#!/bin/bash

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
HELLO_WORLD_DIR="$( cd "$SCRIPT_DIR/.." && pwd )"

# Advanced case: Neurodegenerative disease analysis with multi-modal brain imaging
echo "Running advanced neurodegenerative analysis case..."
cd "$HELLO_WORLD_DIR" && python -m hello_world.main --prompt "Complex neurodegenerative case analysis. 68-year-old patient with progressive cognitive decline. Brain MRI volumetrics show hippocampal atrophy (volume below 5th percentile) and cortical thinning in temporal and parietal regions. FDG-PET reveals characteristic hypometabolism pattern. Amyloid-PET positive with high retention in precuneus and posterior cingulate. Tau-PET shows Braak stage 4 pattern. CSF analysis: decreased Aβ42 (350 pg/mL), elevated p-tau (85 pg/mL), elevated t-tau (450 pg/mL). Blood-based biomarkers: elevated plasma NfL (35 pg/mL), positive plasma p-tau181. Longitudinal cognitive scores: MMSE decline from 28 to 23 over 18 months, progressive impairment in delayed recall and executive function. Digital biomarkers from smartphone interactions show declining processing speed. Polygenic risk score in 95th percentile. Whole genome sequencing reveals APOE ε4 homozygous, TREM2 R47H variant. Sleep EEG shows disrupted slow-wave patterns. Retinal imaging demonstrates reduced vessel density and increased amyloid deposits. Gait analysis indicates early balance impairment. Microbiome analysis suggests altered gut-brain axis signaling." --task both
