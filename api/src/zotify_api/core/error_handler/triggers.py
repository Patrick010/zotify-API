import importlib
import logging
import pkgutil
from typing import Callable, Dict, List

from . import actions
from .config import TriggerConfig

log = logging.getLogger(__name__)

class TriggerManager:
    """
    Manages the execution of actions based on configured triggers.
    Actions are dynamically loaded from the 'actions' sub-package.
    """

    def __init__(self, triggers: List[TriggerConfig]):
        self.triggers = triggers
        self.action_map: Dict[str, Callable] = self._load_actions()
        log.info(
            f"TriggerManager initialized with {len(triggers)} triggers "
            f"and {len(self.action_map)} actions."
        )

    def _load_actions(self) -> Dict[str, Callable]:
        """Dynamically loads all actions from the 'actions' sub-package."""
        action_map = {}
        action_pkg_path = actions.__path__
        action_pkg_name = actions.__name__

        for _, name, _ in pkgutil.iter_modules(action_pkg_path, f"{action_pkg_name}."):
            try:
                module = importlib.import_module(name)
                if hasattr(module, "run") and callable(module.run):
                    action_name = name.split('.')[-1]
                    action_map[action_name] = module.run
                    log.debug(f"Successfully loaded action: {action_name}")
            except Exception:
                log.exception(f"Failed to load action module: {name}")
        return action_map

    def process_triggers(self, exc: Exception):
        """
        Checks if the given exception matches any configured triggers and
        executes the associated actions.
        """
        exc_type_str = f"{exc.__class__.__module__}.{exc.__class__.__name__}"

        for trigger in self.triggers:
            if trigger.exception_type == exc_type_str:
                log.info(
                    f"Exception '{exc_type_str}' matched a trigger. "
                    "Executing actions."
                )
                for action_config in trigger.actions:
                    action_func = self.action_map.get(action_config.type)
                    if action_func:
                        try:
                            action_func(exc, action_config.details)
                        except Exception:
                            log.exception(
                                "Failed to execute action of type "
                                f"'{action_config.type}'"
                            )
                    else:
                        log.warning(
                            f"Unknown action type '{action_config.type}' configured."
                        )
