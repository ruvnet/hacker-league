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
    echo -e "${BLUE}║               Beverage Product Development CLI                    ║${NC}"
    echo -e "${BLUE}╚══════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

# Function to display innovation cases menu
show_innovation_menu() {
    show_header
    echo -e "${GREEN}Product Innovation Cases:${NC}"
    echo "1. Health-Focused Beverage Development"
    echo "2. Plant-Based Alternative Analysis"
    echo "3. Functional Beverage Innovation"
    echo "4. Sustainable Packaging Design"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to handle innovation cases
handle_innovation_case() {
    case $1 in
        1) "$SCRIPT_DIR/scripts/health_focused_case.sh" ;;
        2) "$SCRIPT_DIR/scripts/plant_based_case.sh" ;;
        3) "$SCRIPT_DIR/scripts/functional_beverage_case.sh" ;;
        4) "$SCRIPT_DIR/scripts/sustainable_packaging_case.sh" ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to display the main menu
show_main_menu() {
    echo -e "${GREEN}Main Menu:${NC}"
    echo "1. Market Research Cases"
    echo "2. Product Development Cases"
    echo "3. Product Innovation Cases"
    echo "4. System Configuration"
    echo "5. Run All Cases"
    echo "6. Help"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to display market research cases menu
show_market_menu() {
    show_header
    echo -e "${GREEN}Market Research Cases:${NC}"
    echo "1. Consumer Trend Analysis"
    echo "2. Competitor Product Analysis"
    echo "3. Market Opportunity Assessment"
    echo "b. Back to Main Menu"
    echo "q. Quit"
    echo ""
    echo -n "Select an option: "
}

# Function to display product development cases menu
show_product_menu() {
    show_header
    echo -e "${GREEN}Product Development Cases:${NC}"
    echo "1. Flavor Profile Development"
    echo "2. Ingredient Optimization"
    echo "3. Quality Assessment"
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

# Function to handle market research cases
handle_market_case() {
    case $1 in
        1) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Analyze current consumer trends in non-alcoholic beverages, focusing on health-conscious millennials and Gen Z preferences." --task both ;;
        2) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Evaluate competitor landscape in premium non-alcoholic beverages, including product positioning, pricing, and unique selling propositions." --task both ;;
        3) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Identify market opportunities in the functional beverage segment, analyzing gaps in current offerings and potential for innovation." --task both ;;
    esac
    echo -e "\n${YELLOW}Press Enter to continue...${NC}"
    read
}

# Function to handle product development cases
handle_product_case() {
    case $1 in
        1) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Develop flavor profile for a new botanical-infused sparkling water, targeting sophisticated non-alcoholic alternatives. Consider seasonal ingredients and premium positioning." --task both ;;
        2) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Optimize ingredient selection for a natural energy drink, focusing on clean label ingredients and sustainable sourcing. Balance taste, functionality, and cost considerations." --task both ;;
        3) cd "$SCRIPT_DIR" && python -m beverages.main --prompt "Conduct quality assessment of new probiotic beverage formulation, evaluating stability, shelf life, and sensory characteristics. Ensure compliance with food safety standards." --task both ;;
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
    echo "This CLI provides access to various beverage product development scenarios and system configuration options."
    echo ""
    echo "Available Categories:"
    echo "1. Market Research Cases - Consumer trends and market analysis"
    echo "2. Product Development Cases - Formulation and quality assessment"
    echo "3. Product Innovation Cases - New product concepts and sustainability"
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
                show_market_menu
                read -r subchoice
                case $subchoice in
                    [1-3]) handle_market_case $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        2)  while true; do
                show_product_menu
                read -r subchoice
                case $subchoice in
                    [1-3]) handle_product_case $subchoice ;;
                    b|B) break ;;
                    q|Q) exit 0 ;;
                    *) echo -e "${RED}Invalid option${NC}" ;;
                esac
            done
            ;;
        3)  while true; do
                show_innovation_menu
                read -r subchoice
                case $subchoice in
                    [1-4]) handle_innovation_case $subchoice ;;
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
