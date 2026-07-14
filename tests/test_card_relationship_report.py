import unittest

from mtg_workbench.deckbuilder.card_relationship_report import (
    CardRelationshipReportError,
    build_card_relationship_report,
)
from mtg_workbench.deckbuilder.relationship_primitives import (
    RelationshipEdge,
    RelationshipEvidence,
)


def make_edge(
    *,
    source_entry_id: str,
    target_entry_id: str,
    relationship_type: str,
    source_behavior: str,
    target_behavior: str,
    derivation_rule: str,
) -> RelationshipEdge:
    return RelationshipEdge(
        source_entry_id=source_entry_id,
        target_entry_id=target_entry_id,
        relationship_type=relationship_type,
        evidence=RelationshipEvidence(
            source_behavior=source_behavior,
            target_behavior=target_behavior,
            oracle_evidence=(
                f"{source_behavior} evidence",
                f"{target_behavior} evidence",
            ),
            conditions=(),
            zones=("battlefield",),
            confidence_band=100,
            derivation_rule=derivation_rule,
        ),
    )


class CardRelationshipReportTests(unittest.TestCase):
    def test_empty_report_is_stable(self) -> None:
        report = build_card_relationship_report(())

        self.assertEqual(report.schema_version, "card_relationship_report.v0")
        self.assertEqual(report.relationship_count, 0)
        self.assertEqual(report.relationship_types, ())
        self.assertEqual(
            report.user_summary,
            "No factual card relationships were provided.",
        )

        self.assertEqual(
            report.to_dict(),
            {
                "schema_version": "card_relationship_report.v0",
                "user_summary": (
                    "No factual card relationships were provided."
                ),
                "relationship_count": 0,
                "relationship_types": [],
                "machine_evidence": {
                    "relationship_count": 0,
                    "relationship_type_counts": {},
                    "edges": [],
                },
                "explanations": [],
            },
        )

    def test_report_preserves_relationship_edges(self) -> None:
        edge = make_edge(
            source_entry_id="source-entry",
            target_entry_id="target-entry",
            relationship_type="supplies",
            source_behavior="outputs:treasure",
            target_behavior="costs:treasure",
            derivation_rule="exact_resource_output_matches_cost",
        )

        report = build_card_relationship_report((edge,))
        payload = report.to_dict()

        self.assertEqual(report.relationship_count, 1)
        self.assertEqual(report.relationship_types, ("supplies",))
        self.assertEqual(
            payload["machine_evidence"]["edges"],
            [edge.to_dict()],
        )
        self.assertEqual(
            payload["machine_evidence"]["relationship_type_counts"],
            {"supplies": 1},
        )

    def test_multiple_relationship_types_are_counted(self) -> None:
        edges = (
            make_edge(
                source_entry_id="source-a",
                target_entry_id="target-a",
                relationship_type="supplies",
                source_behavior="outputs:artifact",
                target_behavior="costs:artifact",
                derivation_rule="exact_resource_output_matches_cost",
            ),
            make_edge(
                source_entry_id="source-b",
                target_entry_id="target-b",
                relationship_type="triggers",
                source_behavior="emitted_events:card_discarded",
                target_behavior="observed_events:card_discarded",
                derivation_rule="exact_emitted_event_matches_observer",
            ),
        )

        report = build_card_relationship_report(edges)

        self.assertEqual(report.relationship_count, 2)
        self.assertEqual(
            report.relationship_types,
            ("supplies", "triggers"),
        )
        self.assertEqual(
            report.machine_evidence["relationship_type_counts"],
            {
                "supplies": 1,
                "triggers": 1,
            },
        )

    def test_edges_are_deterministically_ordered(self) -> None:
        trigger = make_edge(
            source_entry_id="source-b",
            target_entry_id="target-b",
            relationship_type="triggers",
            source_behavior="emitted_events:card_discarded",
            target_behavior="observed_events:card_discarded",
            derivation_rule="exact_emitted_event_matches_observer",
        )
        supply = make_edge(
            source_entry_id="source-a",
            target_entry_id="target-a",
            relationship_type="supplies",
            source_behavior="outputs:artifact",
            target_behavior="costs:artifact",
            derivation_rule="exact_resource_output_matches_cost",
        )

        report = build_card_relationship_report((trigger, supply))

        self.assertEqual(
            tuple(edge.relationship_type for edge in report.edges),
            ("supplies", "triggers"),
        )

    def test_explanations_are_factual_not_strategic(self) -> None:
        edge = make_edge(
            source_entry_id="source-entry",
            target_entry_id="target-entry",
            relationship_type="supplies",
            source_behavior="outputs:treasure",
            target_behavior="costs:treasure",
            derivation_rule="exact_resource_output_matches_cost",
        )

        report = build_card_relationship_report((edge,))

        self.assertEqual(
            report.explanations,
            (
                (
                    "source-entry supplies target-entry because "
                    "outputs:treasure exactly matches costs:treasure."
                ),
            ),
        )

        forbidden = (
            "good",
            "strong",
            "synergy",
            "powerful",
            "recommend",
            "combo",
        )
        explanation = report.explanations[0].casefold()

        for word in forbidden:
            self.assertNotIn(word, explanation)

    def test_debug_details_are_optional(self) -> None:
        edge = make_edge(
            source_entry_id="source-entry",
            target_entry_id="target-entry",
            relationship_type="supplies",
            source_behavior="outputs:treasure",
            target_behavior="costs:treasure",
            derivation_rule="exact_resource_output_matches_cost",
        )

        report = build_card_relationship_report((edge,))

        self.assertNotIn("debug_details", report.to_dict())
        self.assertEqual(
            report.to_dict(include_debug=True)["debug_details"],
            {
                "report_boundaries": {
                    "relationship_derivation": "not_performed",
                    "deck_wide_scanning": "not_implemented",
                    "all_pairs_comparison": "not_implemented",
                    "package_detection": "not_implemented",
                    "combo_solving": "not_implemented",
                    "synergy_scoring": "not_implemented",
                    "recommendations": "not_implemented",
                    "strategic_quality_judgments": "not_implemented",
                }
            },
        )

    def test_duplicate_edges_are_deduplicated(self) -> None:
        edge = make_edge(
            source_entry_id="source-entry",
            target_entry_id="target-entry",
            relationship_type="supplies",
            source_behavior="outputs:treasure",
            target_behavior="costs:treasure",
            derivation_rule="exact_resource_output_matches_cost",
        )

        report = build_card_relationship_report((edge, edge))

        self.assertEqual(report.relationship_count, 1)
        self.assertEqual(len(report.edges), 1)

    def test_non_edge_input_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardRelationshipReportError,
            "RelationshipEdge",
        ):
            build_card_relationship_report(("not-an-edge",))


if __name__ == "__main__":
    unittest.main()
