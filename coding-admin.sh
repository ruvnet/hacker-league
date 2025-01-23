#!/bin/bash

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Configuration files
CONFIG_FILE=".aider.conf.yml"
OPENROUTER_CONFIG="openrouter_config.yml"
ENV_FILE=".env"

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

# Initialize config files
init_config() {
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "# Aider Configuration File" > "$CONFIG_FILE"
        echo "# Created by coding-admin.sh" >> "$CONFIG_FILE"
        echo "" >> "$CONFIG_FILE"
    fi
    
    if [ ! -f "$OPENROUTER_CONFIG" ]; then
        echo "# OpenRouter Configuration" > "$OPENROUTER_CONFIG"
        echo "models:" >> "$OPENROUTER_CONFIG"
        echo "  development:" >> "$OPENROUTER_CONFIG"
        echo "    tdd: []" >> "$OPENROUTER_CONFIG"
        echo "    swarm: []" >> "$OPENROUTER_CONFIG"
        echo "    agile: []" >> "$OPENROUTER_CONFIG"
    fi

    if [ ! -f "$ENV_FILE" ]; then
        echo "# OpenRouter API Key" > "$ENV_FILE"
        echo "# Get your key from: https://openrouter.ai/keys" >> "$ENV_FILE"
        echo "OPENROUTER_API_KEY=" >> "$ENV_FILE"
        echo "" >> "$ENV_FILE"
        echo "# Optional: Custom base URL (default: https://openrouter.ai/api/v1)" >> "$ENV_FILE"
        echo "# OPENROUTER_BASE_URL=" >> "$ENV_FILE"
        
        echo -e "${YELLOW}Notice: .env file created. Please set your OpenRouter API key.${NC}"
        setup_openrouter_key
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

# Helper function to toggle boolean settings
toggle_setting() {
    local key=$1
    current=$(get_setting "$key")
    if [ "$current" = "true" ]; then
        update_setting "$key" "false"
    else
        update_setting "$key" "true"
    fi
}

# Chat with AI using HelloWorldCrew
chat_with_ai() {
    local prompt=$1
    local task_type=${2:-"both"}
    
    echo -e "\n${CYAN}╔══════════════════════════════════════════════════════════════════╗"
    echo -e "║                   NEURAL CORE ACTIVATION                        ║"
    echo -e "╚══════════════════════════════════════════════════════════════════╝${NC}\n"
    
    # Run the HelloWorldCrew agent with the prompt and task type
    cd /workspaces/hacker-league-jan23 && poetry run python src/hello_world/main.py --prompt "$prompt" --task "$task_type"
    
    local exit_code=$?
    if [ $exit_code -eq 0 ]; then
        echo -e "\n${GREEN}Neural processing completed successfully.${NC}"
    else
        echo -e "\n${RED}Neural processing encountered an error (Exit code: $exit_code).${NC}"
    fi
}

# Setup OpenRouter API Key
setup_openrouter_key() {
    echo -e "\n${CYAN}Would you like to set up your OpenRouter API key now? (y/n):${NC} "
    read -r setup_key
    if [ "$setup_key" = "y" ]; then
        echo -e "\n${CYAN}Please enter your OpenRouter API key (from https://openrouter.ai/keys):${NC} "
        read -r api_key
        if [ ! -z "$api_key" ]; then
            sed -i "s/OPENROUTER_API_KEY=.*/OPENROUTER_API_KEY=$api_key/" "$ENV_FILE"
            echo -e "${GREEN}API key has been set successfully!${NC}"
        else
            echo -e "${RED}No API key provided. You can set it later in the .env file.${NC}"
        fi
    fi
}

# Model Settings Menu
model_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Model Settings ===${NC}\n"
        echo -e "1) Set Main Model"
        echo -e "2) Set Editor Model"
        echo -e "3) Set Weak Model"
        echo -e "4) Configure Model Aliases"
        echo -e "5) Set Model Settings File"
        echo -e "6) Set Model Metadata File"
        echo -e "7) Configure SSL Settings"
        echo -e "8) Set API Timeout"
        echo -e "9) Configure Edit Format"
        echo -e "10) Configure Model Warnings"
        echo -e "11) Set Chat History Tokens"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Select Main Model:${NC}"
                echo "1) GPT-4 Turbo (gpt-4-1106-preview)"
                echo "2) GPT-4 (gpt-4-0613)"
                echo "3) GPT-3.5 Turbo"
                echo "4) Claude-3 Opus"
                echo "5) Claude-3 Sonnet"
                echo "6) Claude-3 Haiku"
                read -r model_choice
                case $model_choice in
                    1) update_setting "model" "gpt-4-1106-preview";;
                    2) update_setting "model" "gpt-4-0613";;
                    3) update_setting "model" "gpt-3.5-turbo";;
                    4) update_setting "model" "claude-3-opus-20240229";;
                    5) update_setting "model" "claude-3-sonnet-20241022";;
                    6) update_setting "model" "claude-3-haiku-20241022";;
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
                echo -e "\n${CYAN}Enter model alias (format: alias:model):${NC} "
                read -r alias
                update_setting "alias" "$alias"
                ;;
            5)
                echo -e "\n${CYAN}Enter model settings file path:${NC} "
                read -r settings_file
                update_setting "model_settings_file" "$settings_file"
                ;;
            6)
                echo -e "\n${CYAN}Enter model metadata file path:${NC} "
                read -r metadata_file
                update_setting "model_metadata_file" "$metadata_file"
                ;;
            7)
                toggle_setting "verify_ssl"
                ;;
            8)
                echo -e "\n${CYAN}Enter API timeout in seconds:${NC} "
                read -r timeout
                update_setting "timeout" "$timeout"
                ;;
            9)
                echo -e "\n${CYAN}Select edit format:${NC}"
                echo "1) Default"
                echo "2) Architect"
                read -r format_choice
                case $format_choice in
                    1) update_setting "edit_format" "default";;
                    2) update_setting "edit_format" "architect";;
                esac
                ;;
            10)
                toggle_setting "show_model_warnings"
                ;;
            11)
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
        echo -e "1) Toggle Git Integration"
        echo -e "2) Configure Gitignore"
        echo -e "3) Set Aiderignore File"
        echo -e "4) Toggle Subtree Only"
        echo -e "5) Configure Auto Commits"
        echo -e "6) Configure Dirty Commits"
        echo -e "7) Configure Author Attribution"
        echo -e "8) Configure Committer Attribution"
        echo -e "9) Configure Commit Messages"
        echo -e "10) Set Commit Prompt"
        echo -e "11) Toggle Dry Run"
        echo -e "12) Configure Repository Checks"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) toggle_setting "git";;
            2) toggle_setting "gitignore";;
            3)
                echo -e "\n${CYAN}Enter aiderignore file path:${NC} "
                read -r aiderignore
                update_setting "aiderignore" "$aiderignore"
                ;;
            4) toggle_setting "subtree_only";;
            5) toggle_setting "auto_commits";;
            6) toggle_setting "dirty_commits";;
            7) toggle_setting "attribute_author";;
            8) toggle_setting "attribute_committer";;
            9)
                toggle_setting "attribute_commit_message_author"
                toggle_setting "attribute_commit_message_committer"
                ;;
            10)
                echo -e "\n${CYAN}Enter commit prompt:${NC} "
                read -r prompt
                update_setting "commit_prompt" "$prompt"
                ;;
            11) toggle_setting "dry_run";;
            12) toggle_setting "skip_sanity_check_repo";;
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
        echo -e "2) Toggle Light Mode"
        echo -e "3) Toggle Pretty Output"
        echo -e "4) Toggle Streaming"
        echo -e "5) Configure Colors"
        echo -e "6) Configure Code Theme"
        echo -e "7) Toggle Show Diffs"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) update_setting "dark_mode" "true";;
            2) update_setting "light_mode" "true";;
            3) toggle_setting "pretty";;
            4) toggle_setting "stream";;
            5)
                echo -e "\n${CYAN}Configure Colors:${NC}"
                echo "1) User Input Color"
                echo "2) Tool Output Color"
                echo "3) Tool Error Color"
                echo "4) Tool Warning Color"
                echo "5) Assistant Output Color"
                read -r color_choice
                echo -e "\n${CYAN}Enter color (e.g., #00cc00):${NC} "
                read -r color
                case $color_choice in
                    1) update_setting "user_input_color" "$color";;
                    2) update_setting "tool_output_color" "$color";;
                    3) update_setting "tool_error_color" "$color";;
                    4) update_setting "tool_warning_color" "$color";;
                    5) update_setting "assistant_output_color" "$color";;
                esac
                ;;
            6)
                echo -e "\n${CYAN}Select Code Theme:${NC}"
                echo "1) Default"
                echo "2) Monokai"
                echo "3) Solarized Dark"
                echo "4) Solarized Light"
                read -r theme_choice
                case $theme_choice in
                    1) update_setting "code_theme" "default";;
                    2) update_setting "code_theme" "monokai";;
                    3) update_setting "code_theme" "solarized-dark";;
                    4) update_setting "code_theme" "solarized-light";;
                esac
                ;;
            7) toggle_setting "show_diffs";;
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
            3) toggle_setting "restore_chat_history";;
            4)
                echo -e "\n${CYAN}Enter LLM history file path:${NC} "
                read -r file
                update_setting "llm_history_file" "$file"
                ;;
            0) return;;
        esac
    done
}

