# Event-Management-Agent

Event Planner AI is a Python-based project to assist in event planning through AI-powered agents. This project uses the Google ADK (Assistant Development Kit) and provides a web interface for interaction.

## Project Description

This project leverages Google's ADK to build intelligent agents for event management. It is developed in Python within a virtual environment for dependency management and ease of use.

## Prerequisites

- Python 3.x
- Virtualenv or venv for Python virtual environments
- Git (optional for repository management)

## Setup and Installation

1. Clone the repository:
git clone https://github.com/jagrutharutla/Event-Management-Agent.git
cd Event-Management-Agent/my_agents

2. Create and activate a virtual environment:
- On Windows:
  ```
  python -m venv venv
  .\venv\Scripts\Activate
  ```
- On macOS/Linux:
  ```
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Install required packages:
pip install google-adk==1.13.0


5. (Optional) Set environment variables by creating a `.env` file in the project directory.

6. Launch the server:
adk web

text
This starts the server for your AI event planning agent.

## Usage

- Activate the virtual environment each time before running the project.
- Use `adk` commands to manage and test your agent.
- The development server runs locally and can be accessed via the browser for testing.
