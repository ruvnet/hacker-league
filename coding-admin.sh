#!/bin/bash

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

CONFIG_FILE=".aider.conf.yml"

# ASCII Art Banner
show_banner() {
    clear
    echo -e "${GREEN}"
    echo "    _    _     _           _____             __ _       "
    echo "   / \  (_) __| | ___ _ __|  ___|_ _  ___  / _(_) __ _ "
    echo "  / _ \ | |/ _\` |/ _ \ '__| |_ / _\` |/ _ \| |_| |/ _\` |"
    echo " / ___ \| | (_| |  __/ |  |  _| (_| | (_) |  _| | (_| |"
    echo "/_/   \_\_|\__,_|\___|_|  |_|  \__,_|\___/|_| |_|\__, |"
    echo "                                                   |___/ "
    echo -e "${NC}"
    echo -e "${CYAN}[ Aider Configuration Management System ]${NC}"
    echo
}

# Initialize config file if it doesn't exist
init_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "# Aider Configuration File" > "$CONFIG_FILE"
        echo "# Created by coding-admin.sh" >> "$CONFIG_FILE"
        echo "" >> "$CONFIG_FILE"
    fi
}

# Update or add a setting in the YAML file
update_setting() {
    local key=$1
    local value=$2
    
    if grep -q "^$key:" "$CONFIG_FILE"; then
        sed -i "s|^$key:.*|$key: $value|" "$CONFIG_FILE"
    else
        echo "$key: $value" >> "$CONFIG_FILE"
    fi
}

# Get current value of a setting
get_setting() {
    local key=$1
    grep "^$key:" "$CONFIG_FILE" | cut -d':' -f2 | tr -d ' ' || echo ""
}

# Model Settings Menu
model_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Model Settings ===${NC}\n"
        echo -e "1) Set Main Model"
        echo -e "2) Set Editor Model"
        echo -e "3) Set Weak Model"
        echo -e "4) Toggle Model Warnings"
        echo -e "5) Set Max Chat History Tokens"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Available Models:${NC}"
                echo "1) gpt-4-1106-preview (4-turbo)"
                echo "2) gpt-4-0613 (4)"
                echo "3) gpt-3.5-turbo (35turbo)"
                echo "4) claude-3-opus-20240229 (opus)"
                echo -e "\n${CYAN}Select model:${NC} "
                read -r model_choice
                case $model_choice in
                    1) update_setting "model" "gpt-4-1106-preview";;
                    2) update_setting "model" "gpt-4-0613";;
                    3) update_setting "model" "gpt-3.5-turbo";;
                    4) update_setting "model" "claude-3-opus-20240229";;
                esac
                ;;
            2)
                echo -e "\n${CYAN}Enter editor model:${NC} "
                read -r editor_model
                update_setting "editor_model" "$editor_model"
                ;;
            3)
                echo -e "\n${CYAN}Enter weak model:${NC} "
                read -r weak_model
                update_setting "weak_model" "$weak_model"
                ;;
            4)
                current=$(get_setting "show_model_warnings")
                if [ "$current" = "false" ]; then
                    update_setting "show_model_warnings" "true"
                else
                    update_setting "show_model_warnings" "false"
                fi
                ;;
            5)
                echo -e "\n${CYAN}Enter max chat history tokens:${NC} "
                read -r tokens
                update_setting "max_chat_history_tokens" "$tokens"
                ;;
            0) return;;
        esac
    done
}

# Git Settings Menu
git_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Git Settings ===${NC}\n"
        echo -e "1) Toggle Auto Commits"
        echo -e "2) Toggle Dirty Commits"
        echo -e "3) Toggle Author Attribution"
        echo -e "4) Toggle Committer Attribution"
        echo -e "5) Set Commit Message Prefix"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                current=$(get_setting "auto_commits")
                if [ "$current" = "false" ]; then
                    update_setting "auto_commits" "true"
                else
                    update_setting "auto_commits" "false"
                fi
                ;;
            2)
                current=$(get_setting "dirty_commits")
                if [ "$current" = "false" ]; then
                    update_setting "dirty_commits" "true"
                else
                    update_setting "dirty_commits" "false"
                fi
                ;;
            3)
                current=$(get_setting "attribute_author")
                if [ "$current" = "false" ]; then
                    update_setting "attribute_author" "true"
                else
                    update_setting "attribute_author" "false"
                fi
                ;;
            4)
                current=$(get_setting "attribute_committer")
                if [ "$current" = "false" ]; then
                    update_setting "attribute_committer" "true"
                else
                    update_setting "attribute_committer" "false"
                fi
                ;;
            5)
                echo -e "\n${CYAN}Enter commit message prefix:${NC} "
                read -r prefix
                update_setting "commit_message_prefix" "$prefix"
                ;;
            0) return;;
        esac
    done
}

