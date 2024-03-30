from beamert.component import *

btc = BeamerTitleCollection()
btc.title = "Welcome to the Jungle"
btc.title_short = "WTTJ"
btc.title_sub = "a gentle introduction"
btc.names = ["Black Zombie", "Lucky Rogue"]
btc.names_short = ["B. Zombie", ]
btc.names_inst_i = ["1, 2", "2"]
btc.insts = ["Pepperland", "Ultra Station"]
btc.insts_short = ["Pl", ]
btc.insts_i = ["1", "2"]
btc.meeting = "Universe Edge Concert"
btc.meeting_short = "UEC"
btc.logo_paths = ["test/figures/logo.png", ]

components = [
    # Header and Style
    BeamerHeader(),
    BeamerStyle(),
    # Basic info and settings
    BeamerTitleSetting(btc=btc),
    BeamerTocSetting(),
    # Begin document
    BeamerDocumentCtrl(Ctrl.Begin),
    # Frames
    BeamerTitleFrame(),
    BeamerTocFrame("Outline"),
    BeamerSection("Section One", level=1),
    BeamerEmptyFrame(),
    BeamerFileFrame("test/frames/frame_sample.tex"),
    BeamerFileFrame("test/frames/frame_figures.tex"),
    BeamerSection("Section Two", level=1),
    BeamerEmptyFrame(),
    BeamerFileFrame("test/frames/frame_twocolumn.tex"),
    # End document
    BeamerDocumentCtrl(Ctrl.End),
]