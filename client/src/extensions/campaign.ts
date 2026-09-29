// SPDX-License-Identifier: AGPL-3.0-or-later
// Client counterparts of this project's server extensions (server/extensions/*),
// kept name-for-name so each maps 1:1 to its server extension.
import { createExtension } from 'zephyrex/extensions';

export const genealogyExtension = createExtension('genealogy');
export const rpgLogExtension = createExtension('rpg_log');
export const rpgStateExtension = createExtension('rpg_state');
