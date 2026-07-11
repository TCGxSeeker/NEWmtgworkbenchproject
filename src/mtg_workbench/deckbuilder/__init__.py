"""Deckbuilder workspace model and native JSON serialization."""

from mtg_workbench.deckbuilder.categories import (
    CategoryNormalization,
    CategoryTaxonomy,
    CategoryTaxonomyError,
    load_category_taxonomy,
    normalize_category_key,
)
from mtg_workbench.deckbuilder.role_rules import (
    EvidenceScoreBand,
    RoleDefinition,
    RoleRulesError,
    RoleRuleSet,
    load_role_rules,
    normalize_match_text,
    normalize_role_key,
)
from mtg_workbench.deckbuilder.role_evidence import (
    CardRoleFacts,
    RoleEvidenceMatch,
    match_all_role_evidence,
    match_role_evidence,
)
from mtg_workbench.deckbuilder.import_export import export_plain_text_decklist, import_plain_text_decklist
from mtg_workbench.deckbuilder.mutations import (
    WorkspaceMutationError,
    add_entry,
    decrease_quantity,
    find_entry,
    get_zone_entries,
    increase_quantity,
    list_entries,
    move_category,
    move_zone,
    remove_entry,
    set_commander,
    update_notes,
    update_tags,
)
from mtg_workbench.deckbuilder.models import DeckEntry, DeckWorkspace
from mtg_workbench.deckbuilder.serialization import load_workspace, save_workspace

__all__ = [
    "DeckEntry",
    "DeckWorkspace",
    "CategoryNormalization",
    "CategoryTaxonomy",
    "CategoryTaxonomyError",
    "match_role_evidence",
    "match_all_role_evidence",
    "RoleEvidenceMatch",
    "CardRoleFacts",
    "normalize_role_key",
    "normalize_match_text",
    "load_role_rules",
    "RoleRuleSet",
    "RoleRulesError",
    "RoleDefinition",
    "EvidenceScoreBand",
    "WorkspaceMutationError",
    "add_entry",
    "decrease_quantity",
    "export_plain_text_decklist",
    "find_entry",
    "get_zone_entries",
    "increase_quantity",
    "import_plain_text_decklist",
    "load_category_taxonomy",
    "list_entries",
    "load_workspace",
    "move_category",
    "move_zone",
    "normalize_category_key",
    "remove_entry",
    "save_workspace",
    "set_commander",
    "update_notes",
    "update_tags",
]
