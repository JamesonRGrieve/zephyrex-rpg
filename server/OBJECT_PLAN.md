# Extension Object Plan

## Scope

This repo is a **Kanka / World Anvil replacement** — the worldbuilding and
campaign management backend. It is the single data layer that three downstream
consumers will build on top of:

1. **AI RPG framework** — user as GM with AI characters, or user as character
   with an AI GM
2. **Video games** — fantasy, zombie, sci-fi, etc.
3. **Virtual tabletop** — Foundry/Roll20-style

Only features **common across consumers** or **unique to the Kanka/World Anvil
worldbuilding domain** are planned and built in this repo. Scenes (playable
areas with placed entities, walls, lights, sounds, regions) are **in scope** —
all three consumers need a spatial canvas model; each renders it differently.
AI-specific runtime features (vector RAG, summarisation, STscript) and
video-game-specific features (physics, rendering, spawn points) are out of
scope — they live in their respective downstream repos.

---

## 1. Platform Feature Audit

### Kanka (verified via [API docs](https://app.kanka.io/api-docs/1.0/entities))

**Entity types** (19 + sub-resources):

| Entity | Key Fields |
|--------|------------|
| Characters | title, age, sex, pronouns, type, location_id, races[] (+ private_races[]), families[] (+ private_families[]), is_dead, traits (personality/appearance), is_personality_visible/pinned, is_appearance_pinned |
| Locations | parent_id (hierarchy), type |
| Maps | location_id, width, height, grid, min/max/initial_zoom, center_x/y, center_marker_id, is_real (OpenStreetMap) |
| Map Markers | map_id, latitude, longitude, name, icon, colour, opacity, size, custom_icon, custom_shape, visibility, group_id, entity_id, pin_size, is_draggable, circle |
| Map Layers | map_id, name, image, entry, position, visibility, type_id |
| Map Groups | map_id, name, is_shown, position |
| Organisations | parent_id, location_id, type; members (role, rank, status, is_private) |
| Families | parent_id, location_id, type; members |
| Items (Objects) | type, size, weight, price, location_id, character_id (holder) |
| Events | date, location_id, type, era_id |
| Calendars | months, weekdays, year length, leap years, moons, seasons, weather, epochs, intercalaries |
| Timelines | type; eras → timeline elements (event links, ordinal) |
| Quests | parent_quest_id (hierarchy), type, date, character_id; quest elements with entity links |
| Journals | date, location_id, character_id, type |
| Notes | type |
| Abilities | type, charges; linkable to any entity |
| Races | parent_race_id (sub-races), type |
| Creatures | location_id, type |
| Conversations | type, target_id; messages (character_id, text, is_in_character) |
| Dice Rolls | parameters, system |
| Property Kits | reusable attribute templates |
| Tags | parent_id (hierarchy), colour, type |

**Common entity fields** (all types): id, name, entry (rich text), type, image/image_full/image_thumb, has_custom_image, entity_image_uuid, entity_header_uuid, is_private, is_template, is_attributes_private, status_id, tags[], tooltip, created_at/by, updated_at/by, archived_at

**Entity sub-resources** (all types):

| Sub-resource | Description |
|-------------|-------------|
| Posts | Pinnable rich-text notes on any entity; per-post visibility, position |
| Connections (Relations) | Typed directed relationships between any two entities; attitude, colour, mirror/reciprocal, is_private |
| Properties (Attributes) | Structured KV: text, number, section, checkbox, random, star-rating; private flag; templates via Property Kits |
| Abilities | Abilities attached to any entity with charges |
| Inventory | Item + quantity on any entity (not just Characters) |
| Entity Assets | Files attached to entities |
| Reminders | Calendar-attached reminders on entities |
| Permissions | Per-entity, per-role visibility |
| Entity Tags | Tag associations |
| Mentions | `[entity:id]` inline references → tooltips |
| Entity Image | Primary + header images |

**Campaign-level resources**: Members, Roles, Applications, Categories, Statuses (custom status taxonomy), Default Thumbnails, Styles (CSS), Dashboard Widgets, Gallery (image library)

### World Anvil (reconstructed from [feature pages](https://www.worldanvil.com/) and reviews)

