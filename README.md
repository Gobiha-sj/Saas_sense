# Saas_sense
# SAAS-SENSE

## AI-Powered Autonomous SaaS Subscription Waste Detection and Optimization Agent

SAAS-SENSE is an AI-powered autonomous agent that helps organizations identify and reduce unnecessary SaaS subscription expenses.

The system analyzes subscription usage, employee information, costs, contracts, renewal dates, and previous decisions. It then investigates potential waste and provides recommendations such as Retain, Review, Downgrade, Reclaim, or Cancel.

---

## Problem Statement

Organizations often spend money on SaaS licenses that are:

- Completely unused
- Used very rarely
- Assigned to employees who have left
- More expensive than required
- Duplicated across departments
- Approaching renewal despite low usage

Manually identifying these issues across multiple SaaS applications is time-consuming.

---

## Proposed Solution

SAAS-SENSE uses an LLM-based autonomous agent to investigate SaaS subscription waste.

Instead of simply identifying low usage, the agent considers multiple factors before making a recommendation.

The agent can analyze:

- Subscription usage
- Monthly subscription cost
- Employee and department
- License plan
- Contract information
- Renewal dates
- Previous investigation decisions

---

## Key Innovation

The main innovation of SAAS-SENSE is **context-aware SaaS waste detection**.

Low usage does not automatically mean that a subscription should be cancelled.

The agent investigates the reason behind low usage and considers factors such as:

- Employee role
- Department
- Plan
- Cost
- Contract
- Renewal date
- Previous decisions

This allows the system to provide more meaningful recommendations instead of relying only on login counts.

---

## LLM Component

The project uses **OpenAI GPT-5.6 Luna** as the Large Language Model.

The LLM is implemented in `agent.py`.

The LLM:

1. Receives the user's question.
2. Decides which tools are required.
3. Calls the appropriate tools.
4. Analyzes the returned information.
5. Performs additional investigation when required.
6. Generates the final recommendation.
7. Saves the investigation to memory.

---

## Agent Workflow

The agent follows a ReAct-style workflow:

