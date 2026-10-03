
"""
AgisRecon - Module Manager

Central manager for reconnaissance modules.

The ModuleManager is responsible for:
- Registering available modules
- Retrieving modules by name
- Checking module availability
- Executing individual modules
- Executing multiple modules in sequence
- Collecting module results
"""

from typing import Any, Dict, List, Optional, Type

from .base import BaseModule
from .subfinder import SubfinderModule
from .assetfinder import AssetfinderModule
from .dnsx import DNSXModule
from .httpx import HTTPXModule
from .nmap import NmapModule
from .waybackurls import WaybackURLsModule
from .katana import KatanaModule
from .nuclei import NucleiModule


class ModuleManager:
    """
    Central manager for all AgisRecon reconnaissance modules.
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the module manager.

        Args:
            config: Optional configuration shared by modules.
        """
        self.config = config or {}

        self.module_classes: Dict[str, Type[BaseModule]] = {
            "subfinder": SubfinderModule,
            "assetfinder": AssetfinderModule,
            "dnsx": DNSXModule,
            "httpx": HTTPXModule,
            "nmap": NmapModule,
            "waybackurls": WaybackURLsModule,
            "katana": KatanaModule,
            "nuclei": NucleiModule,
        }

        self.modules: Dict[str, BaseModule] = {}

        self._initialize_modules()

    def _initialize_modules(self) -> None:
        """
        Create an instance of every registered module.
        """
        for name, module_class in self.module_classes.items():
            self.modules[name] = module_class(self.config)

    def register(
        self,
        module_class: Type[BaseModule],
    ) -> None:
        """
        Register a new module.

        Args:
            module_class: Module class that inherits from BaseModule.

        Raises:
            TypeError: If the supplied class is not a BaseModule subclass.
            ValueError: If the module name is invalid or already registered.
        """
        if not issubclass(module_class, BaseModule):
            raise TypeError(
                "Module must inherit from BaseModule."
            )

        name = module_class.name

        if not name:
            raise ValueError(
                "Module must define a name."
            )

        if name in self.module_classes:
            raise ValueError(
                f"Module '{name}' is already registered."
            )

        self.module_classes[name] = module_class
        self.modules[name] = module_class(self.config)

    def get(self, name: str) -> BaseModule:
        """
        Retrieve a module by name.

        Args:
            name: Registered module name.

        Returns:
            The requested module instance.

        Raises:
            KeyError: If the module does not exist.
        """
        module_name = name.strip().lower()

        if module_name not in self.modules:
            raise KeyError(
                f"Module '{name}' is not registered."
            )

        return self.modules[module_name]

    def list_modules(self) -> List[str]:
        """
        Return the names of all registered modules.

        Returns:
            List of module names.
        """
        return list(self.modules.keys())

    def available_modules(self) -> List[str]:
        """
        Return modules whose external tools are available.

        Returns:
            List of available module names.
        """
        available: List[str] = []

        for name, module in self.modules.items():
            if module.is_available():
                available.append(name)

        return available

    def unavailable_modules(self) -> List[str]:
        """
        Return modules whose external tools are unavailable.

        Returns:
            List of unavailable module names.
        """
        unavailable: List[str] = []

        for name, module in self.modules.items():
            if not module.is_available():
                unavailable.append(name)

        return unavailable

    def run(
        self,
        name: str,
        target: str,
        **kwargs: Any,
    ) -> List[Any]:
        """
        Execute a single module.

        Args:
            name: Name of the module to execute.
            target: Target supplied to the module.
            **kwargs: Module-specific options.

        Returns:
            Results returned by the module.
        """
        module = self.get(name)

        return module.run(
            target,
            **kwargs,
        )

    def run_all(
        self,
        target: str,
        modules: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> Dict[str, List[Any]]:
        """
        Execute multiple modules in sequence.

        If no module list is supplied, all registered modules
        are executed in their registration order.

        Args:
            target: Target supplied to each module.
            modules: Optional list of module names.
            **kwargs: Module-specific options.

        Returns:
            Dictionary mapping module names to their results.

        Note:
            Modules whose external tools are unavailable are skipped.
        """
        selected_modules = modules or self.list_modules()

        results: Dict[str, List[Any]] = {}

        for name in selected_modules:
            module = self.get(name)

            if not module.is_available():
                results[name] = []
                continue

            try:
                results[name] = module.run(
                    target,
                    **kwargs,
                )
            except (ValueError, RuntimeError):
                results[name] = []

        return results

    def get_module_info(self, name: str) -> Dict[str, Any]:
        """
        Return information about a registered module.

        Args:
            name: Module name.

        Returns:
            Module information dictionary.
        """
        module = self.get(name)

        info = module.get_info()
        info["available"] = module.is_available()

        return info

    def get_all_module_info(self) -> Dict[str, Dict[str, Any]]:
        """
        Return information about all registered modules.

        Returns:
            Dictionary containing information for every module.
        """
        return {
            name: self.get_module_info(name)
            for name in self.list_modules()
        }

    def __contains__(self, name: str) -> bool:
        """
        Check whether a module is registered.

        Example:
            'subfinder' in manager
        """
        return name.strip().lower() in self.modules

    def __len__(self) -> int:
        """
        Return the number of registered modules.
        """
        return len(self.modules)

    def __repr__(self) -> str:
        """
        Return a readable representation of the manager.
        """
        return (
            f"<ModuleManager modules={len(self.modules)} "
            f"registered>"
        )

