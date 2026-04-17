import re

class InputValidator:

    def validate_target(self, target):

        if not target:
            return False

        pattern = re.compile(
            r'^(http|https)://[a-zA-Z0-9.-]+'
        )

        return bool(pattern.match(target))