# Linting Settings Menu
linting_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Linting Settings ===${NC}\n"
        echo -e "1) Toggle Auto Lint"
        echo -e "2) Set Lint Command"
        echo -e "3) Configure Language-specific Linting"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) toggle_setting "auto_lint";;
            2)
                echo -e "\n${CYAN}Enter lint command:${NC} "
                read -r cmd
                update_setting "lint_cmd" "$cmd"
                ;;
            3)
                echo -e "\n${CYAN}Select language:${NC}"
                echo "1) Python"
                echo "2) JavaScript"
                echo "3) TypeScript"
                read -r lang_choice
                echo -e "\n${CYAN}Enter lint command for selected language:${NC} "
                read -r cmd
                case $lang_choice in
                    1) update_setting "lint_cmd" "python: $cmd";;
                    2) update_setting "lint_cmd" "javascript: $cmd";;
                    3) update_setting "lint_cmd" "typescript: $cmd";;
                esac
                ;;
            0) return;;
        esac
    done
}

# Testing Settings Menu
testing_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Testing Settings ===${NC}\n"
        echo -e "1) Toggle Auto Test"
        echo -e "2) Set Test Command"
        echo -e "3) Configure Test Strategy"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) toggle_setting "auto_test";;
            2)
                echo -e "\n${CYAN}Enter test command:${NC} "
                read -r cmd
                update_setting "test_cmd" "$cmd"
                ;;
            3)
                echo -e "\n${CYAN}Select test strategy:${NC}"
                echo "1) Unit Tests Only"
                echo "2) Integration Tests"
                echo "3) Full Test Suite"
                read -r strategy
                case $strategy in
                    1) update_setting "test_cmd" "python -m pytest tests/unit";;
                    2) update_setting "test_cmd" "python -m pytest tests/integration";;
                    3) update_setting "test_cmd" "python -m pytest";;
                esac
                ;;
            0) return;;
        esac
    done
}

