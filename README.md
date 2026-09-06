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
