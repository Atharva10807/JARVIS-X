from app.core.jarvis import Jarvis


def main():
    print("JARVIS-X")
    print("System initialized.")
    print("Type 'exit' to shut down.\n")

    jarvis = Jarvis()

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("JARVIS: Shutting down. Goodbye.")
            break

        try:
            response = jarvis.respond(user_input)
            print(f"JARVIS: {response}")
        except Exception as error:
            print(f"JARVIS: Sorry, I encountered an error: {error}")


if __name__ == "__main__":
    main()