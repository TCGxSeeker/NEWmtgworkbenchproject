from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import unittest

from mtg_workbench.cli.main import main


FIXTURE_ROOT = Path(__file__).parent / "fixtures"


class CliParseTests(unittest.TestCase):
    def test_parse_command_outputs_stable_json(self) -> None:
        output = io.StringIO()
        with redirect_stdout(output):
            exit_code = main(
                [
                    "parse",
                    str(FIXTURE_ROOT / "decklists" / "plain_commander.txt"),
                    "--cards",
                    str(FIXTURE_ROOT / "cards" / "tiny_cards.json"),
                ]
            )

        self.assertEqual(exit_code, 0)
        payload = json.loads(output.getvalue())
        self.assertEqual(payload["commanders"][0]["name"], "Example Commander")
        self.assertEqual(payload["mainboard"][1]["quantity"], 35)
        self.assertEqual(payload["unknown_cards"][0]["raw_name"], "Unknown Mystery")
        self.assertEqual(payload["warnings"][0]["code"], "duplicate_non_basic")
        self.assertEqual(list(payload.keys()), sorted(payload.keys()))


if __name__ == "__main__":
    unittest.main()
