import asyncio
import argparse
import sys
from typing import Type

from jbot import config
from opendevin.agent import Agent

# import agenthub  # noqa F401 (we import this to get the agents registered)

# from opendevin.controller import AgentController
from opendevin.llm.llm import LLM
from opendevin.plan import Plan
from opendevin.state import State
from src.jbot.linear.linear import Linear


def read_task_from_file(file_path: str) -> str:
    """Read task from the specified file."""
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def read_task_from_stdin() -> str:
    """Read task from stdin."""
    return sys.stdin.read()


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Run an agent with a specific task")
    parser.add_argument(
        "-t", "--task", type=str, default="", help="The task for the agent to perform"
    )
    parser.add_argument(
        "-f",
        "--file",
        type=str,
        help="Path to a file containing the task. Overrides -t if both are provided.",
    )
    parser.add_argument(
        "-c",
        "--agent-cls",
        default="MonologueAgent",
        type=str,
        choices=["MonologueAgent", "CodeActAgent", "PlannerAgent"],
        help="The agent class to use (default: MonologueAgent)",
    )
    parser.add_argument(
        "-m",
        "--model-name",
        default=config.get_or_default("LLM_MODEL", "gpt-4-0125-preview"),
        type=str,
        help="The (litellm) model name to use",
    )
    parser.add_argument(
        "-i",
        "--max-iterations",
        default=100,
        type=int,
        help="The maximum number of iterations to run the agent",
    )
    return parser.parse_args()


async def main():
    """Main coroutine to run the agent controller with task input flexibility."""
    args = parse_arguments()

    print(f"Running agent {args.agent_cls} (model: {args.model_name}) ")
    llm = LLM(args.model_name)
    # AgentCls: Type[Agent] = Agent.get_cls(args.agent_cls)
    # agent = AgentCls(llm=llm)
    # controller = AgentController(
    #     agent=agent, workdir=args.directory, max_iterations=args.max_iterations
    # )
    # plan = Plan(
    #     "Write a function that takes a list of numbers and returns the sum of all the numbers in the list."
    # )
    # state = State(plan)
    # agent.step(state)

    # await controller.start_loop(task)

    # get latest task from linear
    linear = Linear()
    task = linear.get_my_todo_issues(first=1)
    print(task)


if __name__ == "__main__":
    asyncio.run(main())
