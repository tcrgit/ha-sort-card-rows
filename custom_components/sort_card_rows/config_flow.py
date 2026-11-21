"""Config flow for Sort Card Rows integration."""
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback
from homeassistant.data_entry_flow import section
from homeassistant.helpers import selector

DOMAIN = "sort_card_rows"

CONF_PINNED_ENTITIES = "pinned_entities"
CONF_NO_HEADER_TOGGLE_AREAS = "no_header_toggle_areas"
CONF_DEVICE_CLASS_ORDER = "device_class_order"
CONF_KEYWORD_ORDER = "keyword_order"
CONF_AUTO_DASHBOARDS_ONLY = "auto_dashboards_only"
SECTION_SORT_OPTIONS = "sort_options"
SECTION_CARD_HEADERS = "card_header_options"

DEFAULT_DEVICE_CLASSES = (
    "temperature, humidity, illuminance, pressure, atmospheric_pressure, "
    "radon, carbon_dioxide, battery"
)


class SortEntitiesConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Sort Card Rows."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title="Sort Card Rows", data={})

        return self.async_show_form(step_id="user")

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry):
        """Return the options flow handler."""
        return SortEntitiesOptionsFlow()


class SortEntitiesOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for Sort Card Rows."""

    async def async_step_init(self, user_input=None):
        """Manage sorting options."""
        if user_input is not None:
            sort_sec = user_input.pop(SECTION_SORT_OPTIONS, {})
            header_sec = user_input.pop(SECTION_CARD_HEADERS, {})
            flattened = {
                CONF_PINNED_ENTITIES: sort_sec.get(CONF_PINNED_ENTITIES, []),
                CONF_DEVICE_CLASS_ORDER: sort_sec.get(
                    CONF_DEVICE_CLASS_ORDER, DEFAULT_DEVICE_CLASSES
                ),
                CONF_KEYWORD_ORDER: sort_sec.get(CONF_KEYWORD_ORDER, ""),
                CONF_AUTO_DASHBOARDS_ONLY: sort_sec.get(
                    CONF_AUTO_DASHBOARDS_ONLY, False
                ),
                CONF_NO_HEADER_TOGGLE_AREAS: header_sec.get(
                    CONF_NO_HEADER_TOGGLE_AREAS, []
                ),
            }
            return self.async_create_entry(title="", data=flattened)

        opts = self.config_entry.options

        schema = vol.Schema(
            {
                vol.Required(SECTION_SORT_OPTIONS): section(
                    vol.Schema(
                        {
                            vol.Optional(
                                CONF_PINNED_ENTITIES,
                                default=opts.get(CONF_PINNED_ENTITIES, []),
                            ): selector.EntitySelector(
                                selector.EntitySelectorConfig(multiple=True)
                            ),
                            vol.Optional(
                                CONF_DEVICE_CLASS_ORDER,
                                default=opts.get(
                                    CONF_DEVICE_CLASS_ORDER, DEFAULT_DEVICE_CLASSES
                                ),
                            ): selector.TextSelector(selector.TextSelectorConfig()),
                            vol.Optional(
                                CONF_KEYWORD_ORDER,
                                default=opts.get(CONF_KEYWORD_ORDER, ""),
                            ): selector.TextSelector(selector.TextSelectorConfig()),
                            vol.Required(
                                CONF_AUTO_DASHBOARDS_ONLY,
                                default=opts.get(CONF_AUTO_DASHBOARDS_ONLY, False),
                            ): selector.BooleanSelector(),
                        }
                    ),
                    {"collapsed": False},
                ),
                vol.Required(SECTION_CARD_HEADERS): section(
                    vol.Schema(
                        {
                            vol.Optional(
                                CONF_NO_HEADER_TOGGLE_AREAS,
                                default=opts.get(CONF_NO_HEADER_TOGGLE_AREAS, []),
                            ): selector.AreaSelector(
                                selector.AreaSelectorConfig(multiple=True)
                            ),
                        }
                    ),
                    {"collapsed": False},
                ),
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
