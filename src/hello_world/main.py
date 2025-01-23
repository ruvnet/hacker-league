from hello_world.crew import HelloWorldCrew

def run():
    crew = HelloWorldCrew().crew()
    result = crew.kickoff(inputs={'topic': 'artificial intelligence'})
    print(result)

if __name__ == "__main__":
    run()