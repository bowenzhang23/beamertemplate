from beamert.component import *
import os, subprocess, logging


class BeamerCompiler(object):
    def __init__(self, components, cmd="pdflatex", verbose=False, force=False):
        self._components = components
        self._cmd = cmd
        self._logger = logging.getLogger("Compiler")
        self._force = force
        logging.basicConfig(
            format="%(asctime)s %(levelname)-8s %(name)-15s %(message)s"
        )
        self._logger.setLevel(logging.DEBUG if verbose else logging.INFO)
        self._logger.info("Initiating compiler ..")
        self._width = 60
    
    def _hint_missing_dollar(self):
        self._logger.info("Found error \"Missing $ inserted\"")
        self._logger.info("Possible mistakes: 1) math expression 2) charactor '_' not backslashed 3) ..")

    def _hint_undefined_control_sequence(self, lines):
        for i, line in enumerate(lines):
            if "! Undefined control sequence" in line:
                break
        self._logger.info("Found error \"Undefined control sequence\"")
        self._logger.info(f"Possible mistake with {lines[i+1]} ..")

    def _hint_illegal_unit_measure(self):
        self._logger.info("Found error \"Illegal unit of measure\"")
        self._logger.info(f"Possible mistake with \"width\" in \"includegraphics\"")

    def _hint(self, msg):
        """TODO add more hints for errors"""
        lines = msg.splitlines()
        self._logger.info(f" Hints ".center(self._width, "-"))
        if "! Missing $ inserted." in msg:
            self._hint_missing_dollar()
        if "! Undefined control sequence" in msg:
            self._hint_undefined_control_sequence(lines)
        if "! Illegal unit of measure" in msg:
            self._hint_illegal_unit_measure()
        else:
            self._logger.info("None")

    def compile(self, output_path):
        def _compile(output_path):
            text = "\n".join([c.parse() for c in self._components])
            try:
                with open(output_path, "w" if self._force else "x") as f:
                    f.write(text)
                return True
            except FileExistsError:
                override = input("File already exist! Override? [Y/n] ")
                if override == "Y" or override == "y":
                    with open(output_path, "w") as f:
                        f.write(text)
                        return True
            return False

        if _compile(output_path):
            self._logger.info(f"[Success] Wrote in {output_path}")
            try:
                out_dir = f"-output-directory={os.path.dirname(output_path)}"
                popen = subprocess.Popen(
                    f"{self._cmd} -interaction=nonstopmode {out_dir} {output_path}",
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
                stdout = popen.stdout.read().decode()
                stderr = popen.stderr.read().decode()
                self._logger.debug(f" {self._cmd} stdout ".center(self._width, "-"))
                self._logger.debug(stdout)
                self._logger.debug(f" {self._cmd} stderr ".center(self._width, "-"))
                self._logger.debug(stderr)
                popen.wait()
                rcode = popen.returncode
                self._logger.info(f"CMD {self._cmd} returning {rcode}")
                if rcode == 0:
                    pdf_path = output_path.replace(".tex", ".pdf")
                    self._logger.info(f"[Success] Pdf in {pdf_path}")
                else:
                    self._hint(stdout)
                    self._logger.error(f"[Failed] {self._cmd} failed to compile..")
            except Exception as e:
                self._logger.error(f"[Failed] {e}")

        else:
            self._logger.error(f"[Failed] No changes are made..")
