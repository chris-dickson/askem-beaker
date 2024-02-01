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

    A mira model is made up of multiple templates that are merged together like ...

    An example mira model will look like this when encoded in json:
    ```
    {
      "id": "foo",
      "bar": "foobar",
      ...
    }

    Instead of manipulating the model directly, the agent will always return code that will be run externally in a jupyter notebook.

    """

    def __init__(self, context: BaseContext = None, tools: list = None, **kwargs):
        super().__init__(context, tools, **kwargs)

    @tool()
    async def replace_template_name(self, old_name: str, new_name: str, model: str, agent: AgentRef, loop: LoopControllerRef):
        """
        This tool is used when a user wants to rename a template that is part of a model.

        Args:
            model (str): The variable name identifier of the model. If not known or specified, the default value of `model` should be used.
            old_name (str): The old/existing name of the template as it exists in the model before changing.
            new_name (str): The name that the template should be changed to.
        """
        code = agent.context.get_code("replace_template_name", {"model": model, "old_name": old_name, "new_name": new_name})
        loop.set_state(loop.STOP_SUCCESS)
        return json.dumps(
            {
                "action": "code_cell",
                "language": "python3",
                "content": code.strip(),
            }
        )

    @tool()
    async def replace_state_name(self, template_name: str, old_name: str, new_name: str, model: str, agent: AgentRef, loop: LoopControllerRef):
        """
        This tool is used when a user wants to rename a state name within a template that is part of a model.

        Args:
            model (str): The variable name identifier of the model. If not known or specified, the default value of `model` should be used.
            template_name (str): the template within the model where these changes will be made
            old_name (str): The old/existing name of the state as it exists in the model before changing.
            new_name (str): The name that the state should be changed to.
        """
        code = agent.context.get_code("replace_state_name", {"model": model, "template_name": template_name, "old_name": old_name, "new_name": new_name})
        loop.set_state(loop.STOP_SUCCESS)
        return json.dumps(
            {
                "action": "code_cell",
                "language": "python3",
                "content": code.strip(),
            }
        )

    @tool()
    async def add_template(self, name: str, subject: str, outcome: str, expr: str, model: str, agent: AgentRef, loop: LoopControllerRef):
        """
        This tool is used when a user wants to add a new transition to a model.

        Args:
            model (str): The variable name identifier of the model. If not known or specified, the default value of `model` should be used.
            subject (str): The state that is the source of the new transition.
            outcome (str): the state that the new transition outputs to.
            expr (str): the mathematical rate law for the transition.
            name (str): the name of the transition
        """
        code = agent.context.get_code("add_template", {"model": model, "subject": subject, "outcome": outcome, "expr": expr, name: "name"})
        loop.set_state(loop.STOP_SUCCESS)
        return json.dumps( # <--- Is this returning to archytas? Why does this action not mean it sends a response with code_cell
            {
                "action": "code_cell",
                "language": "python3",
                "content": code.strip(),
            }
        )
