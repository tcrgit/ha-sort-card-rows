"""Sort Card Rows Frontend Integration."""
from pathlib import Path
import re

from homeassistant.components.frontend import add_extra_js_url
from homeassistant.components.http import HomeAssistantView, StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv, label_registry as lr
from homeassistant.helpers.typing import ConfigType

from .config_flow import (
    CONF_AUTO_DASHBOARDS_ONLY,
    CONF_DEVICE_CLASS_ORDER,
    CONF_KEYWORD_ORDER,
    CONF_NO_HEADER_TOGGLE_AREAS,
    CONF_PINNED_ENTITIES,
    DEFAULT_DEVICE_CLASSES,
    DOMAIN,
)

URL_BASE = "/sort_card_rows"
JS_FILENAME = "sort-card-rows.js"
CONF_LABELS_SEEDED = "labels_seeded"

STARTER_LABELS = [
    ("sort-0", "mdi:numeric-0-box-outline", "Sort priority 0 (intended for temporary use above sort-1)"),
    ("sort-1", "mdi:numeric-1-box-outline", "Sort priority 1 (top group/item)"),
    ("sort-2", "mdi:numeric-2-box-outline", "Sort priority 2"),
    ("sort-3", "mdi:numeric-3-box-outline", "Sort priority 3"),
    ("sort-4", "mdi:numeric-4-box-outline", "Sort priority 4"),
    ("sort-5", "mdi:numeric-5-box-outline", "Sort priority 5"),
    ("sort-6", "mdi:numeric-6-box-outline", "Sort priority 6"),
    ("sort-7", "mdi:numeric-7-box-outline", "Sort priority 7"),
    ("sort-8", "mdi:numeric-8-box-outline", "Sort priority 8"),
    ("sort-9", "mdi:numeric-9-box-outline", "Sort priority 9"),
    ("sort-top", "mdi:arrow-up-bold-box-outline", "Sort to top of card (above even sort-0)"),
    ("sort-bottom", "mdi:arrow-down-bold-box-outline", "Sort to bottom of card (same as sort-999)"),
]

CONFIG_SCHEMA = cv.empty_config_schema(DOMAIN)


def _normalize_token(value: str) -> str:
    """Normalize label names/IDs while keeping decimal points."""
    return re.sub(r"[^a-z0-9.]", "", value.lower())


def _async_seed_labels(hass: HomeAssistant) -> None:
    """Pre-create starter sort-* labels if not already present."""
    registry = lr.async_get(hass)
    existing = set()
    for entry in registry.labels.values():
        existing.add(_normalize_token(entry.label_id))
        existing.add(_normalize_token(entry.name))

    for name, icon, desc in STARTER_LABELS:
        if _normalize_token(name) not in existing:
            try:
                registry.async_create(name, icon=icon, description=desc)
            except ValueError:
                pass


def _build_settings_payload(options: dict) -> dict:
    """Convert raw options into clean JSON for the frontend."""
    raw_classes = options.get(CONF_DEVICE_CLASS_ORDER, DEFAULT_DEVICE_CLASSES)
    raw_keywords = options.get(CONF_KEYWORD_ORDER, "")

    device_classes = [
        c.strip().lower().replace(" ", "_")
        for c in raw_classes.split(",")
        if c.strip()
    ]
    keywords = [k.strip().lower() for k in raw_keywords.split(",") if k.strip()]

    return {
        "pinned_entities": options.get(CONF_PINNED_ENTITIES, []),
        "no_header_toggle_areas": options.get(CONF_NO_HEADER_TOGGLE_AREAS, []),
        "device_class_order": device_classes,
        "keyword_order": keywords,
        "auto_dashboards_only": options.get(CONF_AUTO_DASHBOARDS_ONLY, True),
    }

class SortEntitiesSettingsView(HomeAssistantView):
    """Serve current sorting options to the frontend."""

    url = f"{URL_BASE}/settings.json"
    name = "sort_card_rows:settings"
    requires_auth = False

    def __init__(self, hass: HomeAssistant) -> None:
        """Initialize the settings view."""
        self.hass = hass

    async def get(self, request):
        """Return active options as JSON."""
        payload = self.hass.data.get(
            f"{DOMAIN}_settings", _build_settings_payload({})
        )
        return self.json(payload)


async def _register_frontend(hass: HomeAssistant) -> None:
    """Register the static JS path, settings view, and extra JS URL."""
    if hass.data.get(DOMAIN):
        return

    js_path = Path(__file__).parent / JS_FILENAME

    await hass.http.async_register_static_paths(
        [
            StaticPathConfig(
                url_path=f"{URL_BASE}/{JS_FILENAME}",
                path=str(js_path),
                cache_headers=False,
            )
        ]
    )

    hass.http.register_view(SortEntitiesSettingsView(hass))
    add_extra_js_url(hass, f"{URL_BASE}/{JS_FILENAME}")
    hass.data[DOMAIN] = True


async def _async_update_options(hass: HomeAssistant, entry: ConfigEntry) -> None:
    """Refresh cached settings when updated in the UI."""
    hass.data[f"{DOMAIN}_settings"] = _build_settings_payload(dict(entry.options))


async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool:
    """Set up via configuration.yaml."""
    if DOMAIN in config:
        hass.data.setdefault(f"{DOMAIN}_settings", _build_settings_payload({}))
        _async_seed_labels(hass)
        await _register_frontend(hass)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up from a UI config entry."""
    hass.data[f"{DOMAIN}_settings"] = _build_settings_payload(dict(entry.options))

    if not entry.data.get(CONF_LABELS_SEEDED):
        _async_seed_labels(hass)
        hass.config_entries.async_update_entry(
            entry, data={**entry.data, CONF_LABELS_SEEDED: True}
        )

    await _register_frontend(hass)
    entry.async_on_unload(entry.add_update_listener(_async_update_options))
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return True

