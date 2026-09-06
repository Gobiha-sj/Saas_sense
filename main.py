from database import initialize_database
from memory import initialize_memory
from agent import run_agent

def main():
    initialize_database()
    initialize_memory()

    print()
    print("=" * 72)
    print("                         SAAS-SENSE")
    print("             Autonomous SaaS Optimization Agent")
    print("=" * 72)
    print()
    print("Ask a question about your SaaS subscriptions.")
    print("Type 'exit' to close the application.")
    print()

    while True:
        question = input("You: ").strip()

        if question.lower() in ("exit", "quit"):
            print("\nSAAS-SENSE closed.")
            break

        if not question:
            continue

        print()
        print("Analyzing your request...")
        print()

        try:
            answer = run_agent(question)

            print("-" * 72)
            print("SAAS-SENSE ANALYSIS")
            print("-" * 72)
            print(answer)
            print("-" * 72)
            print()

        except Exception as e:
            print()
            print("ERROR")
            print(str(e))
            print()

if __name__ == "__main__":
    main()