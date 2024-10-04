# for ipynb

# %%
!pip show openai

# %%
import json

def show_json(obj):
    display(json.loads(obj.model_dump_json()))

# %%
from openai import OpenAI

client = OpenAI(api_key='...')

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a personal math tutor. Answer questions briefly, in a sentence or less.",
    model="gpt-4-1106-preview",
)
show_json(assistant)

# %%
thread = client.beta.threads.create()
show_json(thread)

# %%
thread

# %%
message = client.beta.threads.messages.create(
    thread_id=thread.id,
    role="user",
    content="I need to solve the equation `3x + 11 = 14`. Can you help me?",
)
show_json(message)

# %% [markdown]
# Notice how the Thread we created is not associated with the Assistant we created earlier! Threads exist independently from Assistants, which may be different from what you'd expect if you've used ChatGPT (where a thread is tied to a model/GPT).
# 
# * thread -> message
# * assistant with model and instruction
# * run: thread & thread

# %%
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)
show_json(run)

# %%
import time

def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run

# %%
run = wait_on_run(run, thread)
show_json(run)

# %%
messages = client.beta.threads.messages.list(thread_id=thread.id)
show_json(messages)

# %%
# Create a message to append to our thread
message = client.beta.threads.messages.create(
    thread_id=thread.id, role="user", content="Could you explain this to me?"
)

# Execute our run
run = client.beta.threads.runs.create(
    thread_id=thread.id,
    assistant_id=assistant.id,
)

# Wait for completion
wait_on_run(run, thread)

# Retrieve all the messages added after our last user message
messages = client.beta.threads.messages.list(
    thread_id=thread.id, order="asc", after=message.id
)
show_json(messages)

# %%
MATH_ASSISTANT_ID = assistant.id


def submit_message(assistant_id, thread, user_message):
    client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    )


def get_response(thread):
    return client.beta.threads.messages.list(thread_id=thread.id, order="asc")


# Pretty printing helper
def pretty_print(messages):
    print("# Messages")
    for m in messages:
        print(f"[{m.role}]:  {m.content[0].text.value}")
    print()

# %%
show_json(thread)

for user_message in [
    "I need to solve the equation `3x + 11 = 14`. Can you help me?",
    "Could you explain linear algebra to me?",
    "I don't like math. What can I do?"]:
    print(f"\n=== {user_message} ===\n")
    # Wait for Run
    run = submit_message(MATH_ASSISTANT_ID, thread, user_message=user_message)
    run = wait_on_run(run, thread)
    pretty_print(get_response(thread))

# %%
def create_thread_and_run(user_input):
    thread = client.beta.threads.create()
    run = submit_message(MATH_ASSISTANT_ID, thread, user_input)
    return thread, run


# Emulating concurrent user requests
thread1, run1 = create_thread_and_run(
    "I need to solve the equation `3x + 11 = 14`. Can you help me?"
)
thread2, run2 = create_thread_and_run()
thread3, run3 = create_thread_and_run()

# %%
!ls ~/Downloads/_逝去的武林.pdf

# %%


# %%
def print_obj(obj):
    display(json.loads(obj.model_dump_json()))


def wait_on_run(run, thread):
    while run.status == "queued" or run.status == "in_progress":
        run = client.beta.threads.runs.retrieve(
            thread_id=thread.id,
            run_id=run.id,
        )
        time.sleep(0.5)
    return run


def ask_assistant(assistant_id, thread, user_message):
    msg = client.beta.threads.messages.create(
        thread_id=thread.id, role="user", content=user_message
    )
    return client.beta.threads.runs.create(
        thread_id=thread.id,
        assistant_id=assistant_id,
    ), msg


# Pretty printing helper
def format_response(thread, message):
    messages = client.beta.threads.messages.list(thread_id=thread.id, order='asc', after=message.id)
    for m in messages:
        print(f"\n{m.role}:  {m.content[0].text.value}\n")
    print()


# %%
client = OpenAI(api_key='...')


file = client.files.create(
    file=open('/Users/bytedance/mydoc/逝去的武林.txt', 'rb'),
    purpose='assistants',
)
# print(file.id)

# create assistant
assistant = client.beta.assistants.create(
    name='read lover',
    instructions='You like reading and sharing what you have learned. Answer questions in a comprehensive way with necessary details.',
    model='gpt-4-1106-preview',
    tools=[{'type': 'retrieval'}],
    file_ids=[file.id],
)
# print_obj(assistant)

ASSISTANT_ID = assistant.id

# create thread
thread = client.beta.threads.create()

for user_message in [
    "逝去的武林这本小说主要讲什么内容?",
    "书中的主要人物有哪些?",
    "孙禄堂是谁?"]:
    print(f"\nuser: {user_message}\n")

    run, msg = ask_assistant(ASSISTANT_ID, thread, user_message=user_message)
    run = wait_on_run(run, thread)
    format_response(thread, msg)

# %%



