import unittest

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
    CardBehavioralProfileError,
)
from mtg_workbench.deckbuilder.relationship_primitives import (
    RelationshipEdge,
    RelationshipEvidence,
    RelationshipPrimitiveError,
    relationship_edge_identity_key,
)


def make_evidence() -> RelationshipEvidence:
    return RelationshipEvidence(
        source_behavior="outputs:treasure",
        target_behavior="costs:treasure",
        oracle_evidence=("Create a Treasure token.",),
        conditions=(),
        zones=(),
        confidence_band=100,
        derivation_rule="exact_resource_output_matches_cost",
    )


class RelationshipPrimitiveInputHardeningTests(unittest.TestCase):
    def test_none_entry_id_is_rejected_instead_of_coerced(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "source_entry_id must be a string",
        ):
            RelationshipEdge(
                source_entry_id=None,
                target_entry_id="target-entry",
                relationship_type="supplies",
                evidence=make_evidence(),
            )

    def test_integer_entry_id_is_rejected_instead_of_coerced(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "target_entry_id must be a string",
        ):
            RelationshipEdge(
                source_entry_id="source-entry",
                target_entry_id=123,
                relationship_type="supplies",
                evidence=make_evidence(),
            )

    def test_none_behavior_text_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "source_behavior must be a string",
        ):
            RelationshipEvidence(
                source_behavior=None,
                target_behavior="costs:treasure",
                oracle_evidence=("Evidence.",),
                conditions=(),
                zones=(),
                confidence_band=100,
                derivation_rule="test_rule",
            )

    def test_shared_edge_identity_key_is_stable(self) -> None:
        edge = RelationshipEdge(
            source_entry_id="source-entry",
            target_entry_id="target-entry",
            relationship_type="supplies",
            evidence=make_evidence(),
        )

        self.assertEqual(
            relationship_edge_identity_key(edge),
            (
                "supplies",
                "outputs:treasure",
                "costs:treasure",
                ("Create a Treasure token.",),
                (),
                (),
                100,
                "exact_resource_output_matches_cost",
                "source-entry",
                "target-entry",
            ),
        )

    def test_string_oracle_evidence_is_rejected_as_collection(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "oracle_evidence must be an iterable of strings",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence="Create a Treasure token.",
                conditions=(),
                zones=(),
                confidence_band=100,
                derivation_rule="test_rule",
            )

    def test_string_conditions_are_rejected_as_collection(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "conditions must be an iterable of strings",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence=("Evidence.",),
                conditions="only during your turn",
                zones=(),
                confidence_band=100,
                derivation_rule="test_rule",
            )

    def test_none_zones_are_rejected_with_domain_error(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "zones must be an iterable of strings",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence=("Evidence.",),
                conditions=(),
                zones=None,
                confidence_band=100,
                derivation_rule="test_rule",
            )

    def test_bool_confidence_band_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "confidence_band must be an integer confidence band",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence=("Evidence.",),
                conditions=(),
                zones=(),
                confidence_band=False,
                derivation_rule="test_rule",
            )

    def test_float_confidence_band_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "confidence_band must be an integer confidence band",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence=("Evidence.",),
                conditions=(),
                zones=(),
                confidence_band=25.0,
                derivation_rule="test_rule",
            )

    def test_empty_relationship_evidence_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "oracle_evidence must contain at least one value",
        ):
            RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:treasure",
                oracle_evidence=(),
                conditions=(),
                zones=(),
                confidence_band=100,
                derivation_rule="test_rule",
            )

    def test_invalid_edge_evidence_object_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "evidence must be a RelationshipEvidence instance",
        ):
            RelationshipEdge(
                source_entry_id="source-entry",
                target_entry_id="target-entry",
                relationship_type="supplies",
                evidence={"not": "relationship evidence"},
            )


class BehavioralProfileInputHardeningTests(unittest.TestCase):
    def test_string_atom_evidence_is_rejected_as_collection(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "oracle_evidence must be an iterable of strings",
        ):
            BehaviorAtom(
                kind="treasure",
                oracle_evidence="Create a Treasure token.",
                conditions=(),
                zones=(),
            )

    def test_bytes_conditions_are_rejected_as_collection(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "conditions must be an iterable of strings",
        ):
            BehaviorAtom(
                kind="treasure",
                oracle_evidence=("Evidence.",),
                conditions=b"condition",
                zones=(),
            )

    def test_none_profile_atom_collection_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "outputs must be an iterable of BehaviorAtom values",
        ):
            CardBehavioralProfile(
                card_name="Fixture Card",
                oracle_id=None,
                outputs=None,
            )

    def test_invalid_profile_atom_object_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "outputs must contain only BehaviorAtom values",
        ):
            CardBehavioralProfile(
                card_name="Fixture Card",
                oracle_id=None,
                outputs=(object(),),
            )

    def test_non_string_oracle_id_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "oracle_id must be a string or None",
        ):
            CardBehavioralProfile(
                card_name="Fixture Card",
                oracle_id=123,
            )

    def test_valid_values_remain_sorted_and_deduplicated(self) -> None:
        atom = BehaviorAtom(
            kind="treasure",
            oracle_evidence=("Second.", "First.", "Second."),
            conditions=("B", "A", "B"),
            zones=("battlefield", "hand", "battlefield"),
        )

        self.assertEqual(atom.oracle_evidence, ("First.", "Second."))
        self.assertEqual(atom.conditions, ("A", "B"))
        self.assertEqual(atom.zones, ("battlefield", "hand"))


if __name__ == "__main__":
    unittest.main()
