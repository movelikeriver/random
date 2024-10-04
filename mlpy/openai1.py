# for ipynb

# %% [markdown]
# # openai exercise
# 
# https://learn.deeplearning.ai/chatgpt-prompt-eng/lesson/2/guidelines
# 
# setup
# 
# create a new conda env
# 
# ```
# conda install openai
# conda install jupyterlab
# conda install python-dotenv
# ```
# 
# 

# %%
import openai
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv())

openai.api_key  = os.getenv('OPENAI_API_KEY')

# %%


# %%
!OPENAI_API_KEY=sk-.....

# %%
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

# %%
import os
import openai

os.environ['OPENAI_API_KEY'] = 'sk-....'

openai.api_key = os.getenv('OPENAI_API_KEY')
print(openai.api_key)

response = openai.Completion.create(
  model="text-davinci-003",
  prompt="I am a highly intelligent question answering bot. If you ask me a question that is rooted in truth, I will give you the answer. If you ask me a question that is nonsense, trickery, or has no clear answer, I will respond with \"Unknown\".\n\nQ: What is human life expectancy in the United States?\nA: Human life expectancy in the United States is 78 years.\n\nQ: Who was president of the United States in 1955?\nA: Dwight D. Eisenhower was president of the United States in 1955.\n\nQ: Which party did he belong to?\nA: He belonged to the Republican Party.\n\nQ: What is the square root of banana?\nA: Unknown\n\nQ: How does a telescope work?\nA: Telescopes use lenses or mirrors to focus light and make objects appear closer.\n\nQ: Where were the 1992 Olympics held?\nA: The 1992 Olympics were held in Barcelona, Spain.\n\nQ: How many squigs are in a bonk?\nA: Unknown\n\nQ: Where is the Valley of Kings?\nA:",
  temperature=0,
  max_tokens=100,
  top_p=1,
  frequency_penalty=0.0,
  presence_penalty=0.0,
  stop=["\n"]
)

# %%
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""

print(prompt)


# %%


# %%
text = f"""
You should express what you want a model to do by \ 
providing instructions that are as clear and \ 
specific as you can possibly make them. \ 
This will guide the model towards the desired output, \ 
and reduce the chances of receiving irrelevant \ 
or incorrect responses. Don't confuse writing a \ 
clear prompt with writing a short prompt. \ 
In many cases, longer prompts provide more clarity \ 
and context for the model, which can lead to \ 
more detailed and relevant outputs.
"""
prompt = f"""
Summarize the text delimited by triple backticks \ 
into a single sentence.
```{text}```
"""
response = get_completion(prompt)
print(response)

# %%
prompt = f"""
Generate a list of three made-up book titles along \ 
with their authors and genres. 
Provide them in JSON format with the following keys: 
book_id, title, author, genre.
"""
response = get_completion(prompt)
print(response)

# %%
text_1 = f"""
Making a cup of tea is easy! First, you need to get some \ 
water boiling. While that's happening, \ 
grab a cup and put a tea bag in it. Once the water is \ 
hot enough, just pour it over the tea bag. \ 
Let it sit for a bit so the tea can steep. After a \ 
few minutes, take out the tea bag. If you \ 
like, you can add some sugar or milk to taste. \ 
And that's it! You've got yourself a delicious \ 
cup of tea to enjoy.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_1}\"\"\"
"""
response = get_completion(prompt)
print("Completion for Text 1:")
print(response)

# %%
text_2 = f"""
The sun is shining brightly today, and the birds are \
singing. It's a beautiful day to go for a \ 
walk in the park. The flowers are blooming, and the \ 
trees are swaying gently in the breeze. People \ 
are out and about, enjoying the lovely weather. \ 
Some are having picnics, while others are playing \ 
games or simply relaxing on the grass. It's a \ 
perfect day to spend time outdoors and appreciate the \ 
beauty of nature.
"""
prompt = f"""
You will be provided with text delimited by triple quotes. 
If it contains a sequence of instructions, \ 
re-write those instructions in the following format:

Step 1 - ...
Step 2 - …
…
Step N - …

If the text does not contain a sequence of instructions, \ 
then simply write \"No steps provided.\"

\"\"\"{text_2}\"\"\"
"""
response = get_completion(prompt)
print("Completion for Text 2:")
print(response)

