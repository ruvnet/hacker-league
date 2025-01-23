import warnings
warnings.filterwarnings('ignore', category=UserWarning)

from hello_world.crew import HelloWorldCrew

def run():
    crew = HelloWorldCrew()
    result = crew.run()
    print(result)

if __name__ == "__main__":
    run()
