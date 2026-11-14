from libqtile.widget import CapsNumLockIndicator
import re
import subprocess


class MyCapsNumLockIndicator(CapsNumLockIndicator):

    def get_indicators(self):
        try:
            output = self.call_process(["xset", "q"])
        except (OSError, subprocess.CalledProcessError):
            return []
        if output.startswith("Keyboard"):
            indicators = re.findall(r"(Caps)\s+Lock:\s*(\w*)", output)
            return indicators
        return []

    def parse(self, raw: str):
        indicators = self.get_indicators()
        status = " ".join([f"<b>{indicator[0].lower()}</b>:"+indicator[1].lower()
                           if indicator[1].lower()=="on" else "" for indicator in indicators])
        return status
