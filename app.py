import os
import openai


def check_openai_api_key():
    if not os.environ.get("OPENAI_API_KEY"):
        print("Error: Environment variable 'OPENAI_API_KEY' is not set.")
        exit(1)


def generate_response(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        max_tokens=2000,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(f"\n> Sending request to agent\n\n{messages}")
    response = response.choices[0].message['content'].strip()
    print(f"\n> Received response from agent\n\n{response}")

    return response


def main():
    check_openai_api_key()

    user_msg = input("Ask a question: ")
    prefixed_msg = f"Question. {user_msg} Answer: Let's work this " \
                   f"out in a step by step way to be sure we have " \
                   f"the right answer."

    def generate_response_user(message):
        return generate_response([{"role": "user", "content": prefixed_msg}])

    answers = [
        f"Answer Option {i + 1}: {generate_response_user(prefixed_msg)}"
        for i in range(3)
    ]

    researcher_prompt = f"{user_msg}\n\n" + "\n".join(answers)
    researcher_prompt += "\n\nYou are a researcher tasked with " \
                         "investigating the three answer options " \
                         "provided. List the flaws and faulty logic " \
                         "of each answer option. Let's think step " \
                         "by step."

    researcher_response = generate_response([
        {"role": "user", "content": prefixed_msg},
        {"role": "assistant", "content": "\n".join(answers)},
        {"role": "user", "content": researcher_prompt},
    ])

    resolver_prompt = "You are a resolver tasked with 1) finding " \
                      "which of the 3 answer options the researcher " \
                      "thought was best, 2) improving that answer, " \
                      "and 3) printing out the improved answer in " \
                      "full. Let's work this out in a step by step way " \
                      "to be sure we have the right answer: "

    resolver_response = generate_response([
        {"role": "user", "content": prefixed_msg},
        {"role": "assistant", "content": "\n".join(answers)},
        {"role": "user", "content": researcher_prompt},
        {"role": "assistant", "content": researcher_response},
        {"role": "user", "content": resolver_prompt},
    ])

    print("\n\n======AGENT RESPONSE======\n\n")
    print(resolver_response)


if __name__ == '__main__':
    main()
