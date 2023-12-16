from abc import ABC, abstractmethod
from beamert.utils import *
from os.path import abspath


class BeamerComponent(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def parse(self):
        raise NotImplementedError()


class BeamerHeader(BeamerComponent):
    def __init__(self):
        super().__init__()
        pass

    def parse(self):
        header_tex = r"""
\documentclass{beamer}
\usepackage[utf8]{inputenc}
"""
        return header_tex


class BeamerStyle(BeamerComponent):
    def __init__(self):
        super().__init__()

    def parse(self):
        style_tex = r"""
\usetheme{Madrid}
\useoutertheme{default}
\useinnertheme{rounded}

\definecolor{myblue}{rgb}{0.04706, 0.13725, 0.26667}
\definecolor{mygrey}{rgb}{0.3686, 0.5255, 0.6235}

\setbeamercolor{palette primary}{bg=myblue,fg=white}
\setbeamercolor{palette secondary}{bg=myblue,fg=white}
\setbeamercolor{palette tertiary}{bg=myblue,fg=white}
\setbeamercolor{palette quaternary}{bg=myblue,fg=white}
\setbeamercolor{structure}{fg=myblue} % itemize, enumerate, etc
\setbeamercolor{section in toc}{fg=myblue} % TOC sections
\setbeamercolor{subsection in head/foot}{bg=mygrey,fg=white}

\setbeamertemplate{title page}[default][rounded=true,shadow=false]
\setbeamertemplate{blocks}[rounded][shadow=false]
"""
        return style_tex


class BeamerTitleSetting(BeamerComponent):
    def __init__(self, btc: BeamerTitleCollection):
        super().__init__()
        self._btc = btc

    def parse(self):
        btc = self._btc
        t_tex = f"\\title[{btc.title_short}]{curlybraket(btc.title)}"
        tsub_tex = f"\\subtitle{curlybraket(btc.title_sub)}"
        nms_extra = ", ".join([nm for nm in btc.names_short])
        nm_extra = " \\and ".join(
            [
                f"{nm}\\inst{curlybraket(btc.names_inst_i[i])}"
                for i, nm in enumerate(btc.names)
            ]
        )
        au_tex = f"\\author[{nms_extra}]{curlybraket(nm_extra)}"
        insts_extra = ",".join([inst for inst in btc.insts_short])
        inst_extra = "\n".join(
            [
                f"\\inst{curlybraket(btc.insts_i[i])}\n{inst}"
                for i, inst in enumerate(btc.insts)
            ]
        )
        inst_tex = f"\\institute[{insts_extra}]" + curlybraket(inst_extra)
        meeting_tex = f"\\date[{btc.meeting_short}]{curlybraket(btc.meeting)}"
        logo_extra = "\n".join(
            [
                f"\\includegraphics[height=1cm]{curlybraket(abspath(p))}"
                for p in btc.logo_paths
            ]
        )
        logo_tex = f"\\logo{curlybraket(logo_extra)}"
        return "\n".join([t_tex, tsub_tex, au_tex, inst_tex, meeting_tex, logo_tex])


class BeamerTocSetting(BeamerComponent):
    def __init__(self):
        super().__init__()

    def parse(self):
        toc_tex = r"""
\AtBeginSection[]
{
  \begin{frame}
    \frametitle{Table of Contents}
    \tableofcontents[currentsection]
  \end{frame}
}
"""
        return toc_tex


class BeamerDocumentCtrl(BeamerComponent):
    def __init__(self, begin):
        super().__init__()
        self._begin = begin

    def parse(self):
        if self._begin:
            return begin("document")
        else:
            return end("document")


class BeamerSection(BeamerComponent):
    def __init__(self, title, level=1):
        super().__init__()
        self._title = title
        self._level = level

    def parse(self):
        tex = f"\\{level_str(self._level)}{curlybraket(self._title)}"
        return tex


class BeamerFrame(BeamerComponent):
    def __init__(self):
        super().__init__()

    def parse(self):
        raise NotImplementedError()


class BeamerTitleFrame(BeamerFrame):
    def __init__(self):
        super().__init__()

    def parse(self):
        return r"""
\frame{\titlepage}
\logo{}
"""


class BeamerTocFrame(BeamerFrame):
    def __init__(self, title):
        super().__init__()
        self._title = title

    def parse(self):
        title_tex = f"\\frametitle{curlybraket(self._title)}"
        toc_tex = r"\tableofcontents"
        return "".join([begin("frame"), title_tex, toc_tex, end("frame")])


class BeamerEmptyFrame(BeamerComponent):
    def __init__(self):
        super().__init__()

    def parse(self):
        return "".join([begin("frame"), end("frame")])


class BeamerFileFrame(BeamerComponent):
    def __init__(self, fn):
        super().__init__()
        self._fn = abspath(fn)

    def parse(self):
        return f"\\input{curlybraket(self._fn)}"
