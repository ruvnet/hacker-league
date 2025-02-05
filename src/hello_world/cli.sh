#!/bin/bash

# Text colors
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to display the header
show_header() {
    clear
    echo -e "${BLUE}╔══════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${BLUE}║                   Medical Analysis System CLI                     ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to display advanced analysis menu
show_advanced_menu() {
    show_header
    echo -e "${GREEN}Advanced Analysis Cases:${NC}"
    echo "1. Pathway Analysis (Treatment-Resistant Melanoma)"
    echo "2. Immunotherapy Response Prediction (NSCLC)"
    echo "3. Neurodegenerative Disease Analysis"
    echo "4. Rare Disease Multi-omic Analysis"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to handle advanced analysis cases
handle_advanced_case() {
    case $1 in
        1) "$SCRIPT_DIR/scripts/pathway_analysis_case.sh" ;;
        2) "$SCRIPT_DIR/scripts/immunotherapy_prediction_case.sh" ;;
        3) "$SCRIPT_DIR/scripts/neuro_analysis_case.sh" ;;
        4) "$SCRIPT_DIR/scripts/rare_disease_analysis_case.sh" ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to display the main menu
show_main_menu() {
    echo -e "${GREEN}Main Menu:${NC}"
    echo "1. General Medical Cases"
    echo "2. Oncology Cases"
    echo "3. Advanced Analysis Cases"
    echo "4. System Configuration"
    echo "5. Run All Cases"
    echo "6. Help"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to display general medical cases menu
show_medical_menu() {
    show_header
    echo -e "${GREEN}General Medical Cases:${NC}"
    echo "1. Simple Case (Headache Assessment)"
    echo "2. Moderate Case (Diabetic Complications)"
    echo "3. Complex Case (Multi-system Trauma)"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to display oncology cases menu
show_oncology_menu() {
    show_header
    echo -e "${GREEN}Oncology Cases:${NC}"
    echo "1. Imaging Analysis (Lung Mass)"
    echo "2. Genomic Analysis (Breast Cancer)"
    echo "3. Multi-modal Analysis (Comprehensive Workup)"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to display system configuration menu
show_config_menu() {
    show_header
    echo -e "${GREEN}System Configuration:${NC}"
    echo "1. View Current Configuration"
    echo "2. Edit Agent Settings"
    echo "3. Edit Task Settings"
    echo "4. Edit Analysis Settings"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Function to handle general medical cases
handle_medical_case() {
    case $1 in
        1) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "Patient presents with moderate headache for 2 days, no other symptoms. No history of migraines." --task both ;;
        2) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "65-year-old diabetic patient presents with fatigue, polyuria, polydipsia for 1 week. Blood glucose reading at home was 385 mg/dL. History of hypertension and peripheral neuropathy." --task both ;;
        3) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "22-year-old trauma patient from MVA. Multiple injuries including closed head trauma (GCS 12), chest wall contusion, suspected internal bleeding. BP 90/60, HR 130, RR 28, O2 sat 88%. Positive seat belt sign, complaining of severe abdominal pain. Multiple lacerations and right femur deformity noted." --task both ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to handle oncology cases
handle_oncology_case() {
    case $1 in
        1) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "Patient presents with suspicious mass on chest CT. 3cm lesion in right upper lobe with spiculated margins. Previous imaging from 6 months ago showed 1.5cm nodule. Recent weight loss and fatigue. Former smoker with 30 pack-year history. Family history of lung cancer in father." --task both ;;
        2) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "Patient with newly diagnosed breast cancer. Tumor sequencing reveals BRCA1 mutation (c.181T>G), PIK3CA mutation, and elevated HER2 expression. 45-year-old female, premenopausal, no previous cancer history. Mother and sister with history of ovarian cancer. Tumor size 2.5cm, grade 3, triple-negative on IHC." --task both ;;
        3) cd "$SCRIPT_DIR" && python -m hello_world.main --prompt "Patient undergoing comprehensive cancer workup. PET-CT shows hypermetabolic lesions in liver (SUV 8.5) and multiple bone metastases. Liver biopsy reveals poorly differentiated adenocarcinoma, CK7+/CK20-, TTF1+. NGS panel shows EGFR exon 19 deletion and TP53 mutation. Previous chest CT from 3 months ago showed 4.2cm right lower lobe mass. 58-year-old Asian female, never-smoker, with progressive fatigue and 15-pound weight loss over 2 months." --task both ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to handle system configuration
handle_config() {
    case $1 in
        1) cat "$SCRIPT_DIR/config/agents.yaml" && cat "$SCRIPT_DIR/config/tasks.yaml" && cat "$SCRIPT_DIR/config/analysis.yaml" ;;
        2) ${EDITOR:-vi} "$SCRIPT_DIR/config/agents.yaml" ;;
        3) ${EDITOR:-vi} "$SCRIPT_DIR/config/tasks.yaml" ;;
        4) ${EDITOR:-vi} "$SCRIPT_DIR/config/analysis.yaml" ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to show help
show_help() {
    show_header
    echo -e "${GREEN}Help:${NC}"
    echo "This CLI provides access to various medical analysis scenarios and system configuration options."
    echo ""
    echo "Available Categories:"
    echo "1. General Medical Cases - Basic to complex medical scenarios"
    echo "2. Oncology Cases - Specialized cancer-related analyses"
    echo "3. Advanced Analysis Cases - Cutting-edge multi-modal analyses"
    echo "4. System Configuration - View and edit system settings"
    echo "5. Run All Cases - Execute all available test cases"
    echo ""
    echo "Navigation:"
    echo "- Use numbers to select options"
    echo "- Use 'b' to go back to previous menu"
    echo "- Use 'q' to quit the program"
    echo ""
    echo -e "${YELLOW}Press Enter to continue...${NC}"
    read
}

# Main program loop
while true; do
    show_header
    show_main_menu
    read -r choice

    case $choice in
        1)  while true; do
                show_medical_menu
                read -r subchoice
                case $subchoice in
                    [1-3]) handle_medical_case $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        2)  while true; do
                show_oncology_menu
                read -r subchoice
                case $subchoice in
                    [1-3]) handle_oncology_case $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        3)  while true; do
                show_advanced_menu
                read -r subchoice
                case $subchoice in
                    [1-4]) handle_advanced_case $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        4)  while true; do
                show_config_menu
                read -r subchoice
                case $subchoice in
                    [1-4]) handle_config $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        5)  "$SCRIPT_DIR/scripts/run_all_cases.sh"
            echo -e "\n${YELLOW}Press Enter to continue...${NC}"
            read
            ;;
        6)  show_help ;;
        q|Q) exit 0 ;;
        *) echo -e "${RED}Invalid option${NC}" ;;
    esac
done
