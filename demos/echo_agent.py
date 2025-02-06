"""Demo agent that echoes input with enterprise-grade formatting and effects."""

import asyncio
import logging
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional, List

# ANSI color codes for formatted output
CYAN = '\033[0;36m'
GREEN = '\033[0;32m'
YELLOW = '\033[0;33m'
BLUE = '\033[0;34m'
MAGENTA = '\033[0;35m'
RED = '\033[0;31m'
NC = '\033[0m'  # No Color

class EchoAgent:
    """Agent that demonstrates enterprise-grade message handling and formatting"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.echo_agent")
        self.name = "echo_agent"
        self.styles = {
            "uppercase": lambda x: x.upper(),
            "lowercase": lambda x: x.lower(),
            "title": lambda x: x.title(),
            "alternating": lambda x: ''.join(c.upper() if i % 2 == 0 else c.lower() for i, c in enumerate(x)),
            "reversed": lambda x: x[::-1],
            "spaced": lambda x: ' '.join(x)
        }

    async def _animate_processing(self, message: str) -> None:
        """Display animated processing effect"""
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        for _ in range(10):  # Show animation for 1 second
            for char in chars:
                print(f"\r{CYAN}{char} Processing message...{NC}", end='', flush=True)
                await asyncio.sleep(0.01)
        print("\r" + " " * 50 + "\r", end='')  # Clear animation line

    def _apply_rainbow_effect(self, text: str) -> str:
        """Apply rainbow color effect to text"""
        colors = [RED, YELLOW, GREEN, CYAN, BLUE, MAGENTA]
        rainbow_text = ""
        for i, char in enumerate(text):
            if char.strip():
                rainbow_text += f"{colors[i % len(colors)]}{char}{NC}"
            else:
                rainbow_text += char
        return rainbow_text

    async def execute(
        self,
        message: str,
        style: Optional[str] = None,
        repeat: int = 1,
        rainbow: bool = False
    ) -> Dict[str, Any]:
        """Echo the input message with enterprise-grade processing"""
        try:
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  🔊 ECHO SYSTEM v1.0
║     PROCESSING MESSAGE...
╚══════════════════════════════════════════════════════════════════╝

{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
📥 INPUT RECEIVED
🎨 STYLE: {style or 'none'}
🔄 REPEAT: {repeat}
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            print(f"{GREEN}[ECHO] Phase 1: Input Validation{NC}")
            self.log.info(f"Processing message: {message}")
            print("✅ Input validated\n")
            
            print(f"{GREEN}[ECHO] Phase 2: Style Processing{NC}")
            await self._animate_processing(message)
            
            # Apply style if specified
            if style and style in self.styles:
                formatted_message = self.styles[style](message)
            else:
                formatted_message = message
            
            # Apply rainbow effect if requested
            if rainbow:
                formatted_message = self._apply_rainbow_effect(formatted_message)
            
            # Repeat message if requested
            result = "\n".join([formatted_message] * repeat)
            
            print(f"{GREEN}[ECHO] Phase 3: Output Formatting{NC}")
            print("📝 Applying final formatting...")
            print("✅ Processing complete\n")
            
            print(f"""
{CYAN}▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
✨ PROCESSING COMPLETE
📤 OUTPUT READY
🎯 ECHO PREPARED
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀{NC}
""")
            
            return {
                "status": "success",
                "data": {
                    "original": message,
                    "formatted": result,
                    "style": style or "none",
                    "repeat": repeat,
                    "rainbow": rainbow
                },
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.log.error(f"Error in echo agent: {str(e)}")
            return {
                "status": "error",
                "error": str(e),
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

    def format_output(self, result: Dict[str, Any]) -> str:
        """Format echo results with enhanced visual presentation"""
        if result["status"] != "success":
            return f"""
╔══════════════════════════════════════════════════════════════════╗
║  ❌ Echo System Error
╚══════════════════════════════════════════════════════════════════╝

Error: {result.get('error', 'Unknown error')}
Timestamp: {result['timestamp']}
"""
        
        data = result["data"]
        style_color = MAGENTA if data["style"] != "none" else BLUE
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║  🔊 Echo Result
╚══════════════════════════════════════════════════════════════════╝

📥 Original Input:
{YELLOW}{data['original']}{NC}

⚙️ Processing Details:
  • Style: {style_color}{data['style']}{NC}
  • Repeat: {data['repeat']} time(s)
  • Rainbow: {'🌈 Yes' if data.get('rainbow') else '❌ No'}

📤 Formatted Output:
{data['formatted']}

⏰ Last Updated: {result['timestamp']}
"""

async def main():
    """Run the EchoAgent demo with enterprise-grade setup"""
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    agent = EchoAgent()
    
    # Demo messages with various styles
    demos = [
        ("Hello, World!", "none", 1, False),
        ("The Quick Brown Fox", "uppercase", 2, False),
        ("JUMPS OVER THE LAZY DOG", "lowercase", 1, False),
        ("testing rainbow effect", "title", 1, True),
        ("Special Effects Demo", "alternating", 2, False),
        ("Reverse This Message", "reversed", 1, False),
        ("No Spaces Here", "spaced", 1, True)
    ]
    
    for message, style, repeat, rainbow in demos:
        try:
            result = await agent.execute(message, style=style, repeat=repeat, rainbow=rainbow)
            print(agent.format_output(result))
            await asyncio.sleep(1)  # Pause between demos
        except Exception as e:
            logging.error(f"Error in demo: {str(e)}")
            continue

if __name__ == "__main__":
    asyncio.run(main())