# %%
prompt = f"""
Your task is to answer in a consistent style.

<child>: Teach me about patience.

<grandparent>: The river that carves the deepest \ 
valley flows from a modest spring; the \ 
grandest symphony originates from a single note; \ 
the most intricate tapestry begins with a solitary thread.

<child>: Teach me about resilience.
"""
response = get_completion(prompt)
print(response)

# %%
text = f"""
In a charming village, siblings Jack and Jill set out on \ 
a quest to fetch water from a hilltop \ 
well. As they climbed, singing joyfully, misfortune \ 
struck—Jack tripped on a stone and tumbled \ 
down the hill, with Jill following suit. \ 
Though slightly battered, the pair returned home to \ 
comforting embraces. Despite the mishap, \ 
their adventurous spirits remained undimmed, and they \ 
continued exploring with delight.
"""
# example 1
prompt_1 = f"""
Perform the following actions: 
1 - Summarize the following text delimited by triple \
backticks with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the following \
keys: french_summary, num_names.

Separate your answers with line breaks.

Text:
```{text}```
"""
response = get_completion(prompt_1)
print("Completion for prompt 1:")
print(response)

# %%
prompt_2 = f"""
Your task is to perform the following actions: 
1 - Summarize the following text delimited by 
  <> with 1 sentence.
2 - Translate the summary into French.
3 - List each name in the French summary.
4 - Output a json object that contains the 
  following keys: french_summary, num_names.

Use the following format:
Text: <text to summarize>
Summary: <summary>
Translation: <summary translation>
Names: <list of names in Italian summary>
Output JSON: <json with summary and num_names>

Text: <{text}>
"""
response = get_completion(prompt_2)
print("\nCompletion for prompt 2:")
print(response)

# %%
prompt = f"""
Determine if the student's solution is correct or not.

Question:
I'm building a solar power installation and I need \
 help working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \ 
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations 
as a function of the number of square feet.

Student's Solution:
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
"""
response = get_completion(prompt)
print(response)

# %%
prompt = f"""
Your task is to determine if the student's solution \
is correct or not.
To solve the problem do the following:
- First, work out your own solution to the problem. 
- Then compare your solution to the student's solution \ 
and evaluate if the student's solution is correct or not. 
Don't decide if the student's solution is correct until 
you have done the problem yourself.

Use the following format:
Question:
```
question here
```
Student's solution:
```
student's solution here
```
Actual solution:
```
steps to work out the solution and your solution here
```
Is the student's solution the same as actual solution \
just calculated:
```
yes or no
```
Student grade:
```
correct or incorrect
```

Question:
```
I'm building a solar power installation and I need help \
working out the financials. 
- Land costs $100 / square foot
- I can buy solar panels for $250 / square foot
- I negotiated a contract for maintenance that will cost \
me a flat $100k per year, and an additional $10 / square \
foot
What is the total cost for the first year of operations \
as a function of the number of square feet.
``` 
Student's solution:
```
Let x be the size of the installation in square feet.
Costs:
1. Land cost: 100x
2. Solar panel cost: 250x
3. Maintenance cost: 100,000 + 100x
Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
```
Actual solution:
"""
response = get_completion(prompt)
print(response)

# %%
prompt = f"""
Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
"""
response = get_completion(prompt)
print(response)

