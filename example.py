from uagents import Agent, Context, Model

agent = Agent(
    name="Example Agent",
    port=8001,
    seed="Example Agent",
    endpoint=["http://localhost:8001/submit"]
)

mini_databae_address = "agent1qg55rgkmytnnssljchyyj9vtjvexsajk7xxs6pejksnnh4xevzxjc626hml"

class Request(Model):
    host: str
    port: int
    username: str
    password: str
    database: str
    user_request: str

class Response(Model):
    summary: str

@agent.on_event("startup")
async def startup(ctx: Context):
    await ctx.send(mini_databae_address, Request(host="host", port=3306, username="username", password="password", database="database", 
                                                user_request="example user request"
                                        ))

@agent.on_message(Response)
async def message_handler(ctx: Context, sender: str, res: Response):
    ctx.logger.info(f"Summary: {res.summary}")

if __name__ == "__main__":
    agent.run()

