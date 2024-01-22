import copy
import datetime
import json
import logging
import os
from typing import TYPE_CHECKING, Any, Dict, Optional

import requests

from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.utils import intercept

from .agent import MiraModelEditAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.subkernels.base import BaseSubkernel

logger = logging.getLogger(__name__)


class MiraModelEditContext(BaseContext):

    agent_cls = MiraModelEditAgent

    model_id: Optional[str]
    model_json: Optional[str]
    model_dict: Optional[dict[str, Any]]
    var_name: Optional[str] = "model"

    def __init__(self, beaker_kernel: "LLMKernel", subkernel: "BaseSubkernel", config: Dict[str, Any]) -> None:
        self.reset()
        super().__init__(beaker_kernel, subkernel, self.agent_cls, config)

    def reset(self):
        pass
        
    async def setup(self, config, parent_header):
        self.config = config
        item_id = config["id"]
        item_type = config.get("type", "model")
        print(f"Processing {item_type} AMR {item_id} as a MIRA model")
        await self.set_model(
            item_id, item_type, parent_header=parent_header
        )

    async def post_execute(self, message):
        await self.send_mira_preview_message(parent_header=message.parent_header)

    @intercept()
    async def replace_template_name(self, message):
        content = message.content

        model = content.get("model")
        old_name  = content.get("old_name")
        new_name = content.get("new_name")

        self.beaker_kernel.send_response(
            "iopub",
            "replace_template_name",
            {
                "model": model,
                "old_name": old_name,
                "new_name": new_name
            },
        )