# %% [markdown]
# # Guidelines for Prompting
# In this lesson, you'll practice two prompting principles and their related tactics in order to write effective prompts for large language models.
# 
# ## Setup
# #### Load the API key and relevant Python libaries.
# 
# In this course, we've provided some code that loads the OpenAI API key for you.
# 
# import openai
# import os
# 
# from dotenv import load_dotenv, find_dotenv
# _ = load_dotenv(find_dotenv())
# 
# openai.api_key  = os.getenv('OPENAI_API_KEY')
# 
# #### helper function
# Throughout this course, we will use OpenAI's `gpt-3.5-turbo` model and the [chat completions endpoint](https://platform.openai.com/docs/guides/chat). 
# 
# This helper function will make it easier to use prompts and look at the generated outputs:
# 
# def get_completion(prompt, model="gpt-3.5-turbo"):
#     messages = [{"role": "user", "content": prompt}]
#     response = openai.ChatCompletion.create(
#         model=model,
#         messages=messages,
#         temperature=0, # this is the degree of randomness of the model's output
#     )
#     return response.choices[0].message["content"]
# 
# ## Prompting Principles
# - **Principle 1: Write clear and specific instructions**
# - **Principle 2: Give the model time to “think”**
# 
# ### Tactics
# 
# #### Tactic 1: Use delimiters to clearly indicate distinct parts of the input
# - Delimiters can be anything like: ```, """, < >, `<tag> </tag>`, `:`
# 
# text = f"""
# You should express what you want a model to do by \ 
# providing instructions that are as clear and \ 
# specific as you can possibly make them. \ 
# This will guide the model towards the desired output, \ 
# and reduce the chances of receiving irrelevant \ 
# or incorrect responses. Don't confuse writing a \ 
# clear prompt with writing a short prompt. \ 
# In many cases, longer prompts provide more clarity \ 
# and context for the model, which can lead to \ 
# more detailed and relevant outputs.
# """
# prompt = f"""
# Summarize the text delimited by triple backticks \ 
# into a single sentence.
# ```{text}```
# """
# response = get_completion(prompt)
# print(response)
# 
# #### Tactic 2: Ask for a structured output
# - JSON, HTML
# 
# prompt = f"""
# Generate a list of three made-up book titles along \ 
# with their authors and genres. 
# Provide them in JSON format with the following keys: 
# book_id, title, author, genre.
# """
# response = get_completion(prompt)
# print(response)
# 
# #### Tactic 3: Ask the model to check whether conditions are satisfied
# 
# text_1 = f"""
# Making a cup of tea is easy! First, you need to get some \ 
# water boiling. While that's happening, \ 
# grab a cup and put a tea bag in it. Once the water is \ 
# hot enough, just pour it over the tea bag. \ 
# Let it sit for a bit so the tea can steep. After a \ 
# few minutes, take out the tea bag. If you \ 
# like, you can add some sugar or milk to taste. \ 
# And that's it! You've got yourself a delicious \ 
# cup of tea to enjoy.
# """
# prompt = f"""
# You will be provided with text delimited by triple quotes. 
# If it contains a sequence of instructions, \ 
# re-write those instructions in the following format:
# 
# Step 1 - ...
# Step 2 - …
# …
# Step N - …
# 
# If the text does not contain a sequence of instructions, \ 
# then simply write \"No steps provided.\"
# 
# \"\"\"{text_1}\"\"\"
# """
# response = get_completion(prompt)
# print("Completion for Text 1:")
# print(response)
# 
# text_2 = f"""
# The sun is shining brightly today, and the birds are \
# singing. It's a beautiful day to go for a \ 
# walk in the park. The flowers are blooming, and the \ 
# trees are swaying gently in the breeze. People \ 
# are out and about, enjoying the lovely weather. \ 
# Some are having picnics, while others are playing \ 
# games or simply relaxing on the grass. It's a \ 
# perfect day to spend time outdoors and appreciate the \ 
# beauty of nature.
# """
# prompt = f"""
# You will be provided with text delimited by triple quotes. 
# If it contains a sequence of instructions, \ 
# re-write those instructions in the following format:
# 
# Step 1 - ...
# Step 2 - …
# …
# Step N - …
# 
# If the text does not contain a sequence of instructions, \ 
# then simply write \"No steps provided.\"
# 
# \"\"\"{text_2}\"\"\"
# """
# response = get_completion(prompt)
# print("Completion for Text 2:")
# print(response)
# 
# #### Tactic 4: "Few-shot" prompting
# 
# prompt = f"""
# Your task is to answer in a consistent style.
# 
# <child>: Teach me about patience.
# 
# <grandparent>: The river that carves the deepest \ 
# valley flows from a modest spring; the \ 
# grandest symphony originates from a single note; \ 
# the most intricate tapestry begins with a solitary thread.
# 
# <child>: Teach me about resilience.
# """
# response = get_completion(prompt)
# print(response)
# 
# ### Principle 2: Give the model time to “think” 
# 
# #### Tactic 1: Specify the steps required to complete a task
# 
# text = f"""
# In a charming village, siblings Jack and Jill set out on \ 
# a quest to fetch water from a hilltop \ 
# well. As they climbed, singing joyfully, misfortune \ 
# struck—Jack tripped on a stone and tumbled \ 
# down the hill, with Jill following suit. \ 
# Though slightly battered, the pair returned home to \ 
# comforting embraces. Despite the mishap, \ 
# their adventurous spirits remained undimmed, and they \ 
# continued exploring with delight.
# """
# # example 1
# prompt_1 = f"""
# Perform the following actions: 
# 1 - Summarize the following text delimited by triple \
# backticks with 1 sentence.
# 2 - Translate the summary into French.
# 3 - List each name in the French summary.
# 4 - Output a json object that contains the following \
# keys: french_summary, num_names.
# 
# Separate your answers with line breaks.
# 
# Text:
# ```{text}```
# """
# response = get_completion(prompt_1)
# print("Completion for prompt 1:")
# print(response)
# 
# #### Ask for output in a specified format
# 
# prompt_2 = f"""
# Your task is to perform the following actions: 
# 1 - Summarize the following text delimited by 
#   <> with 1 sentence.
# 2 - Translate the summary into French.
# 3 - List each name in the French summary.
# 4 - Output a json object that contains the 
#   following keys: french_summary, num_names.
# 
# Use the following format:
# Text: <text to summarize>
# Summary: <summary>
# Translation: <summary translation>
# Names: <list of names in Italian summary>
# Output JSON: <json with summary and num_names>
# 
# Text: <{text}>
# """
# response = get_completion(prompt_2)
# print("\nCompletion for prompt 2:")
# print(response)
# 
# #### Tactic 2: Instruct the model to work out its own solution before rushing to a conclusion
# 
# prompt = f"""
# Determine if the student's solution is correct or not.
# 
# Question:
# I'm building a solar power installation and I need \
#  help working out the financials. 
# - Land costs $100 / square foot
# - I can buy solar panels for $250 / square foot
# - I negotiated a contract for maintenance that will cost \ 
# me a flat $100k per year, and an additional $10 / square \
# foot
# What is the total cost for the first year of operations 
# as a function of the number of square feet.
# 
# Student's Solution:
# Let x be the size of the installation in square feet.
# Costs:
# 1. Land cost: 100x
# 2. Solar panel cost: 250x
# 3. Maintenance cost: 100,000 + 100x
# Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
# """
# response = get_completion(prompt)
# print(response)
# 
# #### Note that the student's solution is actually not correct.
# #### We can fix this by instructing the model to work out its own solution first.
# 
# prompt = f"""
# Your task is to determine if the student's solution \
# is correct or not.
# To solve the problem do the following:
# - First, work out your own solution to the problem. 
# - Then compare your solution to the student's solution \ 
# and evaluate if the student's solution is correct or not. 
# Don't decide if the student's solution is correct until 
# you have done the problem yourself.
# 
# Use the following format:
# Question:
# ```
# question here
# ```
# Student's solution:
# ```
# student's solution here
# ```
# Actual solution:
# ```
# steps to work out the solution and your solution here
# ```
# Is the student's solution the same as actual solution \
# just calculated:
# ```
# yes or no
# ```
# Student grade:
# ```
# correct or incorrect
# ```
# 
# Question:
# ```
# I'm building a solar power installation and I need help \
# working out the financials. 
# - Land costs $100 / square foot
# - I can buy solar panels for $250 / square foot
# - I negotiated a contract for maintenance that will cost \
# me a flat $100k per year, and an additional $10 / square \
# foot
# What is the total cost for the first year of operations \
# as a function of the number of square feet.
# ``` 
# Student's solution:
# ```
# Let x be the size of the installation in square feet.
# Costs:
# 1. Land cost: 100x
# 2. Solar panel cost: 250x
# 3. Maintenance cost: 100,000 + 100x
# Total cost: 100x + 250x + 100,000 + 100x = 450x + 100,000
# ```
# Actual solution:
# """
# response = get_completion(prompt)
# print(response)
# 
# ## Model Limitations: Hallucinations
# - Boie is a real company, the product name is not real.
# 
# prompt = f"""
# Tell me about AeroGlide UltraSlim Smart Toothbrush by Boie
# """
# response = get_completion(prompt)
# print(response)
# 
# ## Try experimenting on your own!
# 
# 
# 
# #### Notes on using the OpenAI API outside of this classroom
# 
# To install the OpenAI Python library:
# ```
# !pip install openai
# ```
# 
# The library needs to be configured with your account's secret key, which is available on the [website](https://platform.openai.com/account/api-keys). 
# 
# You can either set it as the `OPENAI_API_KEY` environment variable before using the library:
#  ```
#  !export OPENAI_API_KEY='sk-...'
#  ```
# 
# Or, set `openai.api_key` to its value:
# 
# ```
# import openai
# openai.api_key = "sk-..."
# ```
# 
# #### A note about the backslash
# - In the course, we are using a backslash `\` to make the text fit on the screen without inserting newline '\n' characters.
# - GPT-3 isn't really affected whether you insert newline characters or not.  But when working with LLMs in general, you may consider whether newline characters in your prompt may affect the model's performance.
# 
# 

