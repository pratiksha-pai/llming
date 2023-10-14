# set_llm_cache(llm)
# llm = OpenAI(openai_api_key=openai_api_key, temperature=0.9, max_tokens=50)
# set_llm_cache(InMemoryCache())


# prompt_template = PromptTemplate(
#     input_variables=["value"],
#     template="I want to open a {value} restaurant, can you suggest me a name?",
# )

# answer = prompt_template.format(value=value)
# print(answer)




# # prompt_template = PromptTemplate(
# #     input_variables=["value"],
# #     template="Can you summarize this - {value}",
# # )

# # answer = prompt_template.format(value=value)
# # print(answer)

# # # answer = llm.predict("Can you summarize \"{value}\"?".format(value=value))
# # # print(answer)

# model_name="gpt-3.5-turbo", 

# name = llm("I want to open a Italian restaurant, can you suggest me a name?")
# print(name)

response = llm(messages)
print(response)