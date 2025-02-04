from uagents import Agent, Context, Model
from lc_helper import graph

agent = Agent(
    name="Databae Mini",
    port=8000,
    seed="Databae Mini",
    endpoint=["http://localhost:8000/submit"]
)

class Request(Model):
    host: str
    port: int
    username: str
    password: str
    database: str
    user_request: str

class Response(Model):
    summary: str

@agent.on_message(Request)
async def message_handler(ctx: Context, sender: str, req: Request):
    ctx.logger.info("Message received")
    initial_state = {
        "host": req.host,
        "port": req.port,
        "username": req.username,
        "password": req.password,
        "database": req.database,
        "message": req.user_request,  
        "sql_query": "",  
        "result_set": ""
    }

    final_state = graph.invoke(initial_state)
    await ctx.send(sender, Response(summary=final_state["analysis"]))

if __name__ == "__main__":
    agent.run()


