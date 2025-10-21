import importlib
import pkgutil

def register_all(tree, guild_id):
    """Auto-register all commands inside this category folder."""
    for module in pkgutil.iter_modules(__path__):
        mod = importlib.import_module(f"{__name__}.{module.name}")
        if hasattr(mod, "register"):
            mod.register(tree, guild_id)
            print(f"Loaded user command: {module.name}")
