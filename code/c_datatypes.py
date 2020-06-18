from talon import Context, Module, actions

mod = Module()
ctx = Context()

ctx.lists["self.c_pointers"] = {
    "pointer": "*",
    "pointer to pointer": "**",
}

ctx.lists["self.c_signed"] = {
    "signed": "signed",
    "unsigned": "unsigned",
}

ctx.lists["self.c_types"] = {
    "character": "char",
    "char": "char",
    "short": "short",
    "long": "long",
    "int": "int",
    "integer": "int",
    "void": "void",
    "double": "double",
    "struct": "struct",
}

mod.list("c_pointers", desc="Common C pointers")
mod.list("c_signed", desc="Common C datatype signed modifiers")
mod.list("c_types", desc="Common C types")


@mod.capture
def datatype(m) -> str:
    "Returns a string"


@mod.capture
def c_pointers(m) -> str:
    "Returns a string"


@mod.capture
def c_signed(m) -> str:
    "Returns a string"


@mod.capture
def c_types(m) -> str:
    "Returns a string"


@ctx.capture(rule="{self.c_pointers}")
def c_pointers(m) -> str:
    return m.c_pointers


@ctx.capture(rule="{self.c_signed}")
def c_signed(m) -> str:
    return m.c_signed


@ctx.capture(rule="{self.c_types}")
def c_types(m) -> str:
    return m.c_types


@ctx.capture(rule="[<self.c_signed>] <self.c_types> [<self.c_pointers>+]")
def datatype(m) -> str:
    return "(" + " ".join(list(m)) + ")"
