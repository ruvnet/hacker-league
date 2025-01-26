import argparse
import sys
from .commands import auth, template, sandbox

class RuvArgumentParser(argparse.ArgumentParser):
    def error(self, message):
        """Override error handling to use exit code 1 instead of 2"""
        self.print_usage(sys.stderr)
        self.exit(1, f"{self.prog}: error: {message}\n")

def main():
    parser = RuvArgumentParser(
        prog="ruv",
        description="RUV CLI - E2B Agent Management"
    )
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # Auth subcommand
    auth_parser = subparsers.add_parser(
        "auth", 
        help="Authentication commands",
        description="Authentication commands for E2B"
    )
    auth_sub = auth_parser.add_subparsers(
        dest="auth_cmd",
        title="Authentication commands",
        metavar="COMMAND"
    )
    
    # Login command
    auth_sub.add_parser(
        "login",
        help="Login to E2B",
        description="Login to E2B using API key from environment"
    )
    
    # Logout command
    auth_sub.add_parser(
        "logout",
        help="Logout from E2B",
        description="Clear stored E2B credentials"
    )

    # Template subcommand
    template_parser = subparsers.add_parser(
        "template",
        help="Template management commands",
        description="Commands for managing E2B sandbox templates"
    )
    template_sub = template_parser.add_subparsers(
        dest="template_cmd",
        title="Template commands",
        metavar="COMMAND"
    )

    # Template init command
    template_sub.add_parser(
        "init",
        help="Initialize new template files",
        description="Create new e2b.toml and Dockerfile"
    )

    # Template build command
    template_sub.add_parser(
        "build",
        help="Build template",
        description="Build sandbox template from current directory"
    )

    # Template list command
    template_sub.add_parser(
        "list",
        help="List templates",
        description="List all available sandbox templates"
    )

    # Sandbox subcommand
    sandbox_parser = subparsers.add_parser(
        "sandbox",
        help="Sandbox management commands",
        description="Commands for managing E2B sandboxes"
    )
    sandbox_sub = sandbox_parser.add_subparsers(
        dest="sandbox_cmd",
        title="Sandbox commands",
        metavar="COMMAND"
    )

    # Sandbox list command
    sandbox_sub.add_parser(
        "list",
        help="List sandboxes",
        description="List all active sandboxes"
    )

    # Sandbox kill command
    kill_parser = sandbox_sub.add_parser(
        "kill",
        help="Kill sandbox",
        description="Terminate a running sandbox"
    )
    kill_parser.add_argument("id", help="Sandbox ID to terminate")

    # Sandbox status command
    status_parser = sandbox_sub.add_parser(
        "status",
        help="Get sandbox status",
        description="Get detailed status of a sandbox"
    )
    status_parser.add_argument("id", help="Sandbox ID to check")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
        
    if args.command == "auth":
        if args.auth_cmd == "login":
            success = auth.login()
            sys.exit(0 if success else 1)
        elif args.auth_cmd == "logout":
            success = auth.logout()
            sys.exit(0 if success else 1)
        else:
            auth_parser.print_help()
            sys.exit(1)
    elif args.command == "template":
        if args.template_cmd == "init":
            success = template.init_template()
            sys.exit(0 if success else 1)
        elif args.template_cmd == "build":
            success = template.build_template()
            sys.exit(0 if success else 1)
        elif args.template_cmd == "list":
            success = template.list_templates()
            sys.exit(0 if success else 1)
        else:
            template_parser.print_help()
            sys.exit(1)
    elif args.command == "sandbox":
        if args.sandbox_cmd == "list":
            success = sandbox.list_sandboxes()
            sys.exit(0 if success else 1)
        elif args.sandbox_cmd == "kill":
            success = sandbox.kill_sandbox(args.id)
            sys.exit(0 if success else 1)
        elif args.sandbox_cmd == "status":
            status = sandbox.get_sandbox_status(args.id)
            if status:
                print("\nSandbox Status:")
                print("-" * 40)
                print(f"ID: {status['id']}")
                print(f"Status: {status['status']}")
                print(f"Started: {status['started']}")
                print("\nResources:")
                for key, value in status['resources'].items():
                    print(f"  {key}: {value}")
                print("\nProcesses:")
                for proc in status['processes']:
                    print(f"  {proc['name']} (PID {proc['pid']}):")
                    print(f"    CPU: {proc['cpu']}")
                    print(f"    Memory: {proc['memory']}")
                sys.exit(0)
            sys.exit(1)
        else:
            sandbox_parser.print_help()
            sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()