# %% [markdown]
# # Lesson 3: Iterative

# %%
fact_sheet_chair = """
OVERVIEW
- Part of a beautiful family of mid-century inspired office furniture, 
including filing cabinets, desks, bookcases, meeting tables, and more.
- Several options of shell color and base finishes.
- Available with plastic back and front upholstery (SWC-100) 
or full upholstery (SWC-110) in 10 fabric and 6 leather options.
- Base finish options are: stainless steel, matte black, 
gloss white, or chrome.
- Chair is available with or without armrests.
- Suitable for home or business settings.
- Qualified for contract use.

CONSTRUCTION
- 5-wheel plastic coated aluminum base.
- Pneumatic chair adjust for easy raise/lower action.

DIMENSIONS
- WIDTH 53 CM | 20.87”
- DEPTH 51 CM | 20.08”
- HEIGHT 80 CM | 31.50”
- SEAT HEIGHT 44 CM | 17.32”
- SEAT DEPTH 41 CM | 16.14”

OPTIONS
- Soft or hard-floor caster options.
- Two choices of seat foam densities: 
 medium (1.8 lb/ft3) or high (2.8 lb/ft3)
- Armless or 8 position PU armrests 

MATERIALS
SHELL BASE GLIDER
- Cast Aluminum with modified nylon PA6/PA66 coating.
- Shell thickness: 10 mm.
SEAT
- HD36 foam

COUNTRY OF ORIGIN
- Italy
"""

