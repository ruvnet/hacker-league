"""Demo agent that echoes input with formatting."""

import asyncio
import logging
from datetime import datetime, timezone
from typing import Dict, Any, Optional

class EchoAgent:
    """Simple agent that demonstrates basic message handling"""
    
    def __init__(self):
        self.log = logging.getLogger("demos.echo_agent")
        self.name = "echo_agent"

    async def execute(
        self,
        message: str,
        style: Optional[str] = None,
        repeat: int = 1
    ) -> Dict[str, Any]:
        """Echo the input message with optional styling"""
        try:
            self.log.info(f"Processing message: {message}")
            
            # Apply style if specified
            if style == "uppercase":
                formatted_message = message.upper()
            elif style == "lowercase":
                formatted_message = message.lower()
            elif style == "title":
                formatted_message = message.title()
            else:
                formatted_message = message
            
            # Repeat message if requested
            result = "\n".join([formatted_message] * repeat)
            
            return {
                "status": "success",
                "data": {
                    "original": message,
                    "formatted": result,
                    "style": style or "none",
                    "repeat": repeat
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

async def main():
    """Demo the echo agent"""
    agent = EchoAgent()
    
    # Demo different styles
    styles = [None, "uppercase", "lowercase", "title"]
    messages = [
        "Hello, World!",
        "Testing 1-2-3",
        "DEMO message HERE"
    ]
    
    for message in messages:
        for style in styles:
            result = await agent.execute(message, style=style, repeat=2)
            print(f"""
╔══════════════════════════════════════════════════════════════════╗
║  Echo Agent Demo - Style: {style or 'none'}
╚══════════════════════════════════════════════════════════════════╝

Original: {result['data']['original']}
Formatted:
{result['data']['formatted']}
""")
            await asyncio.sleep(1)  # Pause between demos

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())