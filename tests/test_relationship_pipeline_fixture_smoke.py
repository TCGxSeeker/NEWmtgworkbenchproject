import copy
import json
import unittest
from pathlib import Path

from mtg_workbench.deckbuilder.behavioral_atom_extraction import (
    extract_card_behavioral_profile,
)
from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.card_relationship_report import (
    build_card_relationship_report,
)
from mtg_workbench.deckbuilder.relationship_edge_derivation import (
    derive_relationship_edges,
)
from mtg_workbench.deckbuilder.relationship_pipeline_smoke import (
    build_relationship_pipeline_smoke_report,
)


FIXTURE_DIRECTORY = Path("tests/fixtures/relationships")
INPUT_FIXTURE = FIXTURE_DIRECTORY / "relationship_pipeline_cards.json"
EXPECTED_FIXTURE = (
    FIXTURE_DIRECTORY / "relationship_pipeline_expected_report.json"
)


class RelationshipPipelineFixtureSmokeTests(unittest.TestCase):
    def test_pipeline_matches_expected_fixture(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))
        expected = json.loads(
            EXPECTED_FIXTURE.read_text(encoding="utf-8-sig")
        )

        actual = build_relationship_pipeline_smoke_report(source)

        self.assertEqual(actual, expected)

    def test_pipeline_is_deterministic(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))

        first = build_relationship_pipeline_smoke_report(source)
        second = build_relationship_pipeline_smoke_report(source)

        self.assertEqual(first, second)

    def test_pipeline_does_not_mutate_source_fixture(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))
        original = copy.deepcopy(source)

        build_relationship_pipeline_smoke_report(source)

        self.assertEqual(source, original)

    def test_unsupported_record_produces_no_atoms(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))
        unsupported = next(
            entry
            for entry in source["entries"]
            if entry["entry_id"] == "unsupported-entry"
        )

        profile = extract_card_behavioral_profile(
            unsupported["record"]
        )

        self.assertEqual(profile.outputs, ())
        self.assertEqual(profile.costs, ())
        self.assertEqual(profile.emitted_events, ())
        self.assertEqual(profile.observed_events, ())

    def test_fixture_only_derives_declared_pairs(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))

        report = build_relationship_pipeline_smoke_report(source)
        edge_pairs = _edge_pairs(report)
        declared_pairs = {
            (
                pair["source_entry_id"],
                pair["target_entry_id"],
            )
            for pair in source["pairs"]
        }

        self.assertLessEqual(edge_pairs, declared_pairs)
        self.assertEqual(
            edge_pairs,
            {
                (
                    "treasure-maker-entry",
                    "treasure-consumer-entry",
                ),
                (
                    "discard-outlet-entry",
                    "discard-listener-entry",
                ),
            },
        )

    def test_pipeline_does_not_add_undeclared_event_pairs(self) -> None:
        source = json.loads(INPUT_FIXTURE.read_text(encoding="utf-8-sig"))
        modified = copy.deepcopy(source)
        modified["pairs"] = [
            pair
            for pair in modified["pairs"]
            if pair["source_entry_id"] != "discard-outlet-entry"
        ]

        report = build_relationship_pipeline_smoke_report(modified)

        self.assertEqual(
            _edge_pairs(report),
            {
                (
                    "treasure-maker-entry",
                    "treasure-consumer-entry",
                ),
            },
        )

    def test_direct_pipeline_components_agree(self) -> None:
        treasure_source = extract_card_behavioral_profile(
            {
                "name": "Fixture Treasure Maker",
                "oracle_id": "fixture-treasure-maker",
                "oracle_text": "Create a Treasure token.",
            }
        )

        treasure_target = CardBehavioralProfile(
            card_name="Fixture Treasure Consumer",
            oracle_id="fixture-treasure-consumer",
            costs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=(
                        "Sacrifice a Treasure: Draw a card.",
                    ),
                    conditions=(),
                    zones=(),
                ),
            ),
        )

        event_source = CardBehavioralProfile(
            card_name="Fixture Discard Outlet",
            oracle_id="fixture-discard-outlet",
            emitted_events=(
                BehaviorAtom(
                    kind="card_discarded",
                    oracle_evidence=("Discard a card:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        event_target = CardBehavioralProfile(
            card_name="Fixture Discard Listener",
            oracle_id="fixture-discard-listener",
            observed_events=(
                BehaviorAtom(
                    kind="card_discarded",
                    oracle_evidence=(
                        "Whenever you discard a card, draw a card.",
                    ),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = (
            derive_relationship_edges(
                source_entry_id="treasure-maker-entry",
                source_profile=treasure_source,
                target_entry_id="treasure-consumer-entry",
                target_profile=treasure_target,
            )
            + derive_relationship_edges(
                source_entry_id="discard-outlet-entry",
                source_profile=event_source,
                target_entry_id="discard-listener-entry",
                target_profile=event_target,
            )
        )

        report = build_card_relationship_report(edges)

        self.assertEqual(report.relationship_count, 2)


def _edge_pairs(report: dict[str, object]) -> set[tuple[str, str]]:
    edges = report["machine_evidence"]["edges"]  # type: ignore[index]

    return {
        (
            edge["source_entry_id"],
            edge["target_entry_id"],
        )
        for edge in edges
    }


if __name__ == "__main__":
    unittest.main()