# %%
prompt = f"""
Your task is to help a marketing team create a 
description for a retail website of a product based 
on a technical fact sheet.

Write a product description based on the information 
provided in the technical specifications delimited by 
triple backticks.

Use at most 50 words.
use at most 3 sentences
at the end of the description, include every 7-character product id in the technical specification


Format everything as HTML that can be used in a website. 
Place the description in a <div> element.


Technical specifications: ```{fact_sheet_chair}```
"""
response = get_completion(prompt)
print(response)


# %%
from IPython.display import display, HTML
display(HTML(response))

# %% [markdown]
# # Lesson 4: Summarizing
# In this lesson, you will summarize text with a focus on specific topics

# %%
prod_review = """
Got this panda plush toy for my daughter's birthday, \
who loves it and takes it everywhere. It's soft and \ 
super cute, and its face has a friendly look. It's \ 
a bit small for what I paid though. I think there \ 
might be other options that are bigger for the \ 
same price. It arrived a day earlier than expected, \ 
so I got to play with it myself before I gave it \ 
to her.
"""

prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words. 

Review: ```{prod_review}```
"""

print(prompt)



# %%
prompt = f"""
Your task is to generate a short summary of a product \
review from an ecommerce site to give feedback to the \
Shipping deparmtment. 

Summarize the review below, delimited by triple 
backticks, in at most 30 words, and focusing on any aspects \
that mention shipping and delivery of the product. 

Review: ```{prod_review}```
"""

print(prompt)

response = get_completion(prompt)
print(response)


# %%

review_1 = prod_review 

# review for a standing lamp
review_2 = """
Needed a nice lamp for my bedroom, and this one \
had additional storage and not too high of a price \
point. Got it fast - arrived in 2 days. The string \
to the lamp broke during the transit and the company \
happily sent over a new one. Came within a few days \
as well. It was easy to put together. Then I had a \
missing part, so I contacted their support and they \
very quickly got me the missing piece! Seems to me \
to be a great company that cares about their customers \
and products. 
"""

# review for an electric toothbrush
review_3 = """
My dental hygienist recommended an electric toothbrush, \
which is why I got this. The battery life seems to be \
pretty impressive so far. After initial charging and \
leaving the charger plugged in for the first week to \
condition the battery, I've unplugged the charger and \
been using it for twice daily brushing for the last \
3 weeks all on the same charge. But the toothbrush head \
is too small. I’ve seen baby toothbrushes bigger than \
this one. I wish the head was bigger with different \
length bristles to get between teeth better because \
this one doesn’t.  Overall if you can get this one \
around the $50 mark, it's a good deal. The manufactuer's \
replacements heads are pretty expensive, but you can \
get generic ones that're more reasonably priced. This \
toothbrush makes me feel like I've been to the dentist \
every day. My teeth feel sparkly clean! 
"""

# review for a blender
review_4 = """
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

