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
                )
                self._logger.debug(popen.stdout.read().decode())
                popen.wait()
                rcode = popen.returncode
                self._logger.info(f"CMD {self._cmd} returning {rcode}")
                if rcode == 0:
                    pdf_path = output_path.replace(".tex", ".pdf")
                    self._logger.info(f"[Success] Pdf in {pdf_path}")
                else:
                    self._logger.error(f"[Failed] {self._cmd} failed to compile..")
            except Exception as e:
                self._logger.error(f"[Failed] {e}")

        else:
            self._logger.error(f"[Failed] No changes are made..")
