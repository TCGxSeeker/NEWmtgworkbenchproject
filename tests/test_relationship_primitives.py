import unittest

from mtg_workbench.deckbuilder.relationship_primitives import (
    CONFIDENCE_BANDS,
    EVENT_KINDS,
    RELATIONSHIP_TYPES,
    RESOURCE_KINDS,
    RelationshipEdge,
    RelationshipEvidence,
    RelationshipPrimitiveError,
)


class RelationshipPrimitiveTests(unittest.TestCase):
    def test_vocabulary_matches_locked_v0_contract(self) -> None:
        self.assertEqual(
            RESOURCE_KINDS,
            (
                "mana",
                "treasure",
                "artifact",
                "creature",
                "card_in_hand",
                "graveyard_card",
            ),
        )
        self.assertEqual(
            EVENT_KINDS,
            (
                "spell_cast",
                "noncreature_spell_cast",
                "permanent_entered",
                "attack_declared",
                "combat_damage_dealt",
                "card_discarded",
                "permanent_sacrificed",
                "creature_died",
                "card_drawn",
            ),
        )
        self.assertEqual(
            RELATIONSHIP_TYPES,
            (
                "supplies",
                "triggers",
                "enables",
                "amplifies",
                "protects",
                "recurs",
                "conflicts_with",
            ),
        )
        self.assertEqual(CONFIDENCE_BANDS, (0, 25, 50, 75, 100))

    def test_relationship_evidence_preserves_factual_fields(self) -> None:
        evidence = RelationshipEvidence(
            source_behavior="outputs:treasure",
            target_behavior="costs:artifact",
            oracle_evidence=(
                "Create a Treasure token.",
                "Sacrifice an artifact: Draw a card.",
            ),
            conditions=("source ability resolves",),
            zones=("battlefield",),
            confidence_band=100,
            derivation_rule="resource_output_matches_cost",
        )

        self.assertEqual(
            evidence.to_dict(),
            {
                "conditions": ["source ability resolves"],
                "confidence_band": 100,
                "derivation_rule": "resource_output_matches_cost",
                "oracle_evidence": [
                    "Create a Treasure token.",
                    "Sacrifice an artifact: Draw a card.",
                ],
                "source_behavior": "outputs:treasure",
                "target_behavior": "costs:artifact",
                "zones": ["battlefield"],
            },
        )

    def test_relationship_edge_preserves_entry_identity(self) -> None:
        edge = RelationshipEdge(
            source_entry_id="entry-source",
            target_entry_id="entry-target",
            relationship_type="supplies",
            evidence=RelationshipEvidence(
                source_behavior="outputs:treasure",
                target_behavior="costs:artifact",
                oracle_evidence=("Create a Treasure token.",),
                conditions=(),
                zones=("battlefield",),
                confidence_band=75,
                derivation_rule="resource_output_matches_cost",
            ),
        )

        self.assertEqual(edge.source_entry_id, "entry-source")
        self.assertEqual(edge.target_entry_id, "entry-target")
        self.assertEqual(edge.relationship_type, "supplies")
        self.assertEqual(
            edge.to_dict(),
            {
                "evidence": {
                    "conditions": [],
                    "confidence_band": 75,
                    "derivation_rule": "resource_output_matches_cost",
                    "oracle_evidence": ["Create a Treasure token."],
                    "source_behavior": "outputs:treasure",
                    "target_behavior": "costs:artifact",
                    "zones": ["battlefield"],
                },
                "relationship_type": "supplies",
                "source_entry_id": "entry-source",
                "target_entry_id": "entry-target",
            },
        )

    def test_unknown_relationship_type_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "Unsupported relationship type",
        ):
            RelationshipEdge(
                source_entry_id="a",
                target_entry_id="b",
                relationship_type="converts",
                evidence=RelationshipEvidence(
                    source_behavior="outputs:mana",
                    target_behavior="costs:mana",
                    oracle_evidence=("Add one mana.",),
                    conditions=(),
                    zones=("battlefield",),
                    confidence_band=100,
                    derivation_rule="fixture",
                ),
            )

    def test_unknown_confidence_band_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "Unsupported confidence band",
        ):
            RelationshipEvidence(
                source_behavior="outputs:mana",
                target_behavior="costs:mana",
                oracle_evidence=("Add one mana.",),
                conditions=(),
                zones=("battlefield",),
                confidence_band=60,
                derivation_rule="fixture",
            )

    def test_blank_required_fields_are_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "source_entry_id",
        ):
            RelationshipEdge(
                source_entry_id=" ",
                target_entry_id="b",
                relationship_type="supplies",
                evidence=RelationshipEvidence(
                    source_behavior="outputs:mana",
                    target_behavior="costs:mana",
                    oracle_evidence=("Add one mana.",),
                    conditions=(),
                    zones=("battlefield",),
                    confidence_band=100,
                    derivation_rule="fixture",
                ),
            )

    def test_collection_fields_are_normalized_deterministically(self) -> None:
        evidence = RelationshipEvidence(
            source_behavior="outputs:treasure",
            target_behavior="costs:artifact",
            oracle_evidence=(
                "Second evidence.",
                "First evidence.",
                "Second evidence.",
            ),
            conditions=("requires target", "requires source", "requires target"),
            zones=("graveyard", "battlefield", "graveyard"),
            confidence_band=50,
            derivation_rule="fixture",
        )

        self.assertEqual(
            evidence.oracle_evidence,
            ("First evidence.", "Second evidence."),
        )
        self.assertEqual(
            evidence.conditions,
            ("requires source", "requires target"),
        )
        self.assertEqual(
            evidence.zones,
            ("battlefield", "graveyard"),
        )

    def test_self_relationship_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            RelationshipPrimitiveError,
            "different deck entries",
        ):
            RelationshipEdge(
                source_entry_id="same-entry",
                target_entry_id="same-entry",
                relationship_type="supplies",
                evidence=RelationshipEvidence(
                    source_behavior="outputs:mana",
                    target_behavior="costs:mana",
                    oracle_evidence=("Add one mana.",),
                    conditions=(),
                    zones=("battlefield",),
                    confidence_band=100,
                    derivation_rule="fixture",
                ),
            )


if __name__ == "__main__":
    unittest.main()