```text
User Question
      |
      v
     LLM
      |
      v
Select Appropriate Tool
      |
      v
Execute Tool
      |
      v
Database / Memory
      |
      v
Tool Result
      |
      v
     LLM
      |
      v
Further Investigation
      |
      v
Final Recommendation
      |
      v
Save Decision to Memory
The basic process is:

Reason -> Action -> Observation -> Reason -> Final Answer

Tools Used

The agent contains six custom tools.

Tool	Purpose
subscription_search()	Searches subscription information by application or department
analyze_usage()	Analyzes license usage and login frequency
calculate_waste()	Estimates monthly and annual subscription waste
renewal_analysis()	Finds subscriptions approaching renewal
contract_analysis()	Checks contract and licensing information
memory_search()	Searches previous investigations and decisions
Memory

SAAS-SENSE uses persistent memory to remember previous investigations.

The memory is stored in:

agent_memory.db

The system stores:

Previous questions
Investigation details
Decisions
Timestamps

This allows the agent to use previous decisions when analyzing similar subscriptions.

Database

The project uses SQLite for storing SaaS information.

Main database:

saas_data.db

The database contains:

subscriptions
employees
contracts
Subscriptions

Stores information such as:

Application
Employee
Department
Plan
Monthly cost
Login frequency
Features used
Renewal date
Owner
Employees

Stores:

Employee name
Department
Employment status
Contracts

Stores:

Application
Plan
Minimum licenses
Renewal date
Annual cost
Cancellation notice period
Project Structure
saas_waste_agent/
│
├── main.py
├── agent.py
├── tools.py
├── memory.py
├── database.py
├── requirements.txt
├── .env
│
├── saas_data.db
└── agent_memory.db
File Description
File	Description
main.py	Main application and user interface
agent.py	LLM, agent logic, tool calling and ReAct loop
tools.py	Custom SaaS analysis tools
memory.py	Persistent agent memory
database.py	Database creation and sample data
requirements.txt	Required Python packages
.env	Stores the OpenAI API key
Technologies Used
Python
OpenAI GPT-5.6 Luna
OpenAI Responses API
Function Calling
ReAct Agent Architecture
SQLite
Python-dotenv
Installation
1. Open the Project

Open the project folder in VS Code or another Python IDE.

2. Install Dependencies
pip install -r requirements.txt
3. Configure the API Key

Create a .env file in the project folder:

OPENAI_API_KEY=your_actual_api_key

Do not share your API key or upload it to GitHub.

4. Initialize the Database

Run:

python database.py

This creates and populates the SQLite database.

5. Run the Application
python main.py
Example Questions

After starting the application, you can ask questions such as:

Which subscriptions have the highest waste?
Which licenses are completely unused?
Show me all subscriptions with low usage.
How much money is being wasted every month?
How much money could the company save annually?
Which subscriptions are renewing within 30 days?
Which subscriptions should we review before renewal?
Analyze all SaaS subscriptions and identify the biggest sources of waste.
Find unused licenses and check their contract information before recommending action.
Example Agent Output
------------------------------------------------------------------------
SAAS-SENSE ANALYSIS
------------------------------------------------------------------------

FINDING
A potentially wasteful SaaS subscription was identified.

EVIDENCE
• Monthly usage is very low.
• The subscription has an active paid plan.
• The subscription has an upcoming renewal.
• Contract information was reviewed.

RECOMMENDATION
Review the subscription for downgrade, reassignment, or cancellation.

ESTIMATED SAVINGS
Monthly: Calculated based on subscription cost
Annual: Calculated based on estimated monthly savings

CONFIDENCE
Medium - recommendation is based on usage and contract evidence.

------------------------------------------------------------------------
Autonomous Agent

SAAS-SENSE is autonomous because the user does not need to manually select every analysis step.

For example:

User:
"Find the biggest sources of SaaS waste."

        ↓

Agent decides to:

Search subscriptions
        ↓
Analyze usage
        ↓
Calculate waste
        ↓
Check contracts
        ↓
Check renewals
        ↓
Search previous decisions
        ↓
Generate recommendation

The agent decides which tools are useful based on the question.

The current version is an autonomous decision-support system. It does not automatically cancel subscriptions. Human approval can be required for high-impact actions.

Sample Waste Categories

SAAS-SENSE can identify:

Unused licenses
Low-usage licenses
Very-low-usage licenses
Potentially expensive waste
Orphaned subscriptions
Upcoming renewal risks
Possible downgrade opportunities
Potential license reclamation opportunities
Security
API keys are stored in .env.
API keys are not hard-coded in the source code.
Sensitive organizational data should be protected.
High-impact actions should require human approval.
The current prototype does not automatically cancel subscriptions.
Limitations

The current prototype uses:

Sample SQLite data
Rule-based waste estimation
Simulated SaaS subscription information
No direct SaaS provider integrations
No automatic subscription cancellation
Future Enhancements

Future versions can include:

Real-time SaaS API integrations
HR system integration
Finance and procurement integration
Email and approval automation
Web dashboard
Real-time usage monitoring
Advanced vector-based memory
Human-in-the-loop approval workflow
Automatic license reclamation
SaaS vendor comparison and consolidation
Project Architecture
                  +----------------+
                  |     USER       |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  |    main.py     |
                  +-------+--------+
                          |
                          v
                  +----------------+
                  |    agent.py    |
                  |   LLM + ReAct  |
                  +-------+--------+
                          |
             +------------+------------+
             |            |            |
             v            v            v
        +---------+  +---------+  +---------+
        | Tools   |  | Memory  |  |  LLM    |
        |tools.py |  |memory.py|  | OpenAI  |
        +----+----+  +----+----+  +---------+
             |            |
             v            v
        +---------+  +-------------+
        | SQLite  |  | Agent       |
        | Database|  | Memory DB   |
        +---------+  +-------------+
             |
             v
      +----------------+
      | Recommendation |
      +----------------+
Expected Benefits

SAAS-SENSE can help organizations:

Reduce unnecessary SaaS spending
Identify unused licenses
Improve license utilization
Detect renewal risks
Support better procurement decisions
Provide explainable recommendations
Reduce manual SaaS auditing effort
