import copy
import datetime
import json
import logging
import os
from typing import TYPE_CHECKING, Any, Dict, Optional

import requests

from beaker_kernel.lib.context import BaseContext
from beaker_kernel.lib.utils import intercept

from .agent import MiraConfigEditAgent

if TYPE_CHECKING:
    from beaker_kernel.kernel import LLMKernel
    from beaker_kernel.lib.subkernels.base import BaseSubkernel

logger = logging.getLogger(__name__)


class MiraConfigEditContext(BaseContext):

    agent_cls = MiraConfigEditAgent

    model_config_id: Optional[str]
    model_config_json: Optional[str]
    model_config_dict: Optional[dict[str, Any]]
    var_name: Optional[str] = "model_config"

    def __init__(self, beaker_kernel: "LLMKernel", subkernel: "BaseSubkernel", config: Dict[str, Any]) -> None:
        self.reset()
        logger.error("initializing...")
        super().__init__(beaker_kernel, subkernel, self.agent_cls, config)

    def reset(self):
        pass

    async def post_execute(self, message):
        pass    
        
    async def setup(self, config, parent_header):
        logger.error(f"performing setup...")
        self.config = config
        item_id = config["id"]
        item_type = config.get("type", "model_config")
        logger.error(f"Processing {item_type} AMR {item_id} as a MIRA model")
        await self.set_model_config(
            item_id, item_type, parent_header=parent_header
        )

    async def set_model_config(self, item_id, agent=None, parent_header={}):
        self.config_id = item_id
        meta_url = f"{os.environ['DATA_SERVICE_URL']}/model_configurations/{self.config_id}"
        logger.error(f"Meta url: {meta_url}")
        self.configuration = requests.get(meta_url).json()
        self.amr = self.configuration.get("configuration")
        self.original_amr = copy.deepcopy(self.amr)
        if self.amr:
            await self.load_mira()
        else:
            raise Exception(f"Model config '{item_id}' not found.")
        await self.send_mira_preview_message(parent_header=parent_header)

    async def load_mira(self):
        command = "\n".join(
            [
                self.get_code("setup"),
                self.get_code("load_model", {
                    "var_name": self.var_name,
                    "model": self.amr,
                }),
            ]
        )
        print(f"Running command:\n-------\n{command}\n---------")
        await self.execute(command)        

    async def send_mira_preview_message(
        self, server=None, target_stream=None, data=None, parent_header={}
    ):
        try:

            preview = await self.evaluate(self.get_code("model_preview"), {"var_name": self.var_name})
            content = preview["return"]
            self.beaker_kernel.send_response(
                "iopub", "model_preview", content, parent_header=parent_header
            )
        except Exception as e:
            raise        