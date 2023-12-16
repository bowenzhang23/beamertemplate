from typing import Iterable

def curlybraket(s):
    return "".join(["{", str(s), "}"])


def begin(s):
    return f"\n\\begin{curlybraket(s)}\n"


def end(s):
    return f"\n\\end{curlybraket(s)}\n"


def level_str(level):
    return {
        1: "section",
        2: "subsection",
        3: "subsubsection",
    }.get(level, "section")


class BeamerTitleCollection(object):
    def __init__(self):
        self.title: str | None = None
        self.title_short: str | None = None
        self.title_sub: str | None = None
        self.names: Iterable | None = None
        self.names_short: Iterable | None = None
        self.names_inst_i: Iterable | None = None
        self.insts: Iterable | None = None
        self.insts_short: Iterable | None = None
        self.insts_i: Iterable | None = None
        self.meeting: str | None = None
        self.meeting_short: str | None = None
        self.logo_paths: Iterable | None = None
