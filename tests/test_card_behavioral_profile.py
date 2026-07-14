import unittest

from mtg_workbench.deckbuilder.card_behavioral_profile import (
    BehaviorAtom,
    CardBehavioralProfile,
    CardBehavioralProfileError,
)


class CardBehavioralProfileTests(unittest.TestCase):
    def test_behavior_atom_preserves_factual_evidence(self) -> None:
        atom = BehaviorAtom(
            kind="treasure",
            oracle_evidence=("Create a Treasure token.",),
            conditions=("ability resolves",),
            zones=("battlefield",),
        )

        self.assertEqual(
            atom.to_dict(),
            {
                "conditions": ["ability resolves"],
                "kind": "treasure",
                "oracle_evidence": ["Create a Treasure token."],
                "zones": ["battlefield"],
            },
        )

    def test_profile_preserves_all_behavior_dimensions(self) -> None:
        profile = CardBehavioralProfile(
            card_name="Treasure Helper",
            oracle_id="oracle-helper",
            outputs=(
                BehaviorAtom(
                    kind="treasure",
                    oracle_evidence=("Create a Treasure token.",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
            costs=(
                BehaviorAtom(
                    kind="artifact",
                    oracle_evidence=("Sacrifice an artifact:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
            requirements=(),
            emitted_events=(
                BehaviorAtom(
                    kind="permanent_sacrificed",
                    oracle_evidence=("Sacrifice an artifact:",),
                    conditions=(),
                    zones=("battlefield",),
                ),
            ),
            observed_events=(),
            permissions=(),
            modifiers=(),
            zone_constraints=("battlefield",),
            timing_constraints=("sorcery_speed",),
        )

        payload = profile.to_dict()

        self.assertEqual(payload["card_name"], "Treasure Helper")
        self.assertEqual(payload["oracle_id"], "oracle-helper")
        self.assertEqual(payload["outputs"][0]["kind"], "treasure")
        self.assertEqual(payload["costs"][0]["kind"], "artifact")
        self.assertEqual(
            payload["emitted_events"][0]["kind"],
            "permanent_sacrificed",
        )
        self.assertEqual(payload["zone_constraints"], ["battlefield"])
        self.assertEqual(payload["timing_constraints"], ["sorcery_speed"])

    def test_resource_dimensions_reject_unknown_kinds(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "Unsupported output kind",
        ):
            CardBehavioralProfile(
                card_name="Mystery Card",
                oracle_id=None,
                outputs=(
                    BehaviorAtom(
                        kind="energy_counter",
                        oracle_evidence=("Get an energy counter.",),
                        conditions=(),
                        zones=("battlefield",),
                    ),
                ),
            )

    def test_event_dimensions_reject_unknown_kinds(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "Unsupported emitted event kind",
        ):
            CardBehavioralProfile(
                card_name="Mystery Card",
                oracle_id=None,
                emitted_events=(
                    BehaviorAtom(
                        kind="turn_started",
                        oracle_evidence=("At the beginning of your turn",),
                        conditions=(),
                        zones=("battlefield",),
                    ),
                ),
            )

    def test_atom_requires_oracle_evidence(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "oracle_evidence",
        ):
            BehaviorAtom(
                kind="mana",
                oracle_evidence=(),
                conditions=(),
                zones=("battlefield",),
            )

    def test_blank_card_name_is_rejected(self) -> None:
        with self.assertRaisesRegex(
            CardBehavioralProfileError,
            "card_name",
        ):
            CardBehavioralProfile(
                card_name=" ",
                oracle_id=None,
            )

    def test_atom_collections_are_deterministic(self) -> None:
        atom = BehaviorAtom(
            kind="treasure",
            oracle_evidence=(
                "Second sentence.",
                "First sentence.",
                "Second sentence.",
            ),
            conditions=("condition-b", "condition-a", "condition-b"),
            zones=("graveyard", "battlefield", "graveyard"),
        )

        self.assertEqual(
            atom.oracle_evidence,
            ("First sentence.", "Second sentence."),
        )
        self.assertEqual(
            atom.conditions,
            ("condition-a", "condition-b"),
        )
        self.assertEqual(
            atom.zones,
            ("battlefield", "graveyard"),
        )

    def test_profile_dimensions_are_deterministically_ordered(self) -> None:
        first = BehaviorAtom(
            kind="treasure",
            oracle_evidence=("Create a Treasure token.",),
            conditions=(),
            zones=("battlefield",),
        )
        second = BehaviorAtom(
            kind="artifact",
            oracle_evidence=("Create an artifact token.",),
            conditions=(),
            zones=("battlefield",),
        )

        profile = CardBehavioralProfile(
            card_name="Ordered Helper",
            oracle_id=None,
            outputs=(first, second, first),
            zone_constraints=("graveyard", "battlefield", "graveyard"),
            timing_constraints=("instant_speed", "sorcery_speed", "instant_speed"),
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.outputs),
            ("artifact", "treasure"),
        )
        self.assertEqual(
            profile.zone_constraints,
            ("battlefield", "graveyard"),
        )
        self.assertEqual(
            profile.timing_constraints,
            ("instant_speed", "sorcery_speed"),
        )


if __name__ == "__main__":
    unittest.main()
