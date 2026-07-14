import copy
import unittest

from mtg_workbench.deckbuilder.card_record_pair_inspection import (
    CardRecordPairInspectionError,
    inspect_card_record_pair,
)


def treasure_maker_record() -> dict[str, object]:
    return {
        "name": "Fixture Treasure Maker",
        "oracle_id": "fixture-treasure-maker",
        "oracle_text": "Create a Treasure token.",
    }


def treasure_consumer_record() -> dict[str, object]:
    return {
        "name": "Fixture Treasure Consumer",
        "oracle_id": "fixture-treasure-consumer",
        "oracle_text": "{T}, Sacrifice a Treasure: Draw a card.",
    }


def unsupported_record() -> dict[str, object]:
    return {
        "name": "Fixture Unsupported Card",
        "oracle_id": "fixture-unsupported",
        "oracle_text": "Investigate, then scry 1.",
    }


class CardRecordPairInspectionTests(unittest.TestCase):
    def test_inspects_two_explicit_card_records(self) -> None:
        report = inspect_card_record_pair(
            source_entry_id="maker-entry",
            source_record=treasure_maker_record(),
            target_entry_id="consumer-entry",
            target_record=treasure_consumer_record(),
        )

        self.assertEqual(report.relationship_count, 1)
        self.assertEqual(report.relationship_types, ("supplies",))

        edge = report.edges[0]
        self.assertEqual(edge.source_entry_id, "maker-entry")
        self.assertEqual(edge.target_entry_id, "consumer-entry")
        self.assertEqual(
            edge.evidence.source_behavior,
            "outputs:treasure",
        )
        self.assertEqual(
            edge.evidence.target_behavior,
            "costs:treasure",
        )
        self.assertEqual(
            set(edge.evidence.oracle_evidence),
            {
                "Create a Treasure token.",
                "{T}, Sacrifice a Treasure: Draw a card.",
            },
        )

    def test_direction_is_not_reversed_automatically(self) -> None:
        report = inspect_card_record_pair(
            source_entry_id="consumer-entry",
            source_record=treasure_consumer_record(),
            target_entry_id="maker-entry",
            target_record=treasure_maker_record(),
        )

        self.assertEqual(report.relationship_count, 0)

    def test_unsupported_records_return_empty_report(self) -> None:
        report = inspect_card_record_pair(
            source_entry_id="unsupported-entry",
            source_record=unsupported_record(),
            target_entry_id="consumer-entry",
            target_record=treasure_consumer_record(),
        )

        self.assertEqual(report.relationship_count, 0)
        self.assertEqual(report.relationship_types, ())

    def test_non_mapping_source_record_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardRecordPairInspectionError,
            "source_record must be a mapping",
        ):
            inspect_card_record_pair(
                source_entry_id="maker-entry",
                source_record=None,
                target_entry_id="consumer-entry",
                target_record=treasure_consumer_record(),
            )

    def test_non_mapping_target_record_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardRecordPairInspectionError,
            "target_record must be a mapping",
        ):
            inspect_card_record_pair(
                source_entry_id="maker-entry",
                source_record=treasure_maker_record(),
                target_entry_id="consumer-entry",
                target_record=[],
            )

    def test_same_entry_pair_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardRecordPairInspectionError,
            "different deck entries",
        ):
            inspect_card_record_pair(
                source_entry_id="same-entry",
                source_record=treasure_maker_record(),
                target_entry_id="same-entry",
                target_record=treasure_consumer_record(),
            )

    def test_entry_ids_are_normalized(self) -> None:
        report = inspect_card_record_pair(
            source_entry_id="  maker-entry  ",
            source_record=treasure_maker_record(),
            target_entry_id="  consumer-entry  ",
            target_record=treasure_consumer_record(),
        )

        self.assertEqual(
            report.edges[0].source_entry_id,
            "maker-entry",
        )
        self.assertEqual(
            report.edges[0].target_entry_id,
            "consumer-entry",
        )

    def test_source_record_extraction_failure_is_clear(self) -> None:
        with self.assertRaisesRegex(
            CardRecordPairInspectionError,
            "Could not extract source behavioral profile",
        ):
            inspect_card_record_pair(
                source_entry_id="maker-entry",
                source_record={"oracle_text": "Create a Treasure token."},
                target_entry_id="consumer-entry",
                target_record=treasure_consumer_record(),
            )

    def test_input_records_are_not_mutated(self) -> None:
        source = treasure_maker_record()
        target = treasure_consumer_record()
        source_before = copy.deepcopy(source)
        target_before = copy.deepcopy(target)

        inspect_card_record_pair(
            source_entry_id="maker-entry",
            source_record=source,
            target_entry_id="consumer-entry",
            target_record=target,
        )

        self.assertEqual(source, source_before)
        self.assertEqual(target, target_before)


if __name__ == "__main__":
    unittest.main()
