import copy
import unittest

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.relationship_pair_inspection import (
    RelationshipPairInspectionError,
    inspect_relationship_pair,
)


def treasure_maker_profile() -> CardBehavioralProfile:
    return CardBehavioralProfile(
        card_name="Fixture Treasure Maker",
        oracle_id="fixture-treasure-maker",
        outputs=(
            BehaviorAtom(
                kind="treasure",
                oracle_evidence=("Create a Treasure token.",),
                conditions=(),
                zones=(),
            ),
        ),
    )


def treasure_consumer_profile() -> CardBehavioralProfile:
    return CardBehavioralProfile(
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


def unrelated_profile() -> CardBehavioralProfile:
    return CardBehavioralProfile(
        card_name="Fixture Unrelated Card",
        oracle_id="fixture-unrelated-card",
        outputs=(
            BehaviorAtom(
                kind="creature",
                oracle_evidence=("Create a creature token.",),
                conditions=(),
                zones=(),
            ),
        ),
    )


class RelationshipPairInspectionTests(unittest.TestCase):
    def setUp(self) -> None:
        self.profiles = {
            "maker-entry": treasure_maker_profile(),
            "consumer-entry": treasure_consumer_profile(),
            "unrelated-entry": unrelated_profile(),
        }

    def test_inspects_one_explicit_pair(self) -> None:
        report = inspect_relationship_pair(
            source_entry_id="maker-entry",
            target_entry_id="consumer-entry",
            profiles_by_entry_id=self.profiles,
        )

        self.assertEqual(report.relationship_count, 1)
        self.assertEqual(report.relationship_types, ("supplies",))

        edge = report.edges[0]
        self.assertEqual(edge.source_entry_id, "maker-entry")
        self.assertEqual(edge.target_entry_id, "consumer-entry")
        self.assertEqual(edge.relationship_type, "supplies")
        self.assertEqual(
            edge.evidence.source_behavior,
            "outputs:treasure",
        )
        self.assertEqual(
            edge.evidence.target_behavior,
            "costs:treasure",
        )

    def test_no_supported_match_returns_empty_report(self) -> None:
        report = inspect_relationship_pair(
            source_entry_id="unrelated-entry",
            target_entry_id="consumer-entry",
            profiles_by_entry_id=self.profiles,
        )

        self.assertEqual(report.relationship_count, 0)
        self.assertEqual(report.relationship_types, ())
        self.assertEqual(
            report.user_summary,
            "No factual card relationships were provided.",
        )

    def test_direction_is_not_reversed_automatically(self) -> None:
        report = inspect_relationship_pair(
            source_entry_id="consumer-entry",
            target_entry_id="maker-entry",
            profiles_by_entry_id=self.profiles,
        )

        self.assertEqual(report.relationship_count, 0)

    def test_missing_source_profile_is_reported(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "No behavioral profile found for source entry",
        ):
            inspect_relationship_pair(
                source_entry_id="missing-entry",
                target_entry_id="consumer-entry",
                profiles_by_entry_id=self.profiles,
            )

    def test_missing_target_profile_is_reported(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "No behavioral profile found for target entry",
        ):
            inspect_relationship_pair(
                source_entry_id="maker-entry",
                target_entry_id="missing-entry",
                profiles_by_entry_id=self.profiles,
            )

    def test_same_entry_pair_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "different deck entries",
        ):
            inspect_relationship_pair(
                source_entry_id="maker-entry",
                target_entry_id="maker-entry",
                profiles_by_entry_id=self.profiles,
            )

    def test_non_string_source_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "source_entry_id must be a string",
        ):
            inspect_relationship_pair(
                source_entry_id=None,
                target_entry_id="consumer-entry",
                profiles_by_entry_id=self.profiles,
            )

    def test_empty_target_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "target_entry_id must be a non-empty string",
        ):
            inspect_relationship_pair(
                source_entry_id="maker-entry",
                target_entry_id="   ",
                profiles_by_entry_id=self.profiles,
            )

    def test_non_mapping_profile_input_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "profiles_by_entry_id must be a mapping",
        ):
            inspect_relationship_pair(
                source_entry_id="maker-entry",
                target_entry_id="consumer-entry",
                profiles_by_entry_id=None,
            )

    def test_entry_ids_are_normalized_before_lookup(self) -> None:
        report = inspect_relationship_pair(
            source_entry_id="  maker-entry  ",
            target_entry_id="  consumer-entry  ",
            profiles_by_entry_id=self.profiles,
        )

        self.assertEqual(report.relationship_count, 1)
        self.assertEqual(
            report.edges[0].source_entry_id,
            "maker-entry",
        )
        self.assertEqual(
            report.edges[0].target_entry_id,
            "consumer-entry",
        )

    def test_invalid_profile_mapping_value_is_rejected(self) -> None:
        profiles = dict(self.profiles)
        profiles["consumer-entry"] = {"card_name": "not a profile"}

        with self.assertRaisesRegex(
            RelationshipPairInspectionError,
            "must be a CardBehavioralProfile",
        ):
            inspect_relationship_pair(
                source_entry_id="maker-entry",
                target_entry_id="consumer-entry",
                profiles_by_entry_id=profiles,
            )

    def test_profiles_mapping_is_not_mutated(self) -> None:
        before = copy.deepcopy(self.profiles)

        inspect_relationship_pair(
            source_entry_id="maker-entry",
            target_entry_id="consumer-entry",
            profiles_by_entry_id=self.profiles,
        )

        self.assertEqual(self.profiles, before)


if __name__ == "__main__":
    unittest.main()
