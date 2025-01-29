E2B allows you to deploy long-running agents with some limitations. Here's how to implement it:

## Basic Agent Deployment

```python
from e2b_code_interpreter import CodeInterpreter
import os

class LongRunningAgent:
    def __init__(self, timeout=3600):  # 1 hour max
        self.sandbox = CodeInterpreter(
            timeout=timeout,
            cpu_count=2,
            memory_mb=4096
        )[1]
        
    async def run(self):
        try:
            with self.sandbox as sandbox:
                # Main agent loop
                while True:
                    # Execute agent tasks
                    result = sandbox.notebook.exec_cell("your_code_here")
                    
                    # Check completion condition
                    if self.is_finished():
                        break
                        
        finally:
            await self.cleanup()
```

## Key Limitations

- Maximum sandbox lifetime is 24 hours[4]
- Sandbox needs to be reconnected after disconnection using:
```python
await Sandbox.reconnect(sandbox.id)[4]
```

## Persistent Storage

```python
def setup_storage(self):
    # Create persistent directories
    self.sandbox.filesystem.makeDir('/data')
    self.sandbox.filesystem.makeDir('/output')
    
    # Save state
    self.sandbox.filesystem.write('/data/state.json', state_data)[4]
```

## Process Management

```python
async def manage_processes(self):
    # Start background process
    process = self.sandbox.commands.start('python worker.py')
    
    try:
        # Monitor process
        while process.is_running():
            await asyncio.sleep(1)
    finally:
        # Cleanup
        process.kill()[1]
```

## Best Practices

1. Implement proper error handling and recovery
2. Use filesystem operations for persistence
3. Monitor resource usage
4. Implement graceful shutdown
5. Use background processes for long-running tasks

## Example Implementation

```python
class PersistentAgent:
    def __init__(self):
        self.sandbox = CodeInterpreter(
            template="custom_template",
            env_vars={
                "AGENT_ID": "unique_id",
                "PERSIST_PATH": "/data"
            }
        )

    async def start(self):
        while True:
            try:
                with self.sandbox as sandbox:
                    # Setup storage
                    await self.setup_storage()
                    
                    # Run main loop
                    await self.run_loop()
                    
            except Exception as e:
                print(f"Error: {e}")
                # Reconnect sandbox
                self.sandbox = await Sandbox.reconnect(self.sandbox.id)
                
            await asyncio.sleep(60)  # Prevent tight loop
            
    async def run_loop(self):
        while True:
            # Execute agent tasks
            result = self.sandbox.notebook.exec_cell(
                "your_agent_code",
                on_stdout=lambda x: print(f"Output: {x}"),
                on_stderr=lambda x: print(f"Error: {x}")
            )
            
            # Save progress
            self.sandbox.filesystem.write(
                '/data/progress.json', 
                result
            )[1][4]
```

Citations:
[1] https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/2592765/ea77bbbd-6403-4426-8e18-3635ca51024e/paste.txt
[2] https://huggingface.co/docs/smolagents/en/tutorials/secure_code_execution
[3] https://www.youtube.com/watch?v=MH3YbiMqusc
[4] https://blog.logrocket.com/building-deploying-ai-agents-e2b/
[5] https://e2b.dev/docs/quickstart/connect-llms
[6] https://e2b.dev/docs/legacy/guide/custom-sandbox
[7] https://e2b.dev/docs
[8] https://e2b.dev
[9] https://www.youtube.com/watch?v=vtRKNbYNrjk
[10] https://github.com/e2b-dev/e2b
[11] https://e2b.dev/blog/build-ai-data-analyst-with-sandboxed-code-execution-using-typescript-and-gpt-4o
[12] https://python.langchain.com/docs/integrations/tools/e2b_data_analysis/