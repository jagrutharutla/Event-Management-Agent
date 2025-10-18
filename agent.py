import json
from google.adk.tools import ToolContext

# --- Data Stores ---
GUEST_DATABASE = {}

# --- Tool Functions ---
def add_guest(name: str, email: str) -> str:
  """Adds a guest's name and email to the event's guest list."""
  print(f"  [Tool Call] Adding guest '{name}' with email '{email}'.")
  GUEST_DATABASE[email] = name
  return f"Successfully added {name} to the guest list."

def get_guest_list(tool_context: ToolContext) -> str:
  """Retrieves the current list of all registered guests for the event."""
  print("  [Tool Call] Retrieving guest list.")
  if not GUEST_DATABASE:
    return "The guest list is currently empty."
  tool_context.state["guest_list"] = GUEST_DATABASE
  return json.dumps(GUEST_DATABASE)

def sum_costs(costs: list[float]) -> float:
  """Calculates the sum of a list of numbers."""
  return sum(costs)

COMPLETION_PHRASE = "The plan is within the budget."
def exit_loop(tool_context: ToolContext):
  """Call this function ONLY when the plan is approved and within budget."""
  print("  [Tool Call] Budget approved. Terminating loop.")
  tool_context.actions.escalate = True
  return "Budget approved. Finalizing plan."

def update_session_state(
    tool_context: ToolContext, event_type: str, city: str, budget: int
) -> str:
  """Saves the extracted event parameters to the session state."""
  tool_context.state['event_type'] = event_type
  tool_context.state['city'] = city
  tool_context.state['budget'] = budget
  return "Session state has been updated with event parameters."

def send_mock_email(tool_context: ToolContext) -> str:
    """
    Simulates sending an email. It retrieves the structured EmailDraft object
    from the session state and formats a mock email.
    """
    print("  [Tool Call] Preparing to send mock emails...")

    guest_list = GUEST_DATABASE
    # Retrieve the structured EmailDraft object directly from the state
    email_draft = tool_context.state.get("email_draft")
    # print(f"[Tool call...] {email_draft}")
    # print(f"Type: {type(email_draft)}")

    if not guest_list:
        return "There are no guests on the list to email."

    print("\n--- SIMULATING EMAIL SEND ---")
    for email, name in guest_list.items():
        print(f"To: {name} <{email}>")
        print(f"Subject: {email_draft['subject']}")
        print("\nBody:\n" + email_draft["body"])
        print("-----------------------------")

    return f"Successfully prepared simulated emails for {len(guest_list)} guests."

from google.adk.agents import Agent
from google.adk.tools import google_search
from google.adk.tools.agent_tool import AgentTool

google_search_agent = Agent(
    name="Google_Search_Agent",
    model="gemini-2.5-flash",
    instruction="You are just a wrapper for the Google Search tool.",
    tools=[google_search]
)

google_search_tool = AgentTool(agent=google_search_agent)

from google.adk.agents import SequentialAgent, LoopAgent, ParallelAgent

# --- Intake Agent ---
intake_agent = Agent(
    name="intake_agent",
    model="gemini-2.5-flash",
    instruction="From the user's query, identify the event type (e.g., 'AI tech meetup'), the city, and the budget. Then, you MUST call the `update_session_state` tool.",
    tools=[update_session_state]
)

# --- Guest Management Agent ---
guest_management_agent = Agent(
    name="guest_management_agent",
    model="gemini-2.5-flash",
    instruction="You are a guest management assistant. Use the `add_guest` and `get_guest_list` tools.",
    tools=[add_guest, get_guest_list]
)

