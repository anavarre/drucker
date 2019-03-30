"""Initialization file for the drucker support library."""
from . import variables
from . import arguments
from . import requirements
from . import local_setup
from . import init
from . import base
from . import mirror
from . import edge
from . import db
from . import search
from . import web

# Declare all submodules so that pydoc and others know how to find them.
__all__ = [
    "variables",
    "arguments",
    "requirements",
    "local_setup",
    "init",
    "base",
    "mirror",
    "edge",
    "db",
    "search",
    "web",
]
