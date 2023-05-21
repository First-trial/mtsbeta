from .context import InteractionCtx
from discord.state import ConnectionState


class State(ConnectionState):
  def parse_interaction_create(self, data):
    interaction = InteractionCtx(
      data=data,
      state=self
    )
    if data['type'] in (2, 4) and self._command_tree:
      self._command_tree._from_interaction(
        interaction
      )
    elif data['type'] == 3:
      inner_data = data['data']
      custom_id = inner_data['custom_id']
      component_type = inner_data['component_type']
      self._view_store.dispatch_view(
        component_type,
        custom_id,
        interaction
      )
    elif data['type'] == 5:
      inner_data = data['data']
      custom_id = inner_data['custom_id']
      components = inner_data['components']
      self._view_store.dispatch_modal(
        custom_id,
        interaction,
        components
      )
    self.dispatch('interaction', interaction)

