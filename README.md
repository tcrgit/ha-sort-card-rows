# Sort Card Rows

A Home Assistant frontend plugin that lets you control the order of the rows inside dashboard cards—including auto-generated Overview, Area, and strategy dashboards—without renaming entities to alphabetize them, or converting cards and dashboards to manual YAML code.

Enables the user **to put the important controls and information first**.

## Features & Sorting Priority

Rows inside supported cards are ordered using a 5-tier priority chain:
1. **Pinned Entities (Drag-and-Drop):** Entities selected under **Pinned entities** in the integration's **Configure** dialog sort to the top of their card. This tool supports drag-and-drop ordering.
2. **Device & Entity sort-x Labels:** Assign native Home Assistant labels (`sort-1` through `sort-9`, `sort-top`, `sort-bottom`, a `sort-0` label to temporarily push a row to the top, or even use custom decimal labels like `sort-1.5`):
	* **Card Row Ordering:** Attach `sort-1`, `sort-2`, or `sort-bottom` directly to individual switch sensor entities to pin them to the top or bottom of a card.
	* **Multi-Device Grouping:** Attach a `sort-x` label to a Device (including *parent* devices with multiple post-`2026.11.0` *child* devices) to keep all of its entities grouped together as a block, and attach more `sort-x` labels to its Entities to order rows within that device group.
3. **Device Class Grouping:** Unranked rows group automatically by device_class using your configured priority list (defaults to temperature, humidity, illuminance, pressure, atmospheric_pressure, radon, carbon_dioxide, battery; but the user can edit the order and add more). For sensors without a device_class, apply a label like `sort-temperature` or `sort-pressure` to make that sensor sort like others that do have a device class.
4. **Priority Keywords:** Optional comma-separated keywords (for example, `Outdoor`, `Indoor`) allows you to sort rows by keywords found in the switch or sensor entity name, just ahead of the default alphabetization order. For example, you could set your dashboard to display the `Outdoor Temperature` before the `Indoor Temperature` automatically, without assigning labels to the entities.
5. **Alphabetical Tie-Breaker:** Any remaining ties sort alphabetically by the switch or sensor entity name.

### Bonus: Card Header Toggle Hiding

* Suppress the card title toggle switch in the header of multi-switch/light cards by selecting Areas under **Hide card headers for these areas** in **Configure**.

## Installation

1. **Marketplace / HACS (Recommended):**
	* Open **Settings > Marketplace (or HACS)**, click the three dots (...) in the top-right corner > **Custom repositories**, and add `https://github.com/tcrgit/ha-sort-card-rows` as an **Integration**.
	* Install **Sort Card Rows**, click Setup (or **Restart Home Assistant** and add it under **Settings > Devices & Services > + Add Integration**), and hard-refresh your browser (`Ctrl + Shift + R` or `Cmd + Shift + R`).
2. **Manual:**
	* Copy custom_components/sort_card_rows into /config/custom_components/, **Restart Home Assistant**, and add **Sort Card Rows** via **Settings > Devices & Services > + Add Integration**.

## Usage & Configuration

* **Auto-Seeded Labels:** On first setup, the integration creates `sort-0` through `sort-9`, and `sort-bottom` under **Settings > Areas, labels & zones > Labels**. Apply them to any device or entity and refresh your dashboard tab.
* **Configure Dialog** (**Settings > Devices & Services > Sort Card Rows > Configure**): Manage your drag-and-drop **Pinned entities** list, customize device_class order, add priority keywords, toggle **Only sort untouched auto-generated** dashboards, or pick those Areas whose card header toggles should be hidden.
* **Troubleshooting:** Check your browser console (`F12` or `Cmd + Option + I`) for `[Sort Card Rows] Active (v1.x.x, ...)`.
