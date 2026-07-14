import unittest

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
)
from mtg_workbench.deckbuilder.relationship_edge_derivation import (
    derive_relationship_edges,
)


def make_profile(
    name: str,
    *,
    outputs: tuple[BehaviorAtom, ...] = (),
    costs: tuple[BehaviorAtom, ...] = (),
    emitted_events: tuple[BehaviorAtom, ...] = (),
    observed_events: tuple[BehaviorAtom, ...] = (),
) -> CardBehavioralProfile:
    return CardBehavioralProfile(
        card_name=name,
        oracle_id=None,
        outputs=outputs,
        costs=costs,
        emitted_events=emitted_events,
        observed_events=observed_events,
    )


class RelationshipEdgeDerivationTests(unittest.TestCase):
    def test_exact_resource_output_matches_cost(self) -> None:
        source = make_profile(
            "Treasure Maker",
            outputs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Create a Treasure token.",),
                    conditions=("ability resolves",),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Artifact Outlet",
            costs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Sacrifice a Treasure:",),
                    conditions=("activate ability",),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="source-entry",
            source_profile=source,
            target_entry_id="target-entry",
            target_profile=target,
        )

        self.assertEqual(len(edges), 1)

        edge = edges[0]

        self.assertEqual(edge.source_entry_id, "source-entry")
        self.assertEqual(edge.target_entry_id, "target-entry")
        self.assertEqual(edge.relationship_type, "supplies")
        self.assertEqual(
            edge.evidence.source_behavior,
            "outputs:treasure",
        )
        self.assertEqual(
            edge.evidence.target_behavior,
            "costs:treasure",
        )
        self.assertEqual(
            edge.evidence.oracle_evidence,
            (
                "Create a Treasure token.",
                "Sacrifice a Treasure:",
            ),
        )
        self.assertEqual(
            edge.evidence.conditions,
            ("ability resolves", "activate ability"),
        )
        self.assertEqual(edge.evidence.zones, ("battlefield",))
        self.assertEqual(edge.evidence.confidence_band, 100)
        self.assertEqual(
            edge.evidence.derivation_rule,
            "exact_resource_output_matches_cost",
        )

    def test_exact_emitted_event_matches_observer(self) -> None:
        source = make_profile(
            "Discard Outlet",
            emitted_events=(
                BehaviorAtom(
                    kind="card_discarded",
                    oracle_evidence=("Discard a card:",),
                    conditions=("activate ability",),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Discard Listener",
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

        edges = derive_relationship_edges(
            source_entry_id="discard-source",
            source_profile=source,
            target_entry_id="discard-target",
            target_profile=target,
        )

        self.assertEqual(len(edges), 1)
        self.assertEqual(edges[0].relationship_type, "triggers")
        self.assertEqual(
            edges[0].evidence.source_behavior,
            "emitted_events:card_discarded",
        )
        self.assertEqual(
            edges[0].evidence.target_behavior,
            "observed_events:card_discarded",
        )
        self.assertEqual(
            edges[0].evidence.derivation_rule,
            "exact_emitted_event_matches_observer",
        )
        self.assertEqual(edges[0].evidence.confidence_band, 100)

    def test_mismatched_resources_produce_no_edge(self) -> None:
        source = make_profile(
            "Treasure Maker",
            outputs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Create a Treasure token.",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Creature Outlet",
            costs=(
                BehaviorAtom(
                    kind="creature",
                    oracle_evidence=("Sacrifice a creature:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="source",
            source_profile=source,
            target_entry_id="target",
            target_profile=target,
        )

        self.assertEqual(edges, ())

    def test_mismatched_events_produce_no_edge(self) -> None:
        source = make_profile(
            "Discard Outlet",
            emitted_events=(
                BehaviorAtom(
                    kind="card_discarded",
                    oracle_evidence=("Discard a card:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Death Listener",
            observed_events=(
                BehaviorAtom(
                    kind="creature_died",
                    oracle_evidence=(
                        "Whenever another creature dies, draw a card.",
                    ),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="source",
            source_profile=source,
            target_entry_id="target",
            target_profile=target,
        )

        self.assertEqual(edges, ())

    def test_resource_and_event_matches_are_both_returned(self) -> None:
        source = make_profile(
            "Busy Source",
            outputs=(
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=("Create an artifact token.",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
            emitted_events=(
                BehaviorAtom(
                    kind="permanent_sacrificed",
                    oracle_evidence=("Sacrifice an artifact:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Busy Target",
            costs=(
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=("Sacrifice an artifact:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
            observed_events=(
                BehaviorAtom(
                    kind="permanent_sacrificed",
                    oracle_evidence=(
                        "Whenever you sacrifice a permanent, draw a card.",
                    ),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="busy-source",
            source_profile=source,
            target_entry_id="busy-target",
            target_profile=target,
        )

        self.assertEqual(
            tuple(edge.relationship_type for edge in edges),
            ("supplies", "triggers"),
        )

    def test_duplicate_matches_are_deduplicated(self) -> None:
        repeated = BehaviorAtom(
            kind="treasure",
            oracle_evidence=("Create a Treasure token.",),
            conditions=(),
            zones=("battlefield",),
        )

        source = make_profile(
            "Repeated Source",
            outputs=(repeated, repeated),
        )
        target = make_profile(
            "Treasure Consumer",
            costs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Sacrifice a Treasure:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="source",
            source_profile=source,
            target_entry_id="target",
            target_profile=target,
        )

        self.assertEqual(len(edges), 1)

    def test_output_order_is_deterministic(self) -> None:
        source = make_profile(
            "Ordered Source",
            outputs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Create a Treasure token.",),
                    conditions=(),
                    zones=("battlefield",),
                ),
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=("Create an artifact token.",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )
        target = make_profile(
            "Ordered Target",
            costs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Sacrifice a Treasure:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=("Sacrifice an artifact:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
        )

        edges = derive_relationship_edges(
            source_entry_id="source",
            source_profile=source,
            target_entry_id="target",
            target_profile=target,
        )

        self.assertEqual(
            tuple(edge.evidence.source_behavior for edge in edges),
            (
                "outputs:artifact",
                "outputs:treasure",
            ),
        )

    def test_empty_profiles_produce_no_edges(self) -> None:
        edges = derive_relationship_edges(
            source_entry_id="source",
            source_profile=make_profile("Empty Source"),
            target_entry_id="target",
            target_profile=make_profile("Empty Target"),
        )

        self.assertEqual(edges, ())


if __name__ == "__main__":
    unittest.main()