# Environment Settings Menu
environment_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Environment Settings ===${NC}\n"
        echo -e "1) Set Environment Variables"
        echo -e "2) Configure API Keys"
        echo -e "3) Set Environment File"
        echo -e "4) Configure Shell Commands"
        echo -e "5) Configure Input Settings"
        echo -e "6) Configure URL Detection"
        echo -e "7) Set Editor"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Enter environment variable (KEY=value):${NC} "
                read -r env_var
                update_setting "set_env" "$env_var"
                ;;
            2)
                echo -e "\n${CYAN}Configure API Keys:${NC}"
                echo "1) OpenAI API Key"
                echo "2) Anthropic API Key"
                read -r api_choice
                echo -e "\n${CYAN}Enter API key:${NC} "
                read -r key
                case $api_choice in
                    1) update_setting "openai_api_key" "$key";;
                    2) update_setting "anthropic_api_key" "$key";;
                esac
                ;;
            3)
                echo -e "\n${CYAN}Enter environment file path:${NC} "
                read -r file
                update_setting "env_file" "$file"
                ;;
            4) toggle_setting "suggest_shell_commands";;
            5)
                toggle_setting "fancy_input"
                toggle_setting "multiline"
                ;;
            6) toggle_setting "detect_urls";;
            7)
                echo -e "\n${CYAN}Enter editor command:${NC} "
                read -r editor
                update_setting "editor" "$editor"
                ;;
            0) return;;
        esac
    done
}

