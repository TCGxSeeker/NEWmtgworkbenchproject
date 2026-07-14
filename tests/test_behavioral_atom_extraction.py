import unittest

from mtg_workbench.deckbuilder.behavioral_atom_extraction import (
    extract_card_behavioral_profile,
)


class BehavioralAtomExtractionTests(unittest.TestCase):
    def test_extracts_treasure_output_from_exact_phrase(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Treasure Maker",
                "oracle_id": "oracle-treasure-maker",
                "oracle_text": "Create a Treasure token.",
            }
        )

        self.assertEqual(profile.card_name, "Treasure Maker")
        self.assertEqual(profile.oracle_id, "oracle-treasure-maker")
        self.assertEqual(
            tuple(atom.kind for atom in profile.outputs),
            ("treasure",),
        )
        self.assertEqual(
            profile.outputs[0].oracle_evidence,
            ("Create a Treasure token.",),
        )

    def test_extracts_discard_cost_and_event(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Discard Outlet",
                "oracle_text": "Discard a card: Draw a card.",
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.costs),
            ("card_in_hand",),
        )
        self.assertEqual(
            tuple(atom.kind for atom in profile.emitted_events),
            ("card_discarded",),
        )

    def test_extracts_artifact_sacrifice_cost_and_event(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Artifact Outlet",
                "oracle_text": "Sacrifice an artifact: Draw a card.",
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.costs),
            ("artifact",),
        )
        self.assertEqual(
            tuple(atom.kind for atom in profile.emitted_events),
            ("permanent_sacrificed",),
        )

    def test_extracts_noncreature_spell_observer(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Spell Listener",
                "oracle_text": (
                    "Whenever you cast a noncreature spell, "
                    "this creature gets +1/+1 until end of turn."
                ),
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.observed_events),
            ("noncreature_spell_cast",),
        )

    def test_multiple_supported_phrases_are_all_preserved(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Busy Helper",
                "oracle_text": (
                    "Create a Treasure token.\n"
                    "Discard a card: Draw a card."
                ),
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.outputs),
            ("treasure",),
        )
        self.assertEqual(
            tuple(atom.kind for atom in profile.costs),
            ("card_in_hand",),
        )
        self.assertEqual(
            tuple(atom.kind for atom in profile.emitted_events),
            ("card_discarded",),
        )

    def test_unsupported_wording_is_not_guessed(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Unsupported Helper",
                "oracle_text": (
                    "Investigate, then you may mill two cards "
                    "and untap a permanent."
                ),
            }
        )

        self.assertEqual(profile.outputs, ())
        self.assertEqual(profile.costs, ())
        self.assertEqual(profile.requirements, ())
        self.assertEqual(profile.emitted_events, ())
        self.assertEqual(profile.observed_events, ())
        self.assertEqual(profile.permissions, ())
        self.assertEqual(profile.modifiers, ())

    def test_missing_oracle_text_produces_empty_profile(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Textless Card",
                "oracle_id": "oracle-textless",
            }
        )

        self.assertEqual(profile.card_name, "Textless Card")
        self.assertEqual(profile.oracle_id, "oracle-textless")
        self.assertEqual(profile.outputs, ())
        self.assertEqual(profile.costs, ())
        self.assertEqual(profile.emitted_events, ())
        self.assertEqual(profile.observed_events, ())

    def test_extraction_is_case_insensitive_but_preserves_source_evidence(
        self,
    ) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Oddly Cased Card",
                "oracle_text": "CREATE A TREASURE TOKEN.",
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.outputs),
            ("treasure",),
        )
        self.assertEqual(
            profile.outputs[0].oracle_evidence,
            ("CREATE A TREASURE TOKEN.",),
        )


    def test_extracts_treasure_sacrifice_cost_and_event(self) -> None:
        profile = extract_card_behavioral_profile(
            {
                "name": "Treasure Consumer",
                "oracle_text": (
                    "{T}, Sacrifice a Treasure: Draw a card."
                ),
            }
        )

        self.assertEqual(
            tuple(atom.kind for atom in profile.costs),
            ("treasure",),
        )
        self.assertEqual(
            tuple(atom.kind for atom in profile.emitted_events),
            ("permanent_sacrificed",),
        )
        self.assertEqual(
            profile.costs[0].oracle_evidence,
            ("{T}, Sacrifice a Treasure: Draw a card.",),
        )

if __name__ == "__main__":
    unittest.main()
