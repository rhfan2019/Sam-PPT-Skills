# -*- coding: utf-8 -*-
"""Layout registry: deck.json `layout` name -> builder(D, slide_dict)."""
import importlib
import importlib.util

REGISTRY = {}

for _mod in ("consult", "openers", "cards", "compare", "misc"):
    if importlib.util.find_spec(f"{__name__}.{_mod}") is not None:
        REGISTRY.update(importlib.import_module(f"{__name__}.{_mod}").LAYOUTS)
