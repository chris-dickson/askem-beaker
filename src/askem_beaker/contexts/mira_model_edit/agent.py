import json
import logging
import re

import requests
from archytas.react import Undefined
from archytas.tool_utils import AgentRef, LoopControllerRef, tool

from beaker_kernel.lib.agent import BaseAgent
from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.jupyter_kernel_proxy import JupyterMessage

logging.disable(logging.WARNING)  # Disable warnings
logger = logging.Logger(__name__)


class MiraModelEditAgent(BaseAgent):
    """
    LLM agent used for working with the Mira Modeling framework ("mira_model" package) in Python 3.
    This will be used to find pre-written functions which will be used to edit a model.
    """

    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        super().__init__(context, tools, **kwargs)

    @tool()
    async def generate_code(
        self, query: str, agent: AgentRef, loop: LoopControllerRef
    ) -> None:
        """
       Generated Python code to be run in an interactive Jupyter notebook for the purpose of exploring, modifying and visualizing a Pandas Dataframe.

        Input is a full grammatically correct question about or request for an action to be performed on the loaded model.

         Args:
            query (str): A fully grammatically correct question about the current model.

        """
        # set up the agent
        # str: Valid and correct python code that fulfills the user's request.
        prompt = f"""
You are a programmer writing code to help with scientific data analysis and manipulation in {agent.context.metadata.get("name", "a Jupyter notebook")}.

Please write code that satisfies the user's request below.

Assume that the model is already loaded and has the variable named `model`.

If you are asked to modify or update the dataframe, modify the dataframe in place, keeping the updated variable the same unless specifically specified otherwise.

If you are asked to replace the template name of the model, use the available function named `replace_template_name` that is defined by the following python code:
````````````````````
def replace_template_name(
    model: mira.metamodel.template_model.TemplateModel,
    old_name: str,
    new_name: str,
) -> mira.metamodel.template_model.TemplateModel

    update the template name within a model.

    E.g., can turn the S.I.R. model into a S.I.Recovery. model by using old_name R and new_name Recovery

    Parameters
    ----------
    template_model :
        A template model
    old_name :
        The (singular) name of the model state or transition to be updated, e.g., ``"I"``
    new_name :
       The (singular) updated name of the model state or transition, e.g., ``"Infected"``

    Returns
    -------
    :
       A template model
````````````````````

You also have access to the libraries {agent.context.metadata.get("libraries", "that are common for these tasks")}.

Please generate the code as if you were programming inside a Jupyter Notebook and the code is to be executed inside a cell.
You MUST wrap the code with a line containing three backticks (```) before and after the generated code.
No addtional text is needed in the response, just the code block.
"""

        llm_response = await agent.oneshot(prompt=prompt, query=query)
        loop.set_state(loop.STOP_SUCCESS)
        preamble, code, coda = re.split("```\w*", llm_response)
        result = json.dumps(
            {
                "action": "code_cell",
                "language": agent.context.lang,
                "content": code.strip(),
            }
        )
        return result

