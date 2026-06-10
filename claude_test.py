from anthropic import Anthropic

client = Anthropic(api_key="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")
response = client.messages.create(
    model="claude-3-opus",
    max_tokens=1000,
    messages=[{"role": "user", "content": "Write a Python function to sort a list."}]
)
print(response.content)