**~28 article template types** (World Anvil's primary differentiator — structured templates with prompted fields):

| Template | Description |
|----------|-------------|
| Generic Article | Free-form |
| Character | Name, biography, traits, affiliations |
| Species | Biology, ecology, habitat, lifecycle |
| Organisation | Structure, goals, members, diplomacy |
| Location (Geographic) | Geography, climate, natural resources, flora/fauna |
| Settlement | Government, infrastructure, demographics, economy |
| Building / Landmark | Architecture, purpose, history |
| Vehicle | Type, propulsion, crew, cargo |
| Technology / Science | Principles, applications, limitations |
| Item | Properties, history, significance |
| Spell | Components, effects, limitations |
| Condition | Symptoms, causes, treatment, prognosis (diseases, mutations, curses) |
| Document | Content, authorship, context |
| Ethnicity | Culture, customs, territory, demographics |
| Language | Phonology, grammar, script, dialects |
| Material | Properties, sources, uses |
| Myth / Legend | Narrative, origin, cultural significance |
| Military Formation | Structure, equipment, tactics, history |
| Military Conflict | Belligerents, timeline, outcome, consequences |
| Rank / Title | Hierarchy, responsibilities, privileges |
| Physical / Metaphysical Law | Rules governing the world (physics, magic systems) |
| Plot | Story structure, acts, hooks, twists |
| Prose | Narrative text (short stories, chapters, poems) |
| Tradition / Ritual | Ceremony, participants, significance |
| Profession | Skills, tools, social status |
| Report (Session) | Events, outcomes, player notes |
| + Custom templates | User-defined article types |

**Unique World Anvil features** (beyond Kanka):

| Feature | Description | In scope? |
|---------|-------------|-----------|
| Family Trees | Interactive visual genealogy trees | **Yes** — genealogy extension already has the data; visualization is a frontend concern but the relationships + ancestry graph are backend |
| Diplomacy Webs | Visual graph of inter-faction relations | **Yes** — world_social extension already models this; visualization is frontend |
| Chronicles | Map + timeline fusion — scroll through events, map zooms to where each happened | **Yes** — backend is linking events to both a location and a timeline position; visualization is frontend |
| Manuscripts | Novel-writing software (chapters, scenes, word count) | **Yes** — this is a journal/document type with structured pages |
| Secrets / Spoilers | Inline content blocks visible only to certain roles | **Yes** — this is per-block ACL on rich-text content |
| Statblocks | RPG stat blocks embedded in articles (100+ system integrations) | **Yes** — rpg_traits provides the data; rendering is frontend |
| Whiteboards | Mind-mapping / brainstorming canvas | **No** — pure frontend/UI tool, no backend model needed |
| HeroForge integration | 3D character model embedding | **No** — third-party integration, not a data model concern |
| Custom CSS | Per-world theming | **No** — frontend concern |

---

## 2. What's In Scope vs Out of Scope

### In scope (this repo)

Everything needed to replace Kanka + World Anvil as a worldbuilding / campaign management backend:

- Identity & biography (persons, characters, creatures, species/races)
- Relationships & social (directed typed relations, factions, families, membership, disposition state machines, diplomacy)
- Spatial (locations, maps with layers/groups/markers, transit graphs, map authoring — stamp library, terrain regions, paths — at every scale from star maps to vehicle interiors)
- Inventory & economy (item catalog, instances, ownership, cross-entity inventory, trade)
- Narrative (events, timelines, chronicles, quests/hooks, journals/manuscripts, lore, posts, plots)
- Calendar & time (custom calendars, months, moons, seasons, eras, reminders)
- Dialogue & conversations (multi-participant, branching, bookmarks)
- Taxonomy & metadata (tags, races/species, creature types, statuses, categories, property kits, structured attributes)
- Media & assets (image/audio/file library, gallery, entity attachments)
- Scenes (playable areas shared by all consumers: background, grid, tokens, walls/doors, lights, sounds, tiles, drawings, notes, regions, fog, playlists)
- RPG mechanics baseline (game systems, campaigns, traits/stats, derivative math, dice/roll tables, combat tracker, cards)
- Event logging (encounter/combat/dialogue/interaction/transaction logs)
- Access control (per-entity, per-post, per-attribute, per-block visibility via ACL)
- AI character cards (SillyTavern V2/V3 spec for downstream AI framework)
- Lorebooks (World Info entries for downstream AI framework)

### Out of scope (downstream repos)

| Consumer | What lives there |
|----------|-----------------|
| **VTT** | Grid rendering, canvas/WebGL, real-time token drag, fog-of-war pixel reveal, dynamic lighting shader, scene UI (toolbar, layers panel), chat/dice UI |
| **AI framework** | Vector storage/RAG, summarisation, STscript automation, regex transforms, token counting, context template assembly, instruct mode runtime, sentiment classification for sprites, generation preset runtime, AI GM/player orchestration |
| **Video games** | Physics, rendering, spawn points, trigger zones, pathfinding, save state, achievements, crafting recipes, dialogue trees (branching player-choice UI), NPC routines/AI behavior, procedural generation |

---

## 3. Extension Hierarchy

**Tier 0** — generic, no worldbuilding dependency.
**Tier 1** — worldbuilding / fiction (the Kanka/World Anvil replacement layer).
**Tier 2** — TTRPG mechanics baseline (shared by all three downstream consumers).
**Tier 3** — event logging.
**Tier AI** — AI character/lorebook data models (consumed by the AI framework).

```
TIER 0 — Generic (framework built-ins, not forked)
├── acl_rbac          [framework]   Per-record VIEW/EDIT/DELETE/SHARE
├── fileio            [framework]   File upload/storage
├── metadata          [framework]   Free-form KV on any record
├── meta_labels       [framework]   Polymorphic label catalog
├── meta_logging      [framework]   Audit trail
├── webhooks          [framework]   Event push notifications

TIER 0 — Generic (this repo)
├── genealogy         [exists]      Person + directed labelled Relationship
├── calendar          [NEW]         Custom calendars, dates, eras, reminders
├── conversation      [NEW]         Multi-participant threaded dialogue,
│                                   branching, bookmarks
└── media             [NEW]         Asset library (image/audio/file),
                                    gallery, polymorphic entity attachment

TIER 1 — Worldbuilding (the Kanka/World Anvil replacement)
├── world_taxonomy     [NEW]        Hierarchical tags, races/species,
│                                   creature types, statuses, categories,
│                                   property kits (attribute templates),
│                                   controlled vocabularies
│   └── depends: meta_labels
├── world_spatial      [NEW]        Locations (hierarchy), maps (multi-layer,
│                                   markers, layers, groups, zoom/grid),
│                                   transit graph, map authoring (stamp
│                                   library, placed stamps, terrain regions
│                                   — Inkarnate-style map creation at every
│                                   scale from star map to vehicle interior)
│   └── depends: genealogy, media
├── world_narrative    [NEW]        Events, timelines, chronicles (event→
│                                   location+time fusion), quests/hooks (DAG),
│                                   journals/manuscripts (multi-page: text/
│                                   image/pdf/video), lore notes, entity posts
│                                   (pinnable, visibility-controlled),
│                                   plots (story structure), session reports
│   └── depends: calendar, world_spatial, genealogy
├── world_social       [NEW]        Factions/organisations/families (hierarchy),
│                                   membership (role/rank/status), faction
│                                   relations (diplomacy web), disposition
│                                   state machines, event-driven attitude
│                                   shifts
│   └── depends: genealogy, world_narrative
└── world_inventory    [NEW]        Item catalog, item instances, ownership
                                    (person + faction), spatial placement,
                                    equipment slots, containers, cross-entity
                                    inventory
    └── depends: genealogy, world_spatial

TIER 2 — TTRPG Mechanics (baseline for all consumers)
├── rpg_core           [refactor of rpg_state]
│                      Game systems, campaigns, character injection
│                      (kind/campaign_id/user_id onto Person),
│                      campaign membership semantics
│   └── depends: genealogy, world_spatial, world_social,
│                world_inventory, world_narrative
├── rpg_traits         [split from rpg_state]
│                      Trait catalog, DerivativeTrait math (6 ops),
│                      PersonTrait join, stacking/qualifier
│   └── depends: rpg_core, world_inventory
├── rpg_scene          [NEW]        Playable area / loaded level shared by
│                                   all 3 consumers. Scene config (background,
│                                   grid, fog, vision, environment); placed
│                                   tokens; walls/doors (per-sense blocking,
│                                   one-way, threshold); lights; ambient
│                                   sounds; tiles; drawings; notes; regions
│                                   with behaviors; measured templates;
│                                   per-user fog exploration; playlists
│   └── depends: rpg_core, world_spatial, media, rpg_traits
├── rpg_dice           [NEW]        Dice formulas, roll tables
│   └── depends: rpg_core
├── rpg_combat         [NEW]        Combat tracker, initiative, combatant
│                                   groups, rounds/turns
│   └── depends: rpg_core, rpg_traits
└── rpg_cards          [NEW]        Decks, cards, piles, draw/shuffle/deal
    └── depends: rpg_core, media

TIER 3 — Event Logging
└── rpg_log            [exists, expanded]
                       Encounter/combat/dialogue/interaction/transaction
                       logs, session logs
    └── depends: rpg_core, rpg_traits, rpg_combat

TIER AI — Character & Lorebook Data Models
├── ai_character       [NEW]        Character cards (V2/V3 spec), persona,
│                                   expression sprites, generation presets
│   └── depends: genealogy, conversation, media
└── ai_lorebook        [NEW]        World Info entries (full SillyTavern
                                    field surface), auto-gen from world_*
    └── depends: world_taxonomy, world_spatial, world_social,
                 world_narrative, world_inventory
```

---

## 4. Extension Model Details

### Phase 1 — Tier 0 Foundations

#### `genealogy` [exists — no changes]

Person + directed labelled Relationship graph. Family trees (World Anvil
feature) are a frontend visualization of the ancestry relationships already
modeled here.

#### `calendar` [NEW]

| Model | Key Fields |
|-------|------------|
| CalendarModel | name, description, year_length, epoch_label, leap_year_rule (JSON) |
| MonthModel | calendar_id FK, name, length, ordinal, is_intercalary |
| WeekdayModel | calendar_id FK, name, ordinal |
| SeasonModel | calendar_id FK, name, month_start, day_start, month_end, day_end, description |
| CelestialBodyModel | calendar_id FK, name, cycle_days, phase_offset, description |
| EraModel | calendar_id FK, name, start_year, end_year, description, abbreviation |
| CalendarDateModel | calendar_id FK, year, month_ordinal, day, notes |
| ReminderModel | calendar_date_id FK, target_entity_type + target_entity_id (polymorphic), message, is_recurring |

Covers: Kanka calendars/moons/seasons/epochs/intercalaries/weather/reminders.

#### `conversation` [NEW]

| Model | Key Fields |
|-------|------------|
| ConversationModel | name, type (ic_dialogue\|ooc\|ai_session), location_id (opt), campaign_id (opt) |
| ConversationParticipantModel | conversation_id FK, person_id FK, role (speaker\|observer\|ai_character\|user), joined_at, left_at |
| MessageModel | conversation_id FK, sender_person_id FK (null = system), parent_message_id (self-FK for branching), text, is_user, is_system, is_in_character, tone, occurred_at (in-world), sent_at (real), metadata (JSON) |
| MessageBookmarkModel | message_id FK, name, description |

Covers: Kanka conversations + messages, SillyTavern chat history / branching / bookmarks / group chats.

#### `media` [NEW]

| Model | Key Fields |
|-------|------------|
| AssetModel | name, file_path (or URL), mime_type, size_bytes, kind (image\|audio\|video\|document\|sprite), description, metadata (JSON) |
| AssetAttachmentModel | asset_id FK, target_entity_type + target_entity_id (polymorphic), role (primary_image\|header_image\|token_image\|map_image\|expression_sprite\|background\|sfx), ordinal |
| GalleryModel | name, description, campaign_id (opt) |
| GalleryEntryModel | gallery_id FK, asset_id FK, ordinal, caption |

Covers: Kanka entity images + header images + entity assets + gallery, World Anvil image/music/sound embedding.

### Phase 2 — Tier 1 Worldbuilding

#### `world_taxonomy` [NEW]

| Model | Key Fields |
|-------|------------|
| TaxonModel | name, parent_id (self-FK), kind (race\|creature_type\|culture\|language_family\|religion\|species\|ethnicity\|condition_type\|material_type), colour, icon, description, game_system_id (opt) |
| EntityTaxonModel | taxon_id FK, target_entity_type + target_entity_id (polymorphic) |
| StatusModel | name, colour, icon, description, kind (entity_status\|quest_status\|...) |
| PropertyKitModel | name, description |
| PropertyKitEntryModel | property_kit_id FK, key, default_value, value_type (text\|number\|checkbox\|section\|star_rating\|random), ordinal, is_private |

Covers: Kanka Races + Creatures + Tags + Statuses + Categories + Property Kits. World Anvil Species + Ethnicity + Language + Material + Condition template types (as taxon kinds rather than separate entity tables — the rich text lives in the entity's description/posts; the taxonomy provides the structured classification).

#### `world_spatial` [NEW]

| Model | Key Fields |
|-------|------------|
| LocationModel | name, description, parent_id (self-FK tree), kind (system\|planet\|moon\|continent\|region\|city\|district\|building\|facility\|room\|vessel\|underground_complex\|container\|equipment_slot\|body\|body_part\|organ), campaign_id (opt), associated_person_id (opt — equipment slots, body parts), container_item_instance_id (opt) |
| MapModel | location_id FK, name, kind (exterior\|interior\|area\|world), scale (stellar\|system\|planetary\|continental\|regional\|city\|building\|vehicle\|interior), level (int), elevation_bottom, elevation_top, image_asset_id FK (opt — null when map is vector-authored, set when using a flat image), width, height, grid, min_zoom, max_zoom, initial_zoom, center_x, center_y, center_marker_id, is_real |
| MapLayerModel | map_id FK, name, image_asset_id FK (opt), position, visibility, kind (terrain\|overlay\|background\|stamp\|annotation) |
| MapGroupModel | map_id FK, name, is_shown, position |
| MapPinModel | map_id FK, x, y, kind (journal\|item\|transit\|poi\|npc\|event), target_entity_type + target_entity_id (polymorphic), label, description, icon, via (for transit), colour, opacity, custom_icon, custom_shape, pin_size, is_draggable, circle_radius, group_id FK, visibility |
| **Map authoring (Inkarnate-style)** | |
| StampCategoryModel | name, parent_id (self-FK tree), scale_filter (JSON array — which map scales this category applies to, e.g. ["stellar","system"] for star/nebula stamps, ["regional","city"] for terrain/building stamps), icon, description |
| StampModel | name, category_id FK, default_width, default_height, kind (terrain_feature\|structure\|vegetation\|icon\|celestial\|decoration\|vehicle\|furniture), tags (JSON), scale_filter (JSON — inherits from category if null), cover_height (float — default cover height in grid units; null = no cover; inheritable by instances), cover_density (float 0-1 — default cover density; null = no cover), blocks_movement (bool — default false; scatter that blocks pathing) |
| StampVariantModel | stamp_id FK, name, asset_id FK (→ media), axis (state\|damage\|orientation\|season\|activation\|phase\|...), value (intact\|damaged\|ruined\|open\|closed\|locked\|lit\|unlit\|N\|NE\|E\|...\|spring\|summer\|...), is_default, sort_order |
| MapStampInstanceModel | map_id FK, layer_id FK, stamp_id FK, active_variants (JSON — {"state":"intact","orientation":"N"} — one value per axis; null axes use is_default variant), x, y, width, height, rotation, scale_x, scale_y, opacity, tint_color, is_flipped_x, is_flipped_y, sort_order, is_locked, target_entity_type + target_entity_id (opt polymorphic — links this stamp to a game object: a Person, Location, ItemInstance, etc.), is_interactable, cover_height (float — override stamp default; null = use stamp default), cover_density (float — override stamp default; null = use stamp default), blocks_movement (bool — override stamp default; null = use stamp default) |
| StampInteractionHookModel | stamp_instance_id FK, event (on_interact\|on_enter\|on_leave\|on_use\|on_open\|on_close\|on_lock\|on_unlock\|on_pickup\|on_destroy\|on_activate\|on_deactivate\|...), action_type (variant_change\|script\|navigate\|transfer_item\|spawn\|dialogue\|sound), action_config (JSON — payload per action_type), ordinal, is_enabled |
| TerrainRegionModel | map_id FK, layer_id FK, name, polygon_points (JSON — array of [x,y] vertices), biome (ocean\|coast\|grassland\|forest\|desert\|mountain\|tundra\|swamp\|void\|nebula\|urban\|hull\|deck\|...), texture_asset_id FK (opt), fill_color, fill_opacity, stroke_color, stroke_width, sort_order |
| MapPathModel | map_id FK, layer_id FK, name, points (JSON — array of [x,y] with optional curve control points), kind (road\|river\|border\|orbit\|trade_route\|wall_outline\|corridor), stroke_color, stroke_width, stroke_style (solid\|dashed\|dotted), fill_color (opt — for closed paths), sort_order |

**Stamp variant system** — a `StampModel` is not a single image. It has one or
more `StampVariantModel` rows, each on an **axis** (an independent dimension of
variation). The axes are free-form strings so any stamp can define its own.
Examples:

- A building stamp: axis `state` → intact / damaged / ruined; axis `activation` → lit / unlit
- A door stamp: axis `state` → open / closed / locked
- A star stamp: axis `phase` → main_sequence / red_giant / white_dwarf
- A tree stamp: axis `season` → spring / summer / autumn / winter / dead
- A ship stamp: axis `orientation` → N / NE / E / SE / S / SW / W / NW; axis `damage` → pristine / hull_breach / derelict

A `MapStampInstanceModel` selects the active value for each axis via
`active_variants` (a JSON map of axis→value). Axes not specified fall back to
the variant marked `is_default`. The frontend composites the selected variant
per axis into the rendered stamp (simple: pick the single variant that matches
all active axes; advanced: layer multiple axes if the art supports it).

At runtime (in a VTT scene or video game), changing a stamp instance's
`active_variants` changes its visual state — a building burns down, a door
opens, a torch lights. The game/VTT consumer just updates the JSON field.

**Interactable stamps** — a `MapStampInstanceModel` with `is_interactable=true`
is a game object, not just decoration. It connects to the rest of the system
in two ways:

1. **Entity link** (`target_entity_type + target_entity_id`) — ties the stamp
   to an existing game object. The stamp is the visual; the entity is the
   state. Examples:
   - A chest stamp → `LocationModel` (kind=container) — the location holds
     ItemInstances; opening the chest reveals its inventory.
   - An NPC stamp → `PersonModel` — clicking initiates dialogue, shows their
     character sheet, or triggers combat.
   - A vehicle stamp → `LocationModel` (kind=vessel) — boarding navigates to
     the vehicle's interior map.
   - A weapon on the ground → `ItemInstanceModel` — picking it up transfers
     ownership and moves it to the character's inventory location.
   - A lever/switch → no entity needed; just hooks.

2. **Interaction hooks** (`StampInteractionHookModel`) — event→action pairs
   that fire when something happens to the stamp. Each hook has:
   - `event` — what triggers it (on_interact, on_enter, on_use, on_open, etc.)
   - `action_type` — what happens:
     - `variant_change` — switch the stamp's visual state (door opens →
       active_variants.state = "open")
     - `script` — execute a consumer-defined script/macro (the script body
       lives in action_config; interpretation is consumer-specific)
     - `navigate` — transition to another map/scene (enter a building, board
       a vehicle, descend a stairway)
     - `transfer_item` — move an ItemInstance to/from the linked entity's
       inventory
     - `spawn` — place a new stamp instance or entity (a trap spawns
       enemies, a container spawns loot)
     - `dialogue` — start a Conversation with the linked Person
     - `sound` — play an audio asset
   - `action_config` (JSON) — parameters specific to the action_type
   - Multiple hooks per event are allowed (chained in ordinal order)

This replaces the need for a separate "actor on map" system. Foundry's Token
(actor placed on scene) and Kanka's Map Marker (entity pinned to map) are both
subsumed: a stamp instance with an entity link IS a token/marker, but it also
supports non-actor entities (items, locations, factions) and scripted
interactions that neither platform offers natively.

Covers: Kanka Locations + Maps + Markers + Layers + Groups. World Anvil
Geographic Location + Settlement + Building / Landmark templates (as location
kinds). dh-campaign location hierarchy + maps block + transit pins. Inkarnate /
Wonderdraft / Dungeondraft map authoring (stamp placement, terrain painting,
path drawing) at every scale from star charts to vehicle interiors.

**Scale semantics** — the `scale` field on MapModel controls:
- Which stamp categories are available (star/nebula stamps for stellar; trees/mountains for regional; furniture for interior)
- What grid units mean (light-years, AU, km, m, ft, squares)
- What biome/terrain options are relevant (void/nebula at stellar; ocean/forest at planetary; hull/deck at vehicle)

A map at `stellar` scale shows a galaxy/sector. Clicking a star drills down
to a `system` scale map (the star system). Clicking a planet drills down to
`planetary`. This is just the location hierarchy — each location at a given
level can have a map at the corresponding scale, and the map's pins link to
child locations that have their own maps.

Cycle guard: manager-layer hook rejects parent_id mutations that would close a cycle.

#### `world_narrative` [NEW]

| Model | Key Fields |
|-------|------------|
| EventModel | name, description, calendar_date_id FK (opt), location_id FK (opt), era_id FK (opt), kind (historical\|plot\|background\|military_conflict\|...), occurred_at (datetime fallback) |
| EventParticipantModel | event_id FK, person_id or faction_id (XOR), role |
| TimelineModel | name, description, campaign_id (opt) |
| TimelineEntryModel | timeline_id FK, event_id FK, ordinal, label |
| HookModel | name, description, campaign_id (opt), kind (major_quest\|side_quest\|objective\|plot_thread\|mystery\|rumor\|obligation\|foreshadowing\|hint\|background), giver_person_id, giver_faction_id |
| HookDependencyModel | parent_hook_id FK, child_hook_id FK, reason |
| PersonHookModel | person_id FK, hook_id FK, status, accepted_at, completed_at, progress |
| FactionHookModel | faction_id FK, hook_id FK, status, accepted_at, completed_at, progress |
| JournalModel | name, description, kind (session_report\|in_world_diary\|lore\|handout\|note\|manuscript\|prose\|chapter), campaign_id (opt), location_id (opt), author_person_id (opt), session_number, occurred_at |
| JournalPageModel | journal_id FK, ordinal, kind (text\|image\|pdf\|video), content, asset_id FK (opt) |
| EntityPostModel | target_entity_type + target_entity_id (polymorphic), name, content (rich text), position (pinned_top\|default), visibility (all\|admin\|self), ordinal |
| PlotModel | name, description, campaign_id (opt), kind (main\|subplot\|arc), parent_plot_id (self-FK for sub-plots) |
| PlotElementModel | plot_id FK, target_entity_type + target_entity_id (polymorphic — links to hooks, events, persons, factions, etc.), role (protagonist\|antagonist\|mcguffin\|setting\|complication), ordinal, notes |

Covers: Kanka Events + Timelines + Quests + Journals + Notes + Posts. World Anvil Plot + Prose + Myth + Military Conflict + Report templates (as event/journal/plot kinds). dh-campaign Hooks (DAG) + session logs.

Chronicles (World Anvil's map+timeline fusion) is not a separate model — it's the query "give me all TimelineEntries whose Events have a location_id, ordered by timeline position." The frontend renders the map-zoom-on-scroll behavior.

#### `world_social` [NEW]

| Model | Key Fields |
|-------|------------|
| FactionModel | name, description, parent_id (self-FK tree), campaign_id (opt), kind (political\|military\|religious\|criminal\|guild\|family\|...), location_id (opt — HQ) |
| @extension_model(RelationshipModel) | faction_id, target_faction_id (XOR with person endpoints) |
| DispositionModel | person_id FK, target_person_id or target_faction_id, attitude, is_default, trigger_event_id FK (opt → world_narrative.EventModel), notes |

Covers: Kanka Organisations + Families + Relations. World Anvil Organisation + Military Formation + Rank/Title + Diplomacy Webs. dh-campaign dispositions + event-driven attitude shifts + superiors.

Diplomacy web is the frontend visualization of Faction↔Faction relationships — the data is already in RelationshipModel with faction endpoints.

Cycle guard: manager-layer hook rejects parent_id cycles.

#### `world_inventory` [NEW]

| Model | Key Fields |
|-------|------------|
| ItemModel | name, description, weight, base_value, stack_size, kind (weapon\|armour\|consumable\|container\|currency\|document\|authority\|misc), game_system_id (opt) |
| ItemInstanceModel | item_id FK, location_id FK, owner_person_id, owner_faction_id, quantity, durability, notes |
| ItemPropertyModel | item_id FK, key, value, kind (mechanical\|descriptive) |
| EntityInventoryModel | target_entity_type + target_entity_id (polymorphic — any entity can hold items), item_instance_id FK, quantity |

Covers: Kanka Items + cross-entity Inventory. World Anvil Item + Technology templates (as item kinds with properties). dh-campaign item ownership semantics.

### Phase 3 — Tier 2 TTRPG Mechanics

#### `rpg_core` [refactor from rpg_state]

| Model | Key Fields |
|-------|------------|
| GameSystemModel | name, description |
| CampaignModel | name, description, game_system_id FK, user_id FK (GM) |
| @extension_model(PersonModel) | kind (pc\|npc\|monster\|creature\|vehicle\|construct), campaign_id, user_id, location_id |

#### `rpg_traits` [split from rpg_state]

| Model | Key Fields |
|-------|------------|
| TraitModel | name, description, kind (attribute\|skill\|spell\|talent\|feat\|ability\|language\|resource\|progression\|status_effect), game_system_id, campaign_id, default_duration_seconds |
| DerivativeTraitModel | source_trait_id, source_item_id, target_trait_id, operation (override\|additive\|multiplicative\|clamp\|downgrade\|upgrade), value, order_index, stacking_group, qualifier |
| PersonTraitModel | person_id FK, trait_id FK, value, rank, started_at, expires_at, source_person_id, source_item_instance_id, target_location_id, notes |

#### `rpg_scene` [NEW]

The playable area — shared by all three consumers. A VTT renders it as a
battlemap canvas. A video game renders it as a loaded level. The AI framework
uses it to know what's in the room, who can see what, and what's interactable.

| Model | Key Fields |
|-------|------------|
| SceneModel | name, map_id FK (→ world_spatial.MapModel), campaign_id FK, width, height, padding, background_color, background_image_asset_id FK, foreground_image_asset_id FK, foreground_elevation, grid_type (gridless\|square\|hex_col_odd\|hex_col_even\|hex_row_odd\|hex_row_even), grid_size, grid_color, grid_opacity, grid_distance, grid_units, token_vision, fog_exploration, fog_explored_color, fog_unexplored_color, global_illumination, darkness_level, global_illumination_threshold, weather_effect, environment_data (JSON), initial_x, initial_y, initial_scale, transition_type, transition_duration, is_active, nav_name, nav_order, playlist_id FK, journal_id FK |
| SceneTokenModel | scene_id FK, person_id FK (the actor), is_actor_linked, actor_delta (JSON overrides for unlinked), name, x, y, width, height, rotation, elevation, texture_asset_id FK, tint_color, disposition (friendly\|neutral\|hostile\|secret), sight_range, sight_angle, sight_mode, light_dim, light_bright, light_angle, light_color, light_animation, bar1_trait_id, bar1_value, bar1_max, bar2_trait_id, bar2_value, bar2_max, is_hidden, is_defeated, lock_rotation, status_markers (JSON) |
| SceneRoomModel | scene_id FK, name, parent_room_id (self-FK — room-in-room nesting), polygon_points (JSON — boundary vertices), floor_texture_asset_id FK (opt), floor_color, floor_opacity, wall_texture_asset_id FK (opt — default texture for this room's boundary walls), wall_color, ceiling_height, elevation, ambient_light_color, ambient_light_intensity, is_hidden, location_id FK (opt — links room to a Location entity for inventory/narrative), sort_order |
| SceneWallModel | scene_id FK, room_id FK (opt — which room owns this wall segment), points (JSON — array of {x,y} supporting line segments AND Bézier curves), door_type (none\|door\|secret\|window\|gate\|portcullis), door_state (closed\|open\|locked\|barred\|broken), move_restriction (none\|normal\|limited), sight_restriction, sound_restriction, light_restriction, direction (both\|left\|right), threshold_distance, threshold_attenuation, texture_left_asset_id FK (opt — texture on the left side of the wall), texture_right_asset_id FK (opt — texture on the right side), texture_left_color, texture_right_color, cover_height (float — height in grid units; null = full room height; 0 = no cover; 0.5 = waist-high wall; etc.), cover_density (float 0-1 — 0=no cover, 0.5=half/light, 0.75=three-quarter/heavy, 1.0=full/solid; iron bars ~0.5, arrow slit ~0.75, stone wall 1.0) |
| SceneLightModel | scene_id FK, room_id FK (opt), x, y, dim_radius, bright_radius, angle, color, intensity, animation_type, animation_speed, animation_intensity, attenuation, luminosity, is_darkness_source, is_constrained_by_walls, is_hidden, coloration_type |
| SceneSoundModel | scene_id FK, room_id FK (opt), x, y, radius, asset_id FK, volume, is_repeat, easing, is_constrained_by_walls, is_hidden |
| SceneTileModel | scene_id FK, room_id FK (opt), x, y, width, height, elevation, rotation, texture_asset_id FK, scale_x, scale_y, tint_color, alpha, is_overhead, is_roof, is_hidden, occlusion_mode, sort_order |
| SceneDrawingModel | scene_id FK, shape_type (rectangle\|ellipse\|polygon\|freehand), x, y, points (JSON), width, height, stroke_width, stroke_color, fill_type, fill_color, text, font_family, font_size, is_hidden, sort_order |
| SceneNoteModel | scene_id FK, x, y, icon_asset_id FK, icon_size, icon_tint, target_entity_type + target_entity_id (polymorphic), label, font_size, text_anchor, text_color |
| SceneRegionModel | scene_id FK, name, color, shapes (JSON), elevation_bottom, elevation_top |
| SceneRegionBehaviorModel | region_id FK, behavior_type (teleport\|adjust_darkness\|execute_script\|pause_game), config (JSON), is_disabled |
| SceneMeasuredTemplateModel | scene_id FK, x, y, shape (circle\|cone\|ray\|rect), distance, direction, angle, width, texture_asset_id FK, border_color, fill_color |
| FogExplorationModel | scene_id FK, user_id FK, explored_data (JSON/binary) |
| PlaylistModel | name, description, campaign_id FK, mode (sequential\|shuffle\|simultaneous), is_playing, fade_duration |
| PlaylistSoundModel | playlist_id FK, asset_id FK, name, volume, is_repeat, fade_duration, sort_order |

**Room system** — scenes are authored room-first (like Dungeondraft), not
wall-first. A `SceneRoomModel` defines a bounded polygon with floor
texture/color, wall texture/color defaults, and ambient lighting. Walls are
generated from room boundaries — when two rooms share a boundary, the shared
wall segment exists once with independent textures per side
(`texture_left_asset_id` / `texture_right_asset_id`). This handles:

- **Room-in-room nesting** (`parent_room_id` self-FK) — a jail cell inside a
  guardhouse. The cell's boundary walls that coincide with the guardhouse walls
  are shared segments; only the cell's inner walls (the bars) have a different
  texture. The parent room's floor shows through in the gap between rooms, or
  the child overrides it.
- **Door states** — `door_type` covers: none, door, secret, window, gate,
  portcullis. `door_state` covers: closed, open, locked, barred, broken. A
  broken door permanently ceases to block movement/sight.
- **Per-side wall textures** — a corridor wall is stone on the corridor side
  and bars on the cell side. Each wall segment carries two texture slots (left
  and right, determined by the wall's direction/facing).
- **Room → Location link** — a room can optionally link to a `LocationModel`
  entity, connecting it to the worldbuilding layer (its inventory, narrative
  posts, transit graph). A chest stamp inside the room links to the same
  Location as a container.
- **Lights/sounds/tiles belonging to a room** — when a room is hidden (fog of
  war, unexplored), its owned lights/sounds/tiles are also hidden. The optional
  `room_id` FK on these models enables this grouping.

Wall `points` are stored as a JSON array of `{x, y}` coordinates rather than
`x1,y1,x2,y2` — this supports multi-segment walls, Bézier curves (UVTT v2
compatibility), and curved walls in a single field.

**Cover system** — walls and stamps carry two system-agnostic physical
properties that enable auto-calculation of cover across any rule system:

- `cover_height` (float, grid units) — how tall the object is. `null` on a
  wall = full room/ceiling height (total cover from that wall). `0` = flush
  with the floor (no cover). `0.5` on a 5ft grid = 2.5 ft, waist-high.
  Combined with token elevation and height, the consumer draws a line from
  attacker head/weapon to target center — if a cover object interposes AND its
  height exceeds the line's elevation at the intersection point, it provides
  cover.
- `cover_density` (float, 0–1) — how opaque/solid the cover is. `1.0` = solid
  stone, full cover. `0.75` = arrow slit, portcullis, heavy cover.
  `0.5` = iron bars, wooden fence, half/light cover. `0` = decorative only.

The game system rules layer maps these raw values to system-specific
categories:
- **D&D 5e:** density ≤0.5 → half cover (+2 AC); ≤0.75 → three-quarters
  (+5 AC); 1.0 → full cover (untargetable).
- **WH40K / DH2e:** density ≤0.5 → light cover (AP bonus); ≤0.75 → heavy
  cover; 1.0 → full cover.
- **Video game:** density maps directly to damage reduction percentage.

Stamps define defaults on `StampModel` (a barrel template is always 0.6 height,
0.7 density). Instances can override per-placement (this particular barrel is
shot up → density drops to 0.3). Variant state changes can also affect cover —
a door stamp with variant axis `state=broken` could carry a hook that sets
cover_density to 0.2.

Walls on rooms inherit `cover_height=null` (full height) and
`cover_density=1.0` (solid) by default — a full wall is full cover. A low wall
(half-height garden wall, barricade) is authored with explicit values.

#### `rpg_dice` [NEW]

| Model | Key Fields |
|-------|------------|
| DiceFormulaModel | name, formula, description, game_system_id (opt) |
| RollTableModel | name, description, formula, game_system_id (opt) |
| RollTableEntryModel | roll_table_id FK, range_low, range_high, result_text, result_entity_type + result_entity_id (opt), weight |

#### `rpg_combat` [NEW]

| Model | Key Fields |
|-------|------------|
| EncounterModel | campaign_id FK, location_id FK (opt), name, round_number, status, current_turn_person_id |
| CombatantModel | encounter_id FK, person_id FK, initiative, side, is_defeated, disposition, is_hidden |
| CombatantGroupModel | encounter_id FK, name |
| CombatantGroupMemberModel | group_id FK, combatant_id FK |

#### `rpg_cards` [NEW]

| Model | Key Fields |
|-------|------------|
| DeckModel | name, description, kind, campaign_id (opt), is_infinite, card_width, card_height |
| CardModel | deck_id FK, name, face_asset_id FK, back_asset_id FK, suit, value, description, sort_order |
| CardPileModel | name, kind (hand\|draw\|discard\|play_area), owner_person_id (opt), deck_id FK |
| CardPileEntryModel | card_pile_id FK, card_id FK, ordinal, is_face_up |

### Phase 3 — Tier 3 Logging

#### `rpg_log` [exists — expanded]

No model changes. Gains references to `rpg_combat.EncounterModel`.

### Phase 4 — Tier AI

#### `ai_character` [NEW]

| Model | Key Fields |
|-------|------------|
| CharacterCardModel | person_id FK, description, personality, first_message, alternate_greetings (JSON array), example_messages, scenario, system_prompt, post_history_instructions, creator_notes, creator, character_version, extensions (JSON) |
| PersonaModel | user_id FK, name, description, avatar_asset_id FK |
| ExpressionSpriteModel | person_id FK, expression (happy\|sad\|angry\|neutral\|...), asset_id FK |
| GenerationPresetModel | name, backend, temperature, top_p, top_k, max_tokens, repetition_penalty, settings (JSON) |

#### `ai_lorebook` [NEW]

| Model | Key Fields |
|-------|------------|
| LorebookModel | name, description, campaign_id (opt), scan_depth, token_budget, recursive_scanning |
| LorebookEntryModel | lorebook_id FK, keys (JSON array), secondary_keys (JSON array), content, name, comment, enabled, insertion_order, priority, position, depth, depth_role, probability, selective, selective_logic, constant, inclusion_group, group_weight, prioritize_inclusion, use_group_scoring, sticky_duration, cooldown_duration, delay_duration, character_filter (JSON), trigger_types (JSON), outlet_name, automation_id, recursion_level, prevent_recursion, delay_until_recursion, matching_sources (JSON), source_entity_type + source_entity_id (opt — auto-generated from world_*) |

---

## 5. Build Order

```
Phase 1 — Foundations (parallel, no inter-deps)
  genealogy           [exists]
  calendar            [new]
  conversation        [new]
  media               [new]

Phase 2 — Worldbuilding (depends on Phase 1)
  world_taxonomy      [new]
  world_spatial       [new]
  world_inventory     [new; depends: world_spatial]
  world_narrative     [new; depends: calendar, world_spatial]
  world_social        [new; depends: world_narrative]

Phase 3 — RPG + AI (depends on Phase 2)
  rpg_core            [refactor]
  rpg_traits          [split]
  rpg_scene           [new; depends: rpg_core, world_spatial, media, rpg_traits]
  rpg_dice            [new]
  rpg_combat          [new]
  rpg_cards           [new]
  rpg_log             [exists]
  ai_character        [new]
  ai_lorebook         [new]
```

---

## 6. The rpg_state Decomposition

| Current rpg_state model | Moves to |
|-------------------------|----------|
| GameSystemModel | rpg_core |
| CampaignModel | rpg_core |
| RPG_PersonModel (injection) | rpg_core |
| RPG_RelationshipModel (injection) | world_social |
| TraitModel | rpg_traits |
| DerivativeTraitModel | rpg_traits |
| PersonTraitModel | rpg_traits |
| FactionModel | world_social |
| LocationModel | world_spatial |
| ItemModel | world_inventory |
| ItemInstanceModel | world_inventory |
| HookModel | world_narrative |
| HookDependencyModel | world_narrative |
| PersonHookModel | world_narrative |
| FactionHookModel | world_narrative |
| Cycle guards | Move with their models |

Clean break — no compatibility shim. Dev uses `create_all`, no Alembic migrations to preserve.

---

## 7. Cross-Cutting Concerns

**Polymorphic entity references:** `target_entity_type + target_entity_id` pattern (framework's `metadata` already uses this).

**Visibility / ACL:** All extensions delegate to `acl_rbac`. No `is_private` columns on models. Kanka's `is_private`, `is_attributes_private`, per-post visibility, per-marker visibility, and World Anvil's secrets/spoiler blocks all map to ACL rules.

**Campaign scoping:** Optional `campaign_id` FK. NULL = shared/global template.

**Extension widening:** `rpg_core` → PersonModel, `world_social` → RelationshipModel.

**Import/export adapters** live in separate consumer scripts, not in extensions.
Target formats:
- **Kanka API** — entity CRUD + relations + attributes + maps + posts
- **Foundry VTT** — Actor/Item/JournalEntry/Scene/RollTable/Combat/Cards JSON
- **Roll20** — Character JSON + handout HTML + page config
- **SillyTavern** — Character card JSON (V2/V3 spec) + lorebook JSON
- **GEDCOM** — genealogy extension
- **Universal VTT (UVTT v1/v2)** — scene import/export. Our `rpg_scene` models
  map directly to the UVTT format: `SceneWallModel` → `line_of_sight` +
  `objects_line_of_sight`, `SceneWallModel` (door_type != none) → `portals`,
  `SceneLightModel` → `lights`, scene grid/dimensions → `resolution`,
  background image → `image`, darkness/illumination → `environment`. UVTT v2
  adds SVG Bézier curves for walls (our wall coords already support this as
  point arrays), directional line-of-sight (our `direction` field), multi-level
  with height-blocking (our `elevation_bottom/top`), and encrypted asset
  delivery. Export from `world_spatial` map authoring (stamps/terrain/paths)
  renders to the flat UVTT image + wall/portal/light overlay.

---

## 8. World Anvil Template Coverage

World Anvil's ~28 article templates map to our model as entity `kind` values or
taxon types — not as separate tables. The rich prose lives in the entity's
description or in EntityPosts; the structured classification lives in
`world_taxonomy.TaxonModel`.

| WA Template | Our Model | kind / taxon |
|-------------|-----------|-------------|
| Character | PersonModel | kind via rpg_core injection |
| Species | TaxonModel | kind='species' |
| Ethnicity | TaxonModel | kind='ethnicity' |
| Language | TaxonModel | kind='language' |
| Material | TaxonModel | kind='material' |
| Condition | TaxonModel | kind='condition' |
| Race | TaxonModel | kind='race' |
| Organisation | FactionModel | kind value |
| Military Formation | FactionModel | kind='military' |
| Rank / Title | (metadata on FactionMembership or PersonTrait) | |
| Location (Geographic) | LocationModel | kind='region' etc. |
| Settlement | LocationModel | kind='city'/'settlement' |
| Building / Landmark | LocationModel | kind='building' |
| Vehicle | LocationModel + rpg_core Person injection | kind='vehicle' (dual-nature) |
| Item | ItemModel | kind value |
| Technology / Science | ItemModel or TaxonModel | kind='technology' |
| Spell | TraitModel | kind='spell' |
| Event | EventModel | kind value |
| Military Conflict | EventModel | kind='military_conflict' |
| Myth / Legend | JournalModel | kind='myth' |
| Prose | JournalModel | kind='prose' |
| Document | JournalModel | kind='document' |
| Report (Session) | JournalModel | kind='session_report' |
| Plot | PlotModel | kind value |
| Tradition / Ritual | (EventModel or JournalModel) | kind='tradition' |
| Profession | TaxonModel | kind='profession' |
| Physical / Metaphysical Law | JournalModel or TaxonModel | kind='law' |
| Generic Article | JournalModel | kind='note' |
| Custom Template | PropertyKitModel + any entity | (attribute templates) |