# Output Settings Menu
output_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Output Settings ===${NC}\n"
        echo -e "1) Toggle Dark Mode"
        echo -e "2) Toggle Pretty Output"
        echo -e "3) Toggle Streaming"
        echo -e "4) Set Code Theme"
        echo -e "5) Set Colors"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                current=$(get_setting "dark_mode")
                if [ "$current" = "false" ]; then
                    update_setting "dark_mode" "true"
                else
                    update_setting "dark_mode" "false"
                fi
                ;;
            2)
                current=$(get_setting "pretty")
                if [ "$current" = "false" ]; then
                    update_setting "pretty" "true"
                else
                    update_setting "pretty" "false"
                fi
                ;;
            3)
                current=$(get_setting "stream")
                if [ "$current" = "false" ]; then
                    update_setting "stream" "true"
                else
                    update_setting "stream" "false"
                fi
                ;;
            4)
                echo -e "\n${CYAN}Available Themes:${NC}"
                echo "1) default"
                echo "2) monokai"
                echo "3) solarized-dark"
                echo "4) solarized-light"
                echo -e "\n${CYAN}Select theme:${NC} "
                read -r theme_choice
                case $theme_choice in
                    1) update_setting "code_theme" "default";;
                    2) update_setting "code_theme" "monokai";;
                    3) update_setting "code_theme" "solarized-dark";;
                    4) update_setting "code_theme" "solarized-light";;
                esac
                ;;
            5)
                echo -e "\n${CYAN}Enter user input color (e.g., #00cc00):${NC} "
                read -r color
                update_setting "user_input_color" "$color"
                ;;
            0) return;;
        esac
    done
}

# History Settings Menu
history_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== History Settings ===${NC}\n"
        echo -e "1) Set Input History File"
        echo -e "2) Set Chat History File"
        echo -e "3) Toggle Chat History Restore"
        echo -e "4) Set LLM History File"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Enter input history file path:${NC} "
                read -r file
                update_setting "input_history_file" "$file"
                ;;
            2)
                echo -e "\n${CYAN}Enter chat history file path:${NC} "
                read -r file
                update_setting "chat_history_file" "$file"
                ;;
            3)
                current=$(get_setting "restore_chat_history")
                if [ "$current" = "false" ]; then
                    update_setting "restore_chat_history" "true"
                else
                    update_setting "restore_chat_history" "false"
                fi
                ;;
            4)
                echo -e "\n${CYAN}Enter LLM history file path:${NC} "
                read -r file
                update_setting "llm_history_file" "$file"
                ;;
            0) return;;
        esac
    done
}

# View Current Configuration
view_config() {
    show_banner
    echo -e "${YELLOW}=== Current Configuration ===${NC}\n"
    echo -e "${CYAN}Contents of $CONFIG_FILE:${NC}\n"
    cat "$CONFIG_FILE"
    echo -e "\n${CYAN}Press Enter to continue...${NC}"
    read -r
}

# Main Menu
main_menu() {
    while true; do
        show_banner
        echo -e "1) Model Settings"
        echo -e "2) Git Settings"
        echo -e "3) Output Settings"
        echo -e "4) History Settings"
        echo -e "5) View Current Configuration"
        echo -e "\n0) Exit"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) model_settings_menu;;
            2) git_settings_menu;;
            3) output_settings_menu;;
            4) history_settings_menu;;
            5) view_config;;
            0) 
                echo -e "\n${GREEN}Configuration saved to $CONFIG_FILE${NC}"
                exit 0
                ;;
        esac
    done
}

# Initialize and start
init_config
main_menu