# --- Parallel Logistics Scouting Team ---
venue_scout_agent = Agent(
    name="venue_scout_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a venue scout. Find 3 potential venues for a {{event_type}} in {{city}}. For each venue, find an estimated rental cost.
    Output ONLY a JSON object with your findings, like this: {"venues": [{"name": "Venue A", "estimated_cost": 5000}]}
    """,
    tools=[google_search],
    output_key="venue_options"
)
catering_scout_agent = Agent(
    name="catering_scout_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a catering scout. Find 3 catering companies suitable for a {{event_type}} in {{city}}. For each caterer, find an estimated cost.
    Output ONLY a JSON object with your findings, like this: {"caterers": [{"name": "Caterer A", "estimated_cost": 4000}]}
    """,
    tools=[google_search],
    output_key="catering_options"
)
entertainment_scout_agent = Agent(
    name="entertainment_scout_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are an entertainment scout. Find 3 entertainment options for a {{event_type}} in {{city}}. For each option, find an estimated booking fee.
    Output ONLY a JSON object with your findings, like this: {"entertainment": [{"name": "DJ A", "estimated_cost": 1500}]}
    """,
    tools=[google_search],
    output_key="entertainment_options"
)
initial_plan_synthesizer_agent = Agent(
    name="initial_plan_synthesizer_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are an initial plan synthesizer. Combine the findings from {{venue_options}}, {{catering_options}}, and {{entertainment_options}} into a single JSON object.
    The final JSON must have the keys "venues", "caterers", and "entertainment". Output ONLY the JSON object.
    Example: {"venues": [...], "caterers": [...], "entertainment": [...]}
    """,
    output_key="current_plan"
)

# --- Budget Optimizer Team (Instructions Updated) ---
accountant_agent = Agent(
    name="accountant_agent",
    model="gemini-2.5-flash",
    tools=[sum_costs],
    instruction=f"""
    You are a meticulous accountant. Your budget is {{budget}}. The current list of options is in {{current_plan}}.

    Your task is to create the most cost-effective plan and evaluate it:
    1. From the lists of 'venues', 'caterers', and 'entertainment', select ONLY the single cheapest option from each category.
    2. Create a "cheapest_plan" consisting of just these three items.
    3. Use the `sum_costs` tool on this "cheapest_plan".

    - IF the total cost > {{budget}}, your output MUST be a JSON object with a 'critique' and the 'cheapest_plan' you created.
    - ELSE, your output MUST be a JSON object where the 'critique' is '{COMPLETION_PHRASE}' and you include the 'cheapest_plan'.

    Example Output if over budget:
    ```json
    {{
        "critique": "Even with the cheapest options, this plan is over budget. Find a cheaper venue.",
        "cheapest_plan": {{
            "venue": {{"name": "Affordable Hall", "estimated_cost": 3200}},
            "caterer": {{"name": "Good Eats Catering", "estimated_cost": 4000}},
            "entertainment": {{"name": "Local DJ", "estimated_cost": 1000}}
        }}
    }}
    ```
    """,
    output_key="evaluation"
)
cost_cutter_agent = Agent(
    name="cost_cutter_agent",
    model="gemini-2.5-flash",
    tools=[google_search_tool, exit_loop],
    instruction=f"""
    You are a cost-cutting expert. You have received an evaluation in the {{evaluation}} variable.

    Your task:
    1. Check the 'critique' field in the {{evaluation}}.
    2. IF the critique is '{COMPLETION_PHRASE}', you MUST call the `exit_loop` tool.
    3. ELSE, the plan is over budget. The plan to modify is in the 'cheapest_plan' field of {{evaluation}}.
    4. Read the 'critique' to identify which item to replace.
    5. Use your search tool to find a single, cheaper alternative for that one item.
    6. Output a new, complete JSON plan with this one change, keeping the other items the same.
    """,
    output_key="current_plan"
)

from pydantic import BaseModel, Field

# Define the structure of the communication agent's output.
class EmailDraft(BaseModel):
  """A model to hold the components of a draft email."""
  subject: str = Field(description="The compelling subject line for the email.")
  body: str = Field(description="The full, well-formatted body of the email.")

