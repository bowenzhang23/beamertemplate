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
\documentclass[aspectratio=1610]{beamer}
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

\definecolor{myblue}{rgb}{0.35686, 0.60784, 0.83529}
\definecolor{mylightblue}{rgb}{0.0, 0.43922, 0.75294}
\definecolor{mydarkblue}{rgb}{0.26667, 0.45490, 0.62745}
\definecolor{myorange}{rgb}{0.92941, 0.49020, 0.19216}
\definecolor{mygrey}{rgb}{0.3686, 0.5255, 0.6235}

\setbeamercolor{palette primary}{bg=myblue,fg=white}
\setbeamercolor{palette secondary}{bg=myblue,fg=white}
\setbeamercolor{palette tertiary}{bg=myblue,fg=white}
\setbeamercolor{palette quaternary}{bg=myblue,fg=white}
\setbeamercolor{structure}{fg=myblue} % itemize, enumerate, etc
\setbeamercolor{section in toc}{fg=myblue} % TOC sections
\setbeamercolor{subsection in head/foot}{bg=mygrey,fg=white}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{itemize items}[square]
\setbeamertemplate{enumerate items}[square]

\setbeamertemplate{title page}[default][rounded=true,shadow=false]
\setbeamertemplate{blocks}[rounded][shadow=false]

\setlength{\leftmargini}{0.3cm}
\setlength{\leftmarginii}{0.3cm}
"""
        return style_tex


class BeamerTitleSetting(BeamerComponent):
    def __init__(self, btc: BeamerTitleCollection):
        super().__init__()
        self._btc = btc

    def parse(self):
        tex_collection = list()
        btc = self._btc
        if btc.title:
            t_tex = f"\\title[{btc.title_short}]{curlybraket(btc.title)}"
            tex_collection.append(t_tex)
        if btc.title_sub:
            tsub_tex = f"\\subtitle{curlybraket(btc.title_sub)}"
            tex_collection.append(tsub_tex)
        if btc.names_short:
            nms_extra = ", ".join([nm for nm in btc.names_short])
        if btc.names and btc.names_inst_i:
            nm_extra = " \\and ".join(
                [
                    f"{nm}\\inst{curlybraket(btc.names_inst_i[i])}"
                    for i, nm in enumerate(btc.names)
                ]
            )
        elif btc.names:
            nm_extra = " \\and ".join([f"{nm}" for _, nm in enumerate(btc.names)])
        if btc.names_short:
            au_tex = f"\\author[{nms_extra}]{curlybraket(nm_extra)}"
            tex_collection.append(au_tex)
        if btc.insts_short:
            insts_extra = ",".join([inst for inst in btc.insts_short])
        if btc.insts and btc.insts_i:
            inst_extra = "\n".join(
                [
                    f"\\inst{curlybraket(btc.insts_i[i])}\n{inst}"
                    for i, inst in enumerate(btc.insts)
                ]
            )
        if btc.insts_short:
            inst_tex = f"\\institute[{insts_extra}]" + curlybraket(inst_extra)
            tex_collection.append(inst_tex)
        if btc.meeting:
            meeting_tex = f"\\date{curlybraket(btc.meeting)}"
            tex_collection.append(meeting_tex)
        if btc.meeting_short and btc.meeting:
            meeting_tex = f"\\date[{btc.meeting_short}]{curlybraket(btc.meeting)}"
            tex_collection.append(meeting_tex)
        if btc.logo_paths:
            logo_extra = "\n".join(
                [
                    f"\\includegraphics[height=1cm]{curlybraket(abspath(p))}"
                    for p in btc.logo_paths
                ]
            )
            logo_tex = f"\\logo{curlybraket(logo_extra)}"
            tex_collection.append(logo_tex)
        return "\n".join(tex_collection)


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
    def __init__(self, ctrl: Ctrl):
        super().__init__()
        self._ctrl = ctrl

    def parse(self):
        if self._ctrl == Ctrl.Begin:
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
