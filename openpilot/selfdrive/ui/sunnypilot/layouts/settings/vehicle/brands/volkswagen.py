"""
Copyright (c) 2021-, Haibin Wen, sunnypilot, and a number of other contributors.

This file is part of sunnypilot and is licensed under the MIT License.
See the LICENSE.md file in the root directory for more details.
"""
from openpilot.selfdrive.ui.sunnypilot.layouts.settings.vehicle.brands.base import BrandSettings
from openpilot.selfdrive.ui.ui_state import ui_state
from openpilot.system.ui.lib.application import gui_app
from openpilot.system.ui.lib.multilang import tr, tr_noop
from openpilot.system.ui.widgets import DialogResult
from openpilot.system.ui.widgets.confirm_dialog import ConfirmDialog
from openpilot.system.ui.sunnypilot.widgets.list_view import toggle_item_sp


DESCRIPTIONS = {
  'cc_only': tr_noop(
    'For Volkswagen vehicles with cruise control only (no ACC). Uses factory cruise control for speed; '
    'openpilot handles steering only.'
  ),
}


class VolkswagenSettings(BrandSettings):
  def __init__(self):
    super().__init__()

    self.cc_only = toggle_item_sp(
      lambda: tr("Cruise Control Only (No ACC)"),
      description=lambda: tr(DESCRIPTIONS["cc_only"]),
      initial_state=ui_state.params.get_bool("VwCCOnly"),
      callback=self._on_toggle_cc_only,
      enabled=lambda: not ui_state.engaged,
    )

    self.items = [
      self.cc_only,
    ]

  def _on_toggle_cc_only(self, state: bool):
    def confirm_callback(result: int):
      if result == DialogResult.CONFIRM:
        ui_state.params.put_bool("VwCCOnly", state)
        ui_state.params.put_bool("OnroadCycleRequested", True)
      else:
        self.cc_only.action_item.set_state(not state)

    content = (f"<h1>{self.cc_only.title}</h1><br>" +
               f"<p>{self.cc_only.description}</p>")

    dlg = ConfirmDialog(content, tr("Enable" if state else "Disable"), rich=True, callback=confirm_callback)
    gui_app.push_widget(dlg)
