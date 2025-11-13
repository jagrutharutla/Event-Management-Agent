

# Event Planning Agent System

## Overview

This project automates event planning using intelligent AI agents to scout venues, catering, entertainment, manage guests, optimize budgets, and generate professional communications. The system orchestrates multiple specialized agents working together to create cost-effective event plans based on user inputs.

***

## Features

- Automated extraction of event details (type, city, budget)
- Parallel scouting for venues, catering, and entertainment options
- Plan synthesis combining scouting results into cohesive plans
- Budget optimization with iterative cost-cutting strategies
- Guest list management (add, view guests)
- Professional announcement email drafting and mock sending
- Comprehensive final report generation

***

## Technology Stack

| Technology      | Purpose                                  |
|-----------------|------------------------------------------|
| Python          | Core programming language                |
| Google ADK      | Agent Development Kit for AI agent orchestration |
| Gemini 2.5 Flash| AI language model for natural language understanding and generation |
| Pydantic        | Data validation and schema enforcement  |
| JSON            | Data interchange format between agents  |

***

## Architecture & Design Patterns

- **Agent Pattern:** Modular AI agents specialized per task (scouting, budgeting, communication).
- **Orchestration Pattern:** Master orchestrator delegates tasks to workflows and agents.
- **Workflow Pattern:** Combining agents in sequential, parallel, and loop flows for iterative planning.
- **Tool Pattern:** Agents expose functionality as callable tools.
- **State Management:** Shared session state for consistent data communication via ToolContext.
- **Mocking:** Simulated actions (e.g., sending emails) to test workflows without external dependencies.

***

## Components

### Agents

- **Intake Agent:** Extracts event-related parameters from user input.
- **Guest Management Agent:** Adds and retrieves guest information.
- **Venue, Catering, Entertainment Scouts:** Find options with cost estimates.
- **Initial Plan Synthesizer:** Merges scouting results into one plan.
- **Accountant Agent:** Selects cheapest options and evaluates plan budget.
- **Cost Cutter Agent:** Iteratively refines plan if over budget.
- **Communications Agent:** Drafts event announcement emails.
- **Final Report Agent:** Produces a comprehensive markdown report.

### Workflows

- **Parallel Logistics Scouting:** Simultaneously scout venues, caterers, and entertainers.
- **Initial Planning Workflow:** Sequential combination of scouting and planning agents.
- **Budget Refinement Loop:** Iterative budget optimization.
- **Full Plan Workflow:** End-to-end planning with all agents.
- **Master Orchestrator:** Overall task delegator.

***

## Usage

1. Provide event details (type, city, budget) to initiate planning.
2. Manage guests via guest management tools.
3. Receive a finalized event plan within budget.
4. Draft and simulate event announcement emails.
5. Obtain comprehensive event planning reports.

***

## Example

```python
# Sample usage to add a guest
addguestname("John Doe", "john@example.com")

# Retrieving guest list
guest_list = getguestlist()
print(guest_list)

# Initiate full event planning workflow
plan = fullplanworkflow(event_type="AI Tech Meetup", city="San Francisco", budget=10000)
print(plan)
```

***

## SET UP AND INSTALLATION
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
