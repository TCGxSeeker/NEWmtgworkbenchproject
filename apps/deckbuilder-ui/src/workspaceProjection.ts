export type WorkspaceViewEntry = {
  entry_id: string
  zone: 'commander' | 'mainboard' | 'maybeboard'
  quantity: number
  card_name: string
  input_name: string
  display_name: string | null
  categories: string[]
  tags: string[]
  secondary_tags: string[]
  imported_category: string | null
  normalized_category: string | null
  generic_category_hint: string | null
  is_unresolved: boolean
  card_fact_status: 'found' | 'missing' | 'ambiguous' | 'not_requested'
  type_line: string | null
  type_labels: string[]
  mana_value: number | null
  colors: string[] | null
  color_identity: string[] | null
}

export type WorkspaceViewGroup = {
  group_id: string
  label: string
  entry_count: number
  quantity_total: number
  entries: WorkspaceViewEntry[]
}

export type WorkspaceViewProjection = {
  schema_version: 'deck_workspace_view_projection.v0'
  deck_id: string
  deck_name: string
  group_by: string
  sort_by: string
  filter_text: string | null
  visible_entry_count: number
  visible_quantity_total: number
  grouped_entry_count: number
  grouped_quantity_total: number
  card_fact_lookup: {
    status: string
    found_count: number
    missing_count: number
    ambiguous_count: number
  }
  groups: WorkspaceViewGroup[]
}

export const workspaceViewProjection: WorkspaceViewProjection = {
  schema_version: 'deck_workspace_view_projection.v0',
  deck_id: 'see-the-deck-v0',
  deck_name: 'Fixture Commander Deck',
  group_by: 'category',
  sort_by: 'mana_value',
  filter_text: null,
  visible_entry_count: 6,
  visible_quantity_total: 40,
  grouped_entry_count: 6,
  grouped_quantity_total: 40,
  card_fact_lookup: {
    status: 'checked',
    found_count: 6,
    missing_count: 0,
    ambiguous_count: 0,
  },
  groups: [
    {
      group_id: 'commander',
      label: 'Commander',
      entry_count: 1,
      quantity_total: 1,
      entries: [
        {
          entry_id: 'entry-commander',
          zone: 'commander',
          quantity: 1,
          card_name: 'Example Commander',
          input_name: 'Example Commander',
          display_name: 'Example Commander',
          categories: ['Commander'],
          tags: ['core'],
          secondary_tags: [],
          imported_category: 'Commander',
          normalized_category: 'Commander',
          generic_category_hint: 'Commander',
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Legendary Creature - Example',
          type_labels: ['Creature'],
          mana_value: 3,
          colors: ['G'],
          color_identity: ['G'],
        },
      ],
    },
    {
      group_id: 'lands',
      label: 'Lands',
      entry_count: 1,
      quantity_total: 35,
      entries: [
        {
          entry_id: 'entry-land',
          zone: 'mainboard',
          quantity: 35,
          card_name: 'Example Basic Land',
          input_name: 'Basic Land Name',
          display_name: 'Example Basic Land',
          categories: ['Lands'],
          tags: [],
          secondary_tags: [],
          imported_category: 'Lands',
          normalized_category: 'Lands',
          generic_category_hint: 'Land',
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Basic Land - Forest',
          type_labels: ['Land'],
          mana_value: 0,
          colors: [],
          color_identity: ['G'],
        },
      ],
    },
    {
      group_id: 'ramp',
      label: 'Ramp',
      entry_count: 1,
      quantity_total: 1,
      entries: [
        {
          entry_id: 'entry-ramp',
          zone: 'mainboard',
          quantity: 1,
          card_name: 'Arcane Helper',
          input_name: 'Arcane Helper',
          display_name: 'Arcane Helper',
          categories: ['Ramp'],
          tags: ['mana'],
          secondary_tags: [],
          imported_category: 'Ramp',
          normalized_category: 'Ramp',
          generic_category_hint: 'Ramp',
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Artifact',
          type_labels: ['Artifact'],
          mana_value: 2,
          colors: [],
          color_identity: [],
        },
      ],
    },
    {
      group_id: 'creatures',
      label: 'Creatures',
      entry_count: 1,
      quantity_total: 1,
      entries: [
        {
          entry_id: 'entry-creature',
          zone: 'mainboard',
          quantity: 1,
          card_name: 'Alias Target',
          input_name: 'Alias Helper',
          display_name: 'Alias Target',
          categories: ['Creatures'],
          tags: [],
          secondary_tags: ['setup'],
          imported_category: 'Creatures',
          normalized_category: 'Creatures',
          generic_category_hint: 'Creature',
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Creature - Example',
          type_labels: ['Creature'],
          mana_value: 1,
          colors: ['G'],
          color_identity: ['G'],
        },
      ],
    },
    {
      group_id: 'recursion',
      label: 'Recursion',
      entry_count: 1,
      quantity_total: 1,
      entries: [
        {
          entry_id: 'entry-recursion',
          zone: 'mainboard',
          quantity: 1,
          card_name: "Can't Stay Away",
          input_name: "Can't Stay Away",
          display_name: "Can't Stay Away",
          categories: ['Recursion'],
          tags: [],
          secondary_tags: [],
          imported_category: 'Recursion',
          normalized_category: 'Recursion',
          generic_category_hint: 'Recursion',
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Sorcery',
          type_labels: ['Sorcery'],
          mana_value: 2,
          colors: ['W', 'B'],
          color_identity: ['W', 'B'],
        },
      ],
    },
    {
      group_id: 'maybeboard',
      label: 'Maybeboard',
      entry_count: 1,
      quantity_total: 1,
      entries: [
        {
          entry_id: 'entry-maybe',
          zone: 'maybeboard',
          quantity: 1,
          card_name: 'Maybe Card',
          input_name: 'Maybe Card',
          display_name: 'Maybe Card',
          categories: ['Maybeboard'],
          tags: [],
          secondary_tags: [],
          imported_category: 'Maybeboard',
          normalized_category: 'Maybeboard',
          generic_category_hint: null,
          is_unresolved: false,
          card_fact_status: 'found',
          type_line: 'Creature - Example',
          type_labels: ['Creature'],
          mana_value: 4,
          colors: ['G'],
          color_identity: ['G'],
        },
      ],
    },
  ],
}
