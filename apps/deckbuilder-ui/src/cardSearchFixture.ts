export type CardSearchCandidate = {
  card_id: string
  card_name: string
  type_line: string
  categories: string[]
  tags: string[]
  mana_value: number
  colors: string[]
  color_identity: string[]
}

export const localCardSearchFixture: CardSearchCandidate[] = [
  {
    card_id: 'candidate-arcane-helper',
    card_name: 'Arcane Helper',
    type_line: 'Artifact',
    categories: ['Ramp'],
    tags: ['mana'],
    mana_value: 2,
    colors: [],
    color_identity: [],
  },
  {
    card_id: 'candidate-drawn-insight',
    card_name: 'Drawn Insight',
    type_line: 'Instant',
    categories: ['Draw'],
    tags: ['cards'],
    mana_value: 2,
    colors: ['U'],
    color_identity: ['U'],
  },
  {
    card_id: 'candidate-rootbound-growth',
    card_name: 'Rootbound Growth',
    type_line: 'Sorcery',
    categories: ['Ramp'],
    tags: ['land'],
    mana_value: 3,
    colors: ['G'],
    color_identity: ['G'],
  },
  {
    card_id: 'candidate-protective-veil',
    card_name: 'Protective Veil',
    type_line: 'Instant',
    categories: ['Protection'],
    tags: ['shield'],
    mana_value: 1,
    colors: ['W'],
    color_identity: ['W'],
  },
  {
    card_id: 'candidate-quiet-removal',
    card_name: 'Quiet Removal',
    type_line: 'Instant',
    categories: ['Removal'],
    tags: ['interaction'],
    mana_value: 2,
    colors: ['B'],
    color_identity: ['B'],
  },
  {
    card_id: 'candidate-grave-recall',
    card_name: 'Grave Recall',
    type_line: 'Sorcery',
    categories: ['Recursion'],
    tags: ['graveyard'],
    mana_value: 3,
    colors: ['B'],
    color_identity: ['B'],
  },
  {
    card_id: 'candidate-engine-piece',
    card_name: 'Engine Piece',
    type_line: 'Artifact',
    categories: ['Engine'],
    tags: ['value'],
    mana_value: 3,
    colors: [],
    color_identity: [],
  },
  {
    card_id: 'candidate-example-basic-land',
    card_name: 'Example Basic Land',
    type_line: 'Basic Land - Forest',
    categories: ['Lands'],
    tags: ['mana'],
    mana_value: 0,
    colors: [],
    color_identity: ['G'],
  },
]
