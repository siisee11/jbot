import asyncio
import argparse
import sys
from typing import Type

from jbot import config
from jbot.github.github import MyGithub
from jbot.utils.pl import get_language_from_filename
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

    prompt = """
You are an expert software engineer.
You are currently solving the following issue within our repository. Here's the issue text:

####
ISSUE:

title: {issue_title}

description: {issue_description}
####

####
INSTRUCTIONS:
1. you're going to solve this issue on your own. You have access to codebase, and you can search for code snippets that might help you solve the issue. 

2. you need to understand the issue. Read the issue description.

3. you should think search terms from the issue description that you can use to search for code snippets that related to this issue.
####

####
IMPORTANT TIPS:
1. SEARCH_TERMS are names that possibly be used as name of variables, functions, components or code file.
if the term is in CamelCase, snake_case, or kebab-case, consider it as variable name and you must include it as is.

2. SEARCH_TERMS are nouns.

3. SEARCH_TERMS should be comma separated.

4. DO NOT include commonly used terms (e.g. Button, Text, etc.) Include any unusual words. 

5. Place most specific term (e.g. variable name) first.

6. If extracted terms are not in English, you must include both the original and translated keywords.
Because codes are written in English. But there is a chance to search original text in UI components or comments.

7. Answer without any explanation. Just provide the terms you would use to search for code snippets.

####

SEARCH_TERMS:
"""

    formatted = prompt.format(
        issue_title=task[0].title, issue_description=task[0].description
    )
    print(formatted)

    messages = [{"content": formatted, "role": "user"}]

    resp = llm.completion(messages=messages)
    search_terms = resp.choices[0].message.content.split(",")
    print(search_terms)

    github = MyGithub()
    search_term_split = search_terms[0].split()
    for term in search_term_split:
        search_result = github.search_code(query=term)
        print(search_result)

        if search_result is None:
            continue

        pl = get_language_from_filename(search_result.file_path)
        code_segment = search_result.fragment

        comment = f"""이 이슈와 관련있는 파일: `{search_result.file_path}` \n\n\n ```{pl}\n{code_segment}
```

(commented by jbot)"""
        linear.create_comment_to_issue(task[0].id, comment)

        break

    print("Done!")


if __name__ == "__main__":
    asyncio.run(main())
