from .code_agent import run_code

def handle_agent_command(args):
    """Route agent commands to appropriate handlers"""
    if args.agent_cmd == "code":
        query = " ".join(args.query) if args.query else ""
        success = run_code(query)
        return success
    else:
        print("[ERROR] Unknown agent subcommand.")
        return False