reviews = [review_1, review_2, review_3, review_4]



# %%
for i in range(len(reviews)):
    prompt = f"""
    Your task is to generate a short summary of a product \ 
    review from an ecommerce site. 

    Summarize the review below, delimited by triple \
    backticks in at most 20 words. 

    Review: ```{reviews[i]}```
    """

    response = get_completion(prompt)
    print(i, response, "\n")


# %% [markdown]
# # Lesson 5: Inferring
# In this lesson, you will infer sentiment and topics from product reviews and news articles.

# %%
lamp_review = """
Needed a nice lamp for my bedroom, and this one had \
additional storage and not too high of a price point. \
Got it fast.  The string to our lamp broke during the \
transit and the company happily sent over a new one. \
Came within a few days as well. It was easy to put \
together.  I had a missing part, so I contacted their \
support and they very quickly got me the missing piece! \
Lumina seems to me to be a great company that cares \
about their customers and products!!
"""

# %%
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Review text: '''{lamp_review}'''
"""

print(prompt)


# %%
prompt = f"""
What is the sentiment of the following product review, 
which is delimited with triple backticks?

Give your answer as a single word, either "positive" \
or "negative".

Review text: '''{lamp_review}'''
"""

print(prompt)


# %%
prompt = f"""
Identify the following items from the review text: 
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Item" and "Brand" as the keys. 
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
  
Review text: '''{lamp_review}'''
"""

print(prompt)


# %%
prompt = f"""
Identify the following items from the review text: 
- Sentiment (positive or negative)
- Is the reviewer expressing anger? (true or false)
- Item purchased by reviewer
- Company that made the item

The review is delimited with triple backticks. \
Format your response as a JSON object with \
"Sentiment", "Anger", "Item" and "Brand" as the keys.
If the information isn't present, use "unknown" \
as the value.
Make your response as short as possible.
Format the Anger value as a boolean.

Review text: '''{lamp_review}'''
"""
print(prompt)

# %%
story = """
In a recent survey conducted by the government, 
public sector employees were asked to rate their level 
of satisfaction with the department they work at. 
The results revealed that NASA was the most popular 
department with a satisfaction rating of 95%.

One NASA employee, John Smith, commented on the findings, 
stating, "I'm not surprised that NASA came out on top. 
It's a great place to work with amazing people and 
incredible opportunities. I'm proud to be a part of 
such an innovative organization."

The results were also welcomed by NASA's management team, 
with Director Tom Johnson stating, "We are thrilled to 
hear that our employees are satisfied with their work at NASA. 
We have a talented and dedicated team who work tirelessly 
to achieve our goals, and it's fantastic to see that their 
hard work is paying off."

The survey also revealed that the 
Social Security Administration had the lowest satisfaction 
rating, with only 45% of employees indicating they were 
satisfied with their job. The government has pledged to 
address the concerns raised by employees in the survey and 
work towards improving job satisfaction across all departments.
"""

# %%
prompt = f"""
Determine five topics that are being discussed in the \
following text, which is delimited by triple backticks.

Make each item one or two words long. 

Format your response as a list of items separated by commas.

