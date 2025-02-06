"""
NOVA Knowledge Distillation CLI
"""

import argparse
import asyncio
from pathlib import Path
import yaml
from .core import KnowledgeDistiller

def format_size(size_mb: int) -> str:
    """Format size in MB to human readable format"""
    if size_mb < 1024:
        return f"{size_mb} MB"
    return f"{size_mb/1024:.1f} GB"

def main():
    parser = argparse.ArgumentParser(description='NOVA Knowledge Distillation System')
    
    # Command subparsers
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Distill command
    distill_parser = subparsers.add_parser('distill', help='Run knowledge distillation')
    distill_parser.add_argument('--domain', type=str, required=True,
                              help='Domain to extract knowledge from')
    distill_parser.add_argument('--prompt', type=str, required=True,
                              help='Prompt for knowledge extraction')
    distill_parser.add_argument('--architecture', type=str, default='transformer_tiny',
                              help='Student model architecture')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List available models')
    list_parser.add_argument('--type', choices=['teacher', 'student'], default='all',
                           help='Type of models to list')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Show model information')
    info_parser.add_argument('model', type=str,
                           help='Model name to show information for')
    
    args = parser.parse_args()
    
    # Load configurations
    config_dir = Path(__file__).parent.parent / 'config'
    with open(config_dir / 'models.yaml', 'r') as f:
        models_config = yaml.safe_load(f)
    
    if args.command == 'distill':
        print(f"""
╔══════════════════════════════════════════════════════════════════╗
║              NOVA KNOWLEDGE DISTILLATION SYSTEM                  ║
║        [ NEURO-SYMBOLIC OPTIMIZED VERSATILE AGENT ]             ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
Domain: {args.domain}
Architecture: {args.architecture}
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
        
        distiller = KnowledgeDistiller()
        success = distiller.run(args.domain, args.prompt, args.architecture)
        
        if success:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║             🌟 DISTILLATION COMPLETE 🌟                         ║
╚══════════════════════════════════════════════════════════════════╝

▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
        ✨ KNOWLEDGE EXTRACTED
        📊 MODEL TRAINED
        🔒 PERFORMANCE VALIDATED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
""")
        else:
            print("""
╔══════════════════════════════════════════════════════════════════╗
║             ❌ DISTILLATION FAILED ❌                           ║
╚══════════════════════════════════════════════════════════════════╝
""")
            
    elif args.command == 'list':
        print("\nAvailable Models:")
        print("================")
        
        if args.type in ['all', 'teacher']:
            print("\nTeacher Models:")
            print("--------------")
            for name, config in models_config['teacher_models'].items():
                print(f"- {name}")
                print(f"  Role: {config['role']}")
                print(f"  Model: {config['llm']}")
                print()
                
        if args.type in ['all', 'student']:
            print("\nStudent Architectures:")
            print("--------------------")
            for name, config in models_config['student_models'].items():
                print(f"- {name}")
                print(f"  Parameters: {config['params']}")
                print(f"  Size: {format_size(config['size_mb'])}")
                print(f"  Capabilities: {', '.join(config['capabilities'])}")
                print()
                
    elif args.command == 'info':
        if args.model in models_config['teacher_models']:
            config = models_config['teacher_models'][args.model]
            print(f"\nTeacher Model: {args.model}")
            print("======================")
            print(f"Role: {config['role']}")
            print(f"Goal: {config['goal']}")
            print(f"Model: {config['llm']}")
            print("\nCapabilities:")
            print(f"- Validation Required: {config['user_prompt']['validation_required']}")
            print(f"- Progress Tracking: {config['user_prompt']['progress_tracking']}")
            print(f"- Reasoning Depth: {config['react_validation']['reasoning_depth']}")
            
        elif args.model in models_config['student_models']:
            config = models_config['student_models'][args.model]
            print(f"\nStudent Architecture: {args.model}")
            print("=========================")
            print(f"Parameters: {config['params']}")
            print(f"Size: {format_size(config['size_mb'])}")
            print(f"Capabilities: {', '.join(config['capabilities'])}")
            print("\nOptimization:")
            print(f"- Quantization: {config['optimization']['quantization']}")
            print(f"- Pruning: {config['optimization']['pruning']}")
            print(f"- Distillation: {config['optimization']['distillation']}")
            
        else:
            print(f"Error: Model '{args.model}' not found")
            
    else:
        parser.print_help()

if __name__ == '__main__':
    main()