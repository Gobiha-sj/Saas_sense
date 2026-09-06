# SAAS-SENSE

## AI-Powered Autonomous SaaS Subscription Waste Detection and Optimization Agent

SAAS-SENSE is an AI-powered autonomous agent that helps organizations identify unnecessary SaaS subscription expenses and recommend cost-saving actions.

## Problem Statement

Organizations often waste money on SaaS subscriptions because of:

- Unused licenses
- Low-usage licenses
- Licenses assigned to employees who have left
- Expensive subscription plans
- Duplicate subscriptions
- Upcoming renewals with low usage

Manually identifying these issues is time-consuming.

## Objective

The objectives of SAAS-SENSE are:

1. Identify potentially wasted SaaS subscriptions.
2. Analyze subscription usage.
3. Calculate estimated financial waste.
4. Analyze contract information.
5. Identify upcoming renewals.
6. Use previous decisions through persistent memory.
7. Provide context-aware recommendations.
8. Estimate potential savings.

## Proposed Solution

SAAS-SENSE uses an LLM-based autonomous agent to investigate SaaS subscription waste.

The agent can:

User Question
    ↓
LLM
    ↓
Select Required Tools
    ↓
Analyze Subscription Data
    ↓
Check Usage
    ↓
Check Cost and Contract
    ↓
Check Renewal
    ↓
Check Previous Decisions
    ↓
Generate Recommendation
    ↓
Save Investigation to Memory

## Key Innovation

Low usage does not automatically mean that a subscription should be cancelled.

The agent considers:

- Employee
- Department
- Usage
- Cost
- Plan
- Features Used
- Contract
- Renewal Date
- Previous Decisions

This provides context-aware recommendations.

## LLM Component

The LLM component is implemented in `agent.py`.

Model:

`OpenAI GPT-5.6 Luna`

The LLM:

- Understands the user's question
- Selects appropriate tools
- Analyzes tool results
- Performs multi-step investigation
- Generates recommendations
- Provides confidence levels
- Saves decisions to memory

## ReAct Agent

The project follows a ReAct-style workflow:

Reason → Action → Observation → Reason → Action → Final Answer

The agent can decide which tools to use based on the user's question.

## Tools Used

SAAS-SENSE contains six custom tools:

| Tool | Purpose |
|------|---------|
| `subscription_search()` | Searches subscription information |
| `analyze_usage()` | Analyzes SaaS usage |
| `calculate_waste()` | Calculates estimated waste |
| `renewal_analysis()` | Finds upcoming renewals |
| `contract_analysis()` | Analyzes contract information |
| `memory_search()` | Searches previous investigations |

## Memory

SAAS-SENSE uses persistent memory stored in:

`agent_memory.db`

The memory stores:

- Previous questions
- Investigation details
- Decisions
- Timestamps

This allows the agent to use previous decisions during future investigations.

## Database

The project uses SQLite.

Main database:

`saas_data.db`

Tables:

- `subscriptions`
- `employees`
- `contracts`

## Project Structure

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

## File Description

| File | Description |
|------|-------------|
| `main.py` | Main application and user interface |
| `agent.py` | LLM integration, agent logic and ReAct loop |
| `tools.py` | Six custom SaaS analysis tools |
| `memory.py` | Persistent agent memory |
| `database.py` | SQLite database and sample data |
| `requirements.txt` | Required Python packages |
| `.env` | Stores the OpenAI API key |

## Technologies Used

- Python
- OpenAI GPT-5.6 Luna
- OpenAI Responses API
- Function Calling
- ReAct Agent Architecture
- SQLite
- Python-dotenv
- Agentic AI
- Persistent Memory

## Requirements

- Python 3.10+
- OpenAI API Key

Required packages:

openai
python-dotenv

## Installation

### 1. Open the Project

Open the project folder in VS Code.

### 2. Open Terminal

Run:

`cd saas_waste_agent`

### 3. Install Dependencies

Run:

`pip install -r requirements.txt`

## API Key Configuration

Create a `.env` file in the project directory.

Add:

`OPENAI_API_KEY=your_actual_api_key`

Do not share your API key or upload it to GitHub.

Add `.env` to `.gitignore`.

## Initialize Database

Run:

`python database.py`

This creates and populates the SQLite database.

