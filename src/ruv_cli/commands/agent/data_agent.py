import os
from typing import List, Optional
from .base_agent import BaseAgent

class DataAgent(BaseAgent):
    """Agent for data science operations"""
    def __init__(self, name: str = "DataAgent"):
        super().__init__(name=name)
        
    def run(self, operation: str, file_path: str = "", columns: List[str] = None) -> str:
        """Execute data operation"""
        try:
            if operation == "load":
                return self._load_data(file_path)
            elif operation == "describe":
                return self._describe_data(file_path, columns)
            elif operation == "plot":
                return self._plot_data(file_path, columns)
            else:
                raise ValueError(f"Unknown operation: {operation}")
        except Exception as e:
            self.log(f"Error executing operation: {str(e)}")
            return ""
            
    def _load_data(self, file_path: str) -> str:
        """Load data from file"""
        if not file_path:
            raise ValueError("File path is required")
            
        # In real implementation, this would use pandas
        # For testing, we'll just simulate loading
        self.log(f"Loading data from {file_path}")
        return f"Loaded data from {file_path}"
        
    def _describe_data(self, file_path: str, columns: Optional[List[str]] = None) -> str:
        """Generate descriptive statistics"""
        if not file_path:
            raise ValueError("File path is required")
            
        # In real implementation, this would use pandas
        # For testing, we'll just simulate description
        cols = ", ".join(columns) if columns else "all columns"
        self.log(f"Describing {cols} in {file_path}")
        return f"Description of {cols} in {file_path}"
        
    def _plot_data(self, file_path: str, columns: Optional[List[str]] = None) -> str:
        """Create visualization"""
        if not file_path:
            raise ValueError("File path is required")
            
        # In real implementation, this would use matplotlib/seaborn
        # For testing, we'll just simulate plotting
        cols = ", ".join(columns) if columns else "all columns"
        self.log(f"Plotting {cols} from {file_path}")
        return f"Plot saved for {cols} from {file_path}"

def run_data_operation(operation: str, file_path: str = "", columns: List[str] = None) -> bool:
    """Run data science operation"""
    if not operation:
        print("[ERROR] Operation is required")
        return False
        
    try:
        agent = DataAgent()
        result = agent.run(operation, file_path, columns)
        if result:
            agent.log(f"Operation Result:\n{result}")
            return True
        return False
        
    except Exception as e:
        print(f"[ERROR] Data operation failed: {str(e)}")
        return False