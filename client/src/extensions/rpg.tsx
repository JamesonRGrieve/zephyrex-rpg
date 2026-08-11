// SPDX-License-Identifier: AGPL-3.0-or-later
'use client';

import type { ZephyrexClientExtension } from 'zephyrex';

function RPGDashboard() {
  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">RPG Campaign Dashboard</h1>
      <p>Genealogy, state tracking, and session logging for your RPG campaigns.</p>
    </div>
  );
}

function RPGSettings() {
  return (
    <div className="p-4">
      <h2 className="text-lg font-semibold mb-2">RPG Settings</h2>
      <p>Configure your campaign extensions.</p>
    </div>
  );
}

export const rpgExtension: ZephyrexClientExtension = {
  name: 'rpg',
  displayName: 'RPG Campaign',
  description: 'Genealogy, state tracking, and session logging',
  serverExtension: 'rpg_state',
  pages: [
    {
      path: 'rpg',
      component: RPGDashboard,
    },
  ],
  navItems: [
    {
      title: 'RPG Campaign',
      url: '/rpg',
    },
  ],
  settingsPanel: RPGSettings,
};