## Run the Project

Run:

`python main.py`

The application will display:

SAAS-SENSE
Autonomous SaaS Optimization Agent

Ask a question about your SaaS subscriptions.

## Example Questions

Which subscriptions have the highest waste?

Which licenses are completely unused?

Show me all subscriptions with low usage.

How much money is being wasted every month?

How much money could the company save annually?

Which subscriptions are renewing within 30 days?

Which subscriptions should we review before renewal?

Find upcoming renewals and estimate potential savings.

Analyze all SaaS subscriptions and identify the biggest sources of waste.

## Recommendation Types

The agent can recommend:

### RETAIN

The subscription is actively required.

### REVIEW

More investigation or human approval is required.

### DOWNGRADE

A cheaper plan may be sufficient.

### RECLAIM

The license may be reassigned or recovered.

### CANCEL

The subscription appears unnecessary based on the available evidence.

The current prototype does not automatically cancel subscriptions.

## Waste Detection

The prototype estimates waste based on monthly login activity.

0 logins:

UNUSED

1-3 logins:

VERY_LOW_USAGE

4-10 logins:

LOW_USAGE

More than 10 logins:

NORMAL_USAGE

These are prototype estimation rules and can be replaced with organization-specific policies.

## Example Use Case

Suppose Rahul has an Adobe Creative Cloud Enterprise subscription.

Employee: Rahul
Application: Adobe Creative Cloud
Plan: Enterprise
Monthly Cost: ₹3500
Monthly Logins: 2

The agent does not immediately recommend cancellation.

It investigates:

Usage
    ↓
Employee
    ↓
Department
    ↓
Features Used
    ↓
Contract
    ↓
Renewal
    ↓
Previous Decisions

It may then recommend:

REVIEW

This demonstrates context-aware decision making.

## Agent Architecture

User
 ↓
main.py
 ↓
agent.py
 ↓
OpenAI LLM
 ↓
Tool Selection
 ↓
tools.py
 ↓
SQLite Database
 ↓
Tool Results
 ↓
LLM Analysis
 ↓
Final Recommendation
 ↓
memory.py
 ↓
agent_memory.db

## Why LLM?

The LLM provides:

- Natural language understanding
- Dynamic tool selection
- Multi-step reasoning
- Context understanding
- Evidence-based recommendations
- Explainable results
- Memory-based reasoning

## Why Agentic AI?

The system follows:

Observe → Decide → Act → Observe Again → Remember

The agent can independently decide which tools are required instead of requiring the user to manually perform every step.

## Security

- API keys are stored in `.env`.
- API keys are not hard-coded.
- `.env` should not be uploaded to GitHub.
- Organizational data should be protected.
- High-impact actions should require human approval.
- The current prototype does not automatically cancel subscriptions.

## Limitations

The current prototype:

1. Uses sample SaaS data.
2. Uses SQLite.
3. Uses rule-based waste estimation.
4. Does not directly connect to SaaS provider APIs.
5. Does not automatically cancel subscriptions.
6. Does not integrate with HR systems.
7. Does not integrate with finance systems.
8. Uses simple text-based memory search.

## Future Enhancements

- Real-time SaaS API integration
- HR system integration
- Finance and procurement integration
- Email and approval automation
- Web dashboard
- Real-time usage monitoring
- Vector-based memory
- Semantic search
- Human-in-the-loop approval
- Automatic license reclamation

## Benefits

SAAS-SENSE can help organizations:

- Reduce unnecessary SaaS spending
- Identify unused licenses
- Improve license utilization
- Detect renewal risks
- Identify downgrade opportunities
- Support procurement decisions
- Reduce manual auditing effort
- Maintain historical decisions
- Provide explainable recommendations

## Conclusion

SAAS-SENSE is an autonomous AI agent that investigates SaaS subscription usage, costs, contracts, renewals, and previous decisions to identify potential waste and recommend cost-saving actions.

The project demonstrates the practical application of:

- Large Language Models
- Agentic AI
- ReAct
- Function Calling
- Custom Tools
- Database Integration
- Persistent Memory
- Context-Aware Decision Making

## License

This project is developed for educational and academic purposes.

## Project Name

SAAS-SENSE

AI-Powered Autonomous SaaS Subscription Waste Detection and Optimization Agent