Text sample: '''{story}'''
"""
print(prompt)

# %% [markdown]
# # Lesson 6 Transforming
# 
# In this notebook, we will explore how to use Large Language Models for text transformation tasks such as language translation, spelling and grammar checking, tone adjustment, and format conversion.
# 

# %%
prompt = f"""
Translate the following English text to Spanish: \ 
```Hi, I would like to order a blender```
"""

print(prompt)

# %%
prompt = f"""
Tell me which language this is: 
```Combien coûte le lampadaire?```
"""
print(prompt)

# %%
prompt = f"""
Translate the following  text to French and Spanish
and English pirate: \
```I want to order a basketball```
"""
response = get_completion(prompt)
print(response)

# %%
text = [ 
  "The girl with the black and white puppies have a ball.",  # The girl has a ball.
  "Yolanda has her notebook.", # ok
  "Its going to be a long day. Does the car need it’s oil changed?",  # Homonyms
  "Their goes my freedom. There going to bring they’re suitcases.",  # Homonyms
  "Your going to need you’re notebook.",  # Homonyms
  "That medicine effects my ability to sleep. Have you heard of the butterfly affect?", # Homonyms
  "This phrase is to cherck chatGPT for speling abilitty"  # spelling
]
for t in text:
    prompt = f"""Proofread and correct the following text
    and rewrite the corrected version. If you don't find
    and errors, just say "No errors found". Don't use 
    any punctuation around the text:
    ```{t}```"""
    
    print(prompt)
    # response = get_completion(prompt)
    # print(response)

# %%
text = f"""
Got this for my daughter for her birthday cuz she keeps taking \
mine from my room.  Yes, adults also like pandas too.  She takes \
it everywhere with her, and it's super soft and cute.  One of the \
ears is a bit lower than the other, and I don't think that was \
designed to be asymmetrical. It's a bit small for what I paid for it \
though. I think there might be other options that are bigger for \
the same price.  It arrived a day earlier than expected, so I got \
to play with it myself before I gave it to my daughter.
"""
prompt = f"proofread and correct this review: ```{text}```"

print(prompt)
#response = get_completion(prompt)
#print(response)

# %%
response = """
Got this for my daughter for her birthday because she keeps taking mine from my room. Yes, adults also like pandas too. She takes it everywhere with her, and it's super soft and cute. However, one of the ears is a bit lower than the other, and I don't think that was designed to be asymmetrical. Additionally, it's a bit small for what I paid for it. I think there might be other options that are bigger for the same price. On the positive side, it arrived a day earlier than expected, so I got to play with it myself before I gave it to my daughter.
"""

# %%
from IPython.display import display, Markdown, Latex, HTML, JSON
from redlines import Redlines

diff = Redlines(text,response)
display(Markdown(diff.output_markdown))

# %%
prompt = f"""
proofread and correct this review. Make it more compelling. 
Ensure it follows APA style guide and targets an advanced reader. 
Output in markdown format.
Text: ```{text}```
"""

print(prompt)

# response = get_completion(prompt)
# display(Markdown(response))

# %%
response = """
Title: A Compelling Review of a Panda Plush Toy

I purchased the panda plush toy as a birthday gift for my daughter, and I must say, it was a wise decision. The toy is not only suitable for children but adults as well. Its super soft texture and cute design make it irresistible to cuddle with. My daughter takes it everywhere she goes, and the toy's durability is outstanding, even after rigorous use.

The toy's asymmetrical design is unique and adds a touch of personality to it. However, the lower ear needs some improvement in its positioning to achieve a symmetrical appearance. Additionally, the size of the toy is a bit small for its price. Although it is worth every penny, there are other options available in the market that are bigger at the same price.

To my surprise, the toy arrived a day earlier than expected, allowing me to test it out before giving it to my daughter. I can confirm that it is indeed a well-crafted and high-quality product that can last for an extended period. I would highly recommend this panda plush toy to anyone looking for a cute and durable stuffed animal for themselves or their loved ones.

Keywords: Panda Plush Toy, Durability, Asymmetrical Design, Quality, Size, Recommendation.

Reference:
[Lastname], [Initials]. (Year, Month Day). [Title]. [Website]. [URL]
"""

display(Markdown(response))

# %%
diff = Redlines(text,response)
display(Markdown(diff.output_markdown))

# %% [markdown]
# # Lesson 7: Expanding
# In this lesson, you will generate customer service emails that are tailored to each customer's review.

# %%
# given the sentiment from the lesson on "inferring",
# and the original customer message, customize the email
sentiment = "negative"

# review for a blender
review = f"""
So, they still had the 17 piece system on seasonal \
sale for around $49 in the month of November, about \
half off, but for some reason (call it price gouging) \
around the second week of December the prices all went \
up to about anywhere from between $70-$89 for the same \
system. And the 11 piece system went up around $10 or \
so in price also from the earlier sale price of $29. \
So it looks okay, but if you look at the base, the part \
where the blade locks into place doesn’t look as good \
as in previous editions from a few years ago, but I \
plan to be very gentle with it (example, I crush \
very hard items like beans, ice, rice, etc. in the \ 
blender first then pulverize them in the serving size \
I want in the blender then switch to the whipping \
blade for a finer flour, and use the cross cutting blade \
first when making smoothies, then use the flat blade \
if I need them finer/less pulpy). Special tip when making \
smoothies, finely cut and freeze the fruits and \
vegetables (if using spinach-lightly stew soften the \ 
spinach then freeze until ready for use-and if making \
sorbet, use a small to medium sized food processor) \ 
that you plan to use that way you can avoid adding so \
much ice if at all-when making your smoothie. \
After about a year, the motor was making a funny noise. \
I called customer service but the warranty expired \
already, so I had to buy another one. FYI: The overall \
quality has gone done in these types of products, so \
they are kind of counting on brand recognition and \
consumer loyalty to maintain sales. Got it in about \
two days.
"""

prompt = f"""
identify the sentiment of the review, output as json format:

