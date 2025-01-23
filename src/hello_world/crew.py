from crewai import Agent, Crew, Process, Task
from hello_world.tools.custom_tool import CustomTool
import yaml
from dotenv import load_dotenv
import os

load_dotenv()  # Load environment variables from .env file

class HelloWorldCrew:
    def __init__(self):
        with open('src/hello_world/config/agents.yaml', 'r') as f:
            self.agents_config = yaml.safe_load(f)
        with open('src/hello_world/config/tasks.yaml', 'r') as f:
            self.tasks_config = yaml.safe_load(f)
            
    def run(self):
        # Create agents
        researcher = Agent(
            role=self.agents_config['researcher']['role'],
            goal=self.agents_config['researcher']['goal'],
            backstory=self.agents_config['researcher']['backstory'],
            tools=[CustomTool()],
            llm_config={"config_list": [{"model": self.agents_config['researcher']['llm'], "api_key": os.getenv("OPENAI_API_KEY"), "base_url": os.getenv("OPENAI_API_BASE")}]}
        )
        
        executor = Agent(
            role=self.agents_config['executor']['role'],
            goal=self.agents_config['executor']['goal'],
            backstory=self.agents_config['executor']['backstory'],
            llm_config={"config_list": [{"model": self.agents_config['executor']['llm'], "api_key": os.getenv("OPENAI_API_KEY"), "base_url": os.getenv("OPENAI_API_BASE")}]}
        )
        
        # Create tasks
        research_task = Task(
            description=self.tasks_config['research_task']['description'],
            agent=researcher
        )
        
        execution_task = Task(
            description=self.tasks_config['execution_task']['description'],
            agent=executor
        )
        
        # Create crew
        crew = Crew(
            agents=[researcher, executor],
            tasks=[research_task, execution_task],
            process=Process.sequential,
            verbose=True
        )
        
        return crew.kickoff()