# --- Communication Agent ---
communications_agent = Agent(
    name="communications_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are a communications expert. Take the event plan from {{current_plan}}.

    Your task is to draft a professional announcement email and format it as a JSON object.
    The JSON object must have two keys: "subject" and "body".

    **CRITICAL: Your entire output must be ONLY the raw JSON object. It must start with `{` and end with `}`. Do not include ```json or any other text, introductions, or formatting.**

    Example of required output format:
    {
      "subject": "📢 Announcing Our Exclusive AI Tech Meetup!",
      "body": "Dear AI Enthusiast,\\n\\nGet ready to connect, learn, and innovate!..."
    }
    """,
    output_key="email_draft",
    output_schema=EmailDraft
)

# --- Final Reporting Agent ---
final_report_agent = Agent(
    name="final_report_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are an expert project assistant compiling a final event plan for a client.
    Your tone should be professional, clear, and confident.

    You have access to the following information:
    - `{{current_plan}}`: The final, budget-approved plan with one vendor for each category.
    - `{{venue_options}}`, `{{catering_options}}`, `{{entertainment_options}}`: The original lists of all vendors that were scouted.
    - `{{budget}}`: The client's initial budget.

    Your task is to generate a comprehensive markdown report that follows this exact structure:

    1.  **Executive Summary:** Start with a brief paragraph confirming the event details (e.g., event type, city) and state that a cost-effective plan has been found within the budget of ${{budget}}.
    2.  **Approved Plan & Cost:** Create a section that clearly lists the single, approved vendor for the Venue, Catering, and Entertainment from `{{current_plan}}`, along with their individual costs. Calculate and display the total final cost.
    3.  **Alternative Vendor Options:** Create a section that lists the *other* vendors that were considered from `{{venue_options}}`, `{{catering_options}}`, and `{{entertainment_options}}`. This gives the client extra options for their reference.
    4.  **Next Steps:** Conclude the report with a brief, professional statement about next steps (e.g., "The next steps would be to contact these vendors to finalize bookings.").

    Your entire output must be only the markdown report. Do not add any other conversational text.
    """,
)

# --- Parallel Logistics Scout Workflow ---
parallel_logistics_scout = ParallelAgent(
    name="parallel_logistics_scout",
    sub_agents=[venue_scout_agent, catering_scout_agent, entertainment_scout_agent]
)

initial_planning_workflow = SequentialAgent(
    name="initial_planning_workflow",
    sub_agents=[parallel_logistics_scout, initial_plan_synthesizer_agent]
)


# --- Budget Optimizer Workflow (no proposer) ---
budget_refinement_loop = LoopAgent(
    name="budget_refinement_loop",
    sub_agents=[accountant_agent, cost_cutter_agent],
    max_iterations=3
)
budget_optimizer_workflow = SequentialAgent(
    name="budget_optimizer_workflow",
    sub_agents=[budget_refinement_loop]
)

# --- Full Autonomous Planning Workflow ---
full_plan_workflow = SequentialAgent(
    name="full_plan_workflow",
    sub_agents=[
        intake_agent,
        initial_planning_workflow,
        budget_optimizer_workflow,
        final_report_agent
    ]
)

# --- Wrap all necessary agents/workflows as tools ---
full_plan_workflow_tool = AgentTool(agent=full_plan_workflow)
guest_list_manager_tool = AgentTool(agent=guest_management_agent)
communications_tool = AgentTool(agent=communications_agent)

# --- The Master Orchestrator ---
master_orchestrator_agent = Agent(
    name="master_orchestrator_agent",
    model="gemini-2.5-flash",
    instruction="""
    You are the master event planning assistant. Delegate tasks to the correct tool.
    - For high-level planning requests (budgeting, finding vendors), use `full_plan_workflow_tool`.
    - For simple guest management (add, view), use `guest_list_manager_tool`.
    - To draft an announcement email, use `communications_tool`.
    - To send the final email, use `send_mock_email`.

    - **IMPORTANT**: When the `communications_tool` is used, its output will be a JSON object with a 'subject' and a 'body'. You MUST format this into a clean, human-readable email draft for the user. Do not just show the raw JSON.
    """,
    tools=[
        full_plan_workflow_tool,
        guest_list_manager_tool,
        communications_tool,
        send_mock_email
    ]
)

root_agent = master_orchestrator_agent