# Performance Settings Menu
performance_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Performance Settings ===${NC}\n"
        echo -e "1) Configure Cache Settings"
        echo -e "2) Configure Map Settings"
        echo -e "3) Configure Analytics"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Cache Settings:${NC}"
                echo "1) Toggle Cache Prompts"
                echo "2) Set Cache Keepalive Pings"
                read -r cache_choice
                case $cache_choice in
                    1) toggle_setting "cache_prompts";;
                    2)
                        echo -e "\n${CYAN}Enter number of keepalive pings:${NC} "
                        read -r pings
                        update_setting "cache_keepalive_pings" "$pings"
                        ;;
                esac
                ;;
            2)
                echo -e "\n${CYAN}Map Settings:${NC}"
                echo "1) Set Map Tokens"
                echo "2) Set Map Refresh Strategy"
                echo "3) Set Map Multiplier"
                read -r map_choice
                case $map_choice in
                    1)
                        echo -e "\n${CYAN}Enter map tokens:${NC} "
                        read -r tokens
                        update_setting "map_tokens" "$tokens"
                        ;;
                    2)
                        echo -e "\n${CYAN}Select refresh strategy:${NC}"
                        echo "1) Auto"
                        echo "2) Always"
                        echo "3) Files"
                        echo "4) Manual"
                        read -r strategy
                        case $strategy in
                            1) update_setting "map_refresh" "auto";;
                            2) update_setting "map_refresh" "always";;
                            3) update_setting "map_refresh" "files";;
                            4) update_setting "map_refresh" "manual";;
                        esac
                        ;;
                    3)
                        echo -e "\n${CYAN}Enter map multiplier:${NC} "
                        read -r multiplier
                        update_setting "map_multiplier_no_files" "$multiplier"
                        ;;
                esac
                ;;
            3)
                echo -e "\n${CYAN}Analytics Settings:${NC}"
                echo "1) Toggle Analytics"
                echo "2) Set Analytics Log File"
                echo "3) Disable Analytics Permanently"
                read -r analytics_choice
                case $analytics_choice in
                    1) toggle_setting "analytics";;
                    2)
                        echo -e "\n${CYAN}Enter analytics log file path:${NC} "
                        read -r log_file
                        update_setting "analytics_log" "$log_file"
                        ;;
                    3) update_setting "analytics_disable" "true";;
                esac
                ;;
            0) return;;
        esac
    done
}

# View Configuration
view_config() {
    show_banner
    echo -e "${YELLOW}=== Current Configuration ===${NC}\n"
    echo -e "${CYAN}Contents of $CONFIG_FILE:${NC}\n"
    cat "$CONFIG_FILE"
    echo -e "\n${CYAN}Contents of $OPENROUTER_CONFIG:${NC}\n"
    cat "$OPENROUTER_CONFIG"
    if [ -f "$ENV_FILE" ]; then
        echo -e "\n${CYAN}Contents of $ENV_FILE:${NC}\n"
        cat "$ENV_FILE"
    fi
    echo -e "\n${CYAN}Press Enter to continue...${NC}"
    read -r
}

# Chat Menu
chat_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== AI Chat Assistant ===${NC}\n"
        echo -e "1) Get Help with Settings"
        echo -e "2) Development Workflow Guidance"
        echo -e "3) Configuration Recommendations"
        echo -e "4) Chat Settings"
        echo -e "\n0) Back to Main Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}What setting would you like help with?${NC} "
                read -r query
                clear
                chat_with_ai "Help me understand and configure this aider setting: $query" "research"
                echo -e "\n${CYAN}Press Enter to return to menu...${NC}"
                read -r
                ;;
            2)
                echo -e "\n${CYAN}What type of development workflow are you interested in?${NC} "
                read -r workflow
                clear
                chat_with_ai "Guide me through setting up aider for $workflow development workflow. Include specific settings and best practices." "both"
                echo -e "\n${CYAN}Press Enter to return to menu...${NC}"
                read -r
                ;;
            3)
                echo -e "\n${CYAN}What type of project are you working on?${NC} "
                read -r project
                clear
                chat_with_ai "Recommend optimal aider settings for a $project project. Include explanations for each recommendation." "research"
                echo -e "\n${CYAN}Press Enter to return to menu...${NC}"
                read -r
                ;;
            4)
                chat_settings_menu
                ;;
            0) return;;
        esac
    done
}

# Chat Settings Menu
chat_settings_menu() {
    while true; do
        show_banner
        echo -e "${YELLOW}=== Chat Settings ===${NC}\n"
        echo -e "1) Set AI Model"
        echo -e "2) Configure OpenRouter Settings"
        echo -e "3) Configure System Prompt"
        echo -e "4) Configure Voice Settings"
        echo -e "\n0) Back to Chat Menu"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1)
                echo -e "\n${CYAN}Select AI Model:${NC}"
                echo "1) anthropic/claude-3-opus (Most capable)"
                echo "2) anthropic/claude-3-sonnet (Balanced)"
                echo "3) google/gemini-pro (Fast)"
                read -r model_choice
                case $model_choice in
                    1) update_setting "chat_model" "anthropic/claude-3-opus";;
                    2) update_setting "chat_model" "anthropic/claude-3-sonnet";;
                    3) update_setting "chat_model" "google/gemini-pro";;
                esac
                ;;
            2)
                setup_openrouter_key
                ;;
            3)
                echo -e "\n${CYAN}Enter system prompt (default: You are a helpful AI assistant focused on research and task execution using ReACT methodology):${NC} "
                read -r prompt
                if [ -z "$prompt" ]; then
                    prompt="You are an AI assistant specialized in helping users configure and use aider effectively. You have comprehensive knowledge of aider's settings and capabilities:

CORE CAPABILITIES:
1. Model Selection: Help users choose between models (GPT-4, Claude-3, etc.) based on their needs
2. Git Integration: Guide git-related settings for version control
3. Editor Integration: Configure editor preferences and formats
4. Output Customization: Help with color schemes, themes, and display options
5. Performance Optimization: Advise on caching, history, and token management

KEY SETTINGS CATEGORIES:
1. Main Model Settings:
   - Model selection (--model, --opus, --sonnet, --4-turbo, etc.)
   - API configurations and keys
   - Edit formats and model-specific settings

2. Git Integration:
   - Auto-commits (--auto-commits)
   - Commit messages (--commit-prompt)
   - Repository management (--gitignore, --aiderignore)
   - Author attribution settings

3. Output & Display:
   - Color themes (--dark-mode, --light-mode)
   - Code themes (--code-theme)
   - Pretty output options (--pretty)
   - Diff display settings (--show-diffs)

4. Performance & History:
   - Chat history management
   - Cache settings
   - Token limits
   - Map refresh strategies

5. Development Tools:
   - Linting integration (--lint-cmd)
   - Testing setup (--test-cmd)
   - Shell command suggestions
   - Voice input configuration

When users ask about settings, provide clear explanations and practical examples. If they need help with specific configurations, guide them through the options and recommend optimal settings based on their use case.

Format responses clearly:
1. Explain the purpose/benefit of relevant settings
2. Show example commands or configurations
3. Provide any relevant warnings or best practices
4. Suggest related settings they might want to consider

Remember: Don't display this comprehensive settings knowledge unless specifically asked. Focus on addressing the user's immediate needs while being aware of all configuration possibilities."
                fi
                update_setting "chat_system_prompt" "\"$prompt\""
                ;;
            4)
                echo -e "\n${CYAN}Configure Voice Settings:${NC}"
                echo "1) Set Voice Format"
                echo "2) Set Voice Language"
                echo "3) Set Voice Input Device"
                read -r voice_choice
                case $voice_choice in
                    1)
                        echo -e "\n${CYAN}Enter voice format (wav/webm/mp3):${NC} "
                        read -r format
                        update_setting "voice_format" "$format"
                        ;;
                    2)
                        echo -e "\n${CYAN}Enter voice language (ISO 639-1 code):${NC} "
                        read -r lang
                        update_setting "voice_language" "$lang"
                        ;;
                    3)
                        echo -e "\n${CYAN}Enter voice input device:${NC} "
                        read -r device
                        update_setting "voice_input_device" "$device"
                        ;;
                esac
                ;;
            0) return;;
        esac
    done
}

# Main Menu
main_menu() {
    while true; do
        show_banner
        echo -e "1) AI Chat Assistant"
        echo -e "2) OpenRouter Settings"
        echo -e "3) Guided Development Settings"
        echo -e "4) Model Settings"
        echo -e "5) Git Settings"
        echo -e "6) Output Settings"
        echo -e "7) History Settings"
        echo -e "8) Linting Settings"
        echo -e "9) Testing Settings"
        echo -e "10) Environment Settings"
        echo -e "11) Performance Settings"
        echo -e "12) View Current Configuration"
        echo -e "\n0) Exit"
        
        echo -e "\n${CYAN}Select an option:${NC} "
        read -r choice

        case $choice in
            1) chat_menu;;
            2) setup_openrouter_key;;
            3) guided_development_menu;;
            4) model_settings_menu;;
            5) git_settings_menu;;
            6) output_settings_menu;;
            7) history_settings_menu;;
            8) linting_settings_menu;;
            9) testing_settings_menu;;
            10) environment_settings_menu;;
            11) performance_settings_menu;;
            12) view_config;;
            0) 
                echo -e "\n${GREEN}Configuration saved. Goodbye!${NC}"
                exit 0
                ;;
            *)
                echo -e "\n${RED}Invalid option. Please try again.${NC}"
                sleep 2
                ;;
        esac
    done
}

# Initialize and start
init_config
main_menu