```
{review}
```
"""

print(prompt)

prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""

print(prompt)
#response = get_completion(prompt)
#print(response)

# %%
prompt = f"""
You are a customer service AI assistant.
Your task is to send an email reply to a valued customer.
Given the customer email delimited by ```, \
Generate a reply to thank the customer for their review.
If the sentiment is positive or neutral, thank them for \
their review.
If the sentiment is negative, apologize and suggest that \
they can reach out to customer service. 
Make sure to use specific details from the review.
Write in a concise and professional tone.
Sign the email as `AI customer agent`.
Customer review: ```{review}```
Review sentiment: {sentiment}
"""
response = get_completion(prompt, temperature=0.7)
print(response)

# %% [markdown]
# # Lesson 8: The Chat Format
# 
# In this notebook, you will explore how you can utilize the chat format to have extended conversations with chatbots personalized or specialized for specific tasks or behaviors.
# 

# %%
def get_completion(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=0, # this is the degree of randomness of the model's output
    )
    return response.choices[0].message["content"]

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

# %%
messages =  [  
{'role':'system', 'content':'You are an assistant that speaks like Shakespeare.'},    
{'role':'user', 'content':'tell me a joke'},   
{'role':'assistant', 'content':'Why did the chicken cross the road'},   
{'role':'user', 'content':'I don\'t know'}  ]

# %% [markdown]
# ## OrderBot
# We can automate the collection of user prompts and assistant responses to build a  OrderBot. The OrderBot will take orders at a pizza restaurant. 

# %%

def get_completion_from_messages(messages, model="gpt-3.5-turbo", temperature=0):
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        temperature=temperature, # this is the degree of randomness of the model's output
    )
#     print(str(response.choices[0].message))
    return response.choices[0].message["content"]

# %%
def collect_messages(_):
    prompt = inp.value_input
    inp.value = ''
    context.append({'role':'user', 'content':f"{prompt}"})
    response = get_completion_from_messages(context) 
    context.append({'role':'assistant', 'content':f"{response}"})
    panels.append(
        pn.Row('User:', pn.pane.Markdown(prompt, width=600)))
    panels.append(
        pn.Row('Assistant:', pn.pane.Markdown(response, width=600, style={'background-color': '#F6F6F6'})))
 
    return pn.Column(*panels)


# %%
import panel as pn  # GUI
pn.extension()

panels = [] # collect display 

context = [ {'role':'system', 'content':"""
You are OrderBot, an automated service to collect orders for a pizza restaurant. \
You first greet the customer, then collects the order, \
and then asks if it's a pickup or delivery. \
You wait to collect the entire order, then summarize it and check for a final \
time if the customer wants to add anything else. \
If it's a delivery, you ask for an address. \
Finally you collect the payment.\
Make sure to clarify all options, extras and sizes to uniquely \
identify the item from the menu.\
You respond in a short, very conversational friendly style. \
The menu includes \
pepperoni pizza  12.95, 10.00, 7.00 \
cheese pizza   10.95, 9.25, 6.50 \
eggplant pizza   11.95, 9.75, 6.75 \
fries 4.50, 3.50 \
greek salad 7.25 \
Toppings: \
extra cheese 2.00, \
mushrooms 1.50 \
sausage 3.00 \
canadian bacon 3.50 \
AI sauce 1.50 \
peppers 1.00 \
Drinks: \
coke 3.00, 2.00, 1.00 \
sprite 3.00, 2.00, 1.00 \
bottled water 5.00 \
"""} ]  # accumulate messages


inp = pn.widgets.TextInput(value="Hi", placeholder='Enter text here…')
button_conversation = pn.widgets.Button(name="Chat!")

interactive_conversation = pn.bind(collect_messages, button_conversation)

dashboard = pn.Column(
    inp,
    pn.Row(button_conversation),
    pn.panel(interactive_conversation, loading_indicator=True, height=300),
)

dashboard

# %%



