**Mini Databae AI Agent**

**Description**: This AI agent is the miniature version of a project we did at Cal Hacks, sponsored by Fetch.ai, called [Databae](https://github.com/trungtran1234/databae). It uses a combination of DeepSeek's, Llama's (Facebook), and OpenAI's models 
powered by Groq in order to produce data analysis of a database. It also only returns a plaintext English response rather than an actual table or pie chart due to uAgents' limitations. It is also powered by LangGraph, so essentially, you can imagine it as three agents combined into one! Finally, it is finally utilizing RAG, and in my testing, it has actually reduced total token usage by 60%.

**Input Data Model**
```
class Request(Model):
    host: str
    port: int
    username: str
    password: str
    database: str
    user_request: str
```

**Output Data Model**
```
class Response(Model):
    summary: str
```
