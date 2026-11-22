# Sort Card Rows

A lightweight Home Assistant frontend integration that lets you control the order of entity and device rows inside dashboard cards—including auto-generated dashboards (such as **Overview (legacy)** and **Areas**) as well as custom **Entities** and **Grid** cards—without renaming entities to alphabetize them, or converting them to custom cards and dashboards.

Empowers you **to position the most important controls and information first**.

## Features & Sorting Priority

The rows inside dashboard cards are ordered using a chain of sorting rules before falling back to Home Assistant's default alphabetization. While some sorting may improve immediately upon installation (e.g. Temperature before Humidity sensors), most people will likely use either the first or second sorting rule methods to accomplish their desired order. However, the available sorting methods are quite extensive:
1. **Pinned Entities (Drag-and-Drop):** Entities selected from **Pinned entities** in the integration's **Configure** dialog sort to the top of their card. This method supports drag-and-drop ordering of those items.
2. **Device & Entity `sort-x` Labels:** Assign native Home Assistant labels (`sort-1` through `sort-9`, `sort-top`, `sort-bottom`, a `sort-0` label to temporarily push a row toward the top, or even create custom decimal labels like `sort-1.5`):
	* **Card Row Ordering:** Attach `sort-1`, `sort-2`, or `sort-bottom` directly to individual switch sensor entities to pin them to the top or bottom of a card.)
	* **Multi-Device Grouping:** Attach a `sort-x` label to a Device (including *parent* devices with multiple post-`2026.11.0` *child* devices) to keep all of its entities grouped together as a block, and attach more `sort-x` labels to its Entities to order rows within that device group.
3. **Device Class Grouping:** Unranked rows group automatically by device_class using your configured priority list (defaults to `temperature`, `humidity`, `illuminance`, `pressure`, `atmospheric_pressure`, `radon`, `carbon_dioxide`, `battery`; but the user can edit the order and add or delete device class names). *Note: For sensors without a device_class, apply a label like `sort-temperature` or `sort-pressure` to make that sensor sort like others that do have a device class.*
4. **Priority Keywords:** Optional comma-separated keywords (for example, `Outdoor, Indoor`) allow you to sort rows by keywords found in the switch or sensor entity name, just ahead of the default alphabetization order. For example, you could set your dashboard to display the `Outdoor Temperature` before the `Indoor Temperature` automatically, without assigning labels to the entities.
5. **Alphabetical Tie-Breaker:** Any remaining ties sort alphabetically by the switch or sensor entity name. This is the default HA behavior for automatically generated cards.

### Bonus: Card Header Toggle Hiding

* Suppress the card title toggle switch in the header of multi-switch/light cards by selecting Areas under **Hide card headers for these areas** in **Configure**.

## Installation

1. **Marketplace / HACS (Recommended):**
	* Open **Settings > Marketplace (or HACS)**, click the three dots (...) in the top-right corner > **Custom repositories**, and add `https://github.com/tcrgit/ha-sort-card-rows` as an **Integration**.
	* Install **Sort Card Rows**, click Setup (or **Restart Home Assistant** and add it under **Settings > Devices & Services > + Add Integration**), and hard-refresh your browser (`Ctrl + Shift + R` or `Cmd + Shift + R`).
2. **Manual:**
	* Copy custom_components/sort_card_rows into /config/custom_components/, **Restart Home Assistant**, and add **Sort Card Rows** via **Settings > Devices & Services > + Add Integration**.

## Usage & Configuration

* **Auto-Seeded Labels:** On first setup, the integration creates `sort-0` through `sort-9`, `sort-top` and `sort-bottom` under **Settings > Areas, labels & zones > Labels**. Apply them to any device or entity and refresh your dashboard tab.
* **Configure Dialog** (**Settings > Devices & Services > Sort Card Rows > Configure**): Manage your drag-and-drop **Pinned entities** list, customize device_class order, add priority keywords, toggle which types of dashboards to sort, or pick those Areas whose card header toggles should be hidden.
* **Troubleshooting:** Check your browser console (`F12` or `Cmd + Option + I`) for `[Sort Card Rows] Active (v1.x.x, ...)`.

## Support for Other Dashboard Templates 

* **Where it works best:** This integration is designed for **Overview (legacy)**, **Areas** auto-generated dashboards, and standard **Entities** or **Grid** cards where multiple devices and sensors share a single card. It will also work on custom (Lovelace) dashboards, but it can be a bit quirky in Edit mode.

### Custom (Lovelace) Dashboards Unsorted by Default

* To support the use of both automatic and custom dashboards, **custom (Lovelace) dashboard card rows and tiles are not sorted by default**, preserving the manual ordering you set using drag-and-drop or YAML in the Lovelace GUI editor. This lets you attach a `sort-x` label to a sensor or switch so a switch or sensor entity sorts properly on auto-generated dashboards while leaving its position untouched on custom dashboards.
* If you would like to have your sorting rules to apply to custom dashboards as well, uncheck **Only sort auto-generated dashboards** in **Configure**—note that when toggled off, your `sort-x` rules will override any manual drag-and-drop or YAML ordering made in Edit Mode---so disable this setting with caution.
  * *Note that when the sorting rules are being applied to custom dashboards and you are editing a custom dashboard, the sorting automatically **pauses** and restores each card's underlying YAML order so clicking or dragging tiles in edit mode always opens and moves the card as expected, then **immediately applies the sorting rules only after you click Done**.)*

### Note on Home Dashboards (`2026.2+`)

* **Largely leaves the newer Home Dashboard untouched:** Because Home Assistant's newer **Home Dashboard** templates use Area navigation buttons and place each device as a tile in its own separate section rather than grouping an entire room's (or area's) switches, sensors and devices onto a list card, **Sort Card Rows** does not reorder those views. 
* The only exception is when multiple entities share a single section, such as in the **Favorites** row on the Home Dashboard's version of Overview.
