# Final Magento Catalogue Profile — report240426.csv
This profile is generated from the final Magento catalogue model supplied by the user on 2026-04-24. The full CSV is intentionally not bundled in the repo zip because it is large and production-like; only the schema profile and first 100 rows sample are included.
## File Shape
- Rows: `121,573`
- Columns: `90`
- Unique SKUs: `121,572`
- Duplicate SKU examples: `none observed`
## Final 90 Columns
```text
attribute_set_id
sku
name
meta_title
url_key
sku_for_vendor_product
treatment
carat_weight
classification
cutting_style
dimensions
j_colour
name2
offers
vendor_id
weight_ratti
shipping_days
hsn_code
price
special_price
weight_carat
price_per_carat
weight_sort1
status
tax_class_id
gemstone
gem_composition
shape
certification
return_policy
colour
cut
dimension_type
dispatch_days
gemstone2
vendor
offer_type
origin
product_type
description
short_description
comment_explation
description2
qty
is_in_stock
gemstone3
image
small_image
thumbnail
invoice_id
news_from_date
news_to_date
stickers
callfor
quality_config_gem
redirect_select_for_quality
select_for_quality
mainproduct_forjewlrypage
gemstone2_type
price_per_carat_range
metal_config
ideal_design
price_for_jewelry
promotion_baseprice_jewlery
product_discount_percentage
promotion_discount_price
specific_gravity
refractive_index
show_pricing_table
callfor_price_wanto_show
automatic_video_link
call_for_price_text
calibrated_size_range
beads_size
hole
beads_in_strand
length_inches
quality_grade
strands
dimension_approx
arrangement_type
length_cm
how_to_wear
certificate_number1
verified_certificateimage
verified_certificateimage1
additional_certification
price_range
gemstone_benifits_new
product_category_type
```
## Required-Field Missing Counts
| Field | Missing count |
|---|---:|
| `sku` | 2 |
| `name` | 0 |
| `gemstone` | 660 |
| `origin` | 42,442 |
| `treatment` | 898 |
| `carat_weight` | 9,815 |
| `shape` | 2 |
| `colour` | 557 |
| `cut` | 977 |
| `dimensions` | 47,023 |
| `certification` | 0 |
| `price` | 2 |
| `qty` | 0 |
| `image` | 5,836 |
| `small_image` | 5,836 |
| `thumbnail` | 5,813 |

## Core Categorical Values

### `attribute_set_id`

| Value | Count |
|---|---:|
| `Gemstones` | 75,685 |
| `Rings - Config X002` | 24,781 |
| `Pendants - Config X002` | 9,726 |
| `Bracelets - Config X002` | 4,634 |
| `Brooches - Config X002` | 3,075 |
| `Necklaces - Config X002` | 1,896 |
| `Earrings - Config X002` | 1,256 |
| `Gemstones - Config1` | 249 |
| `Default` | 163 |
| `beads-necklace-byquality` | 99 |
| `Gemstone Sets - Config N1` | 9 |

### `status`

| Value | Count |
|---|---:|
| `Enabled` | 109,877 |
| `Disabled` | 11,696 |

### `tax_class_id`

| Value | Count |
|---|---:|
| `Jewellery` | 48,203 |
| `Jewellery Semiprecious` | 46,358 |
| `Jewellery Sapphire` | 23,736 |
| `Jewellery Corals` | 3,202 |
| `All Taxable Services` | 38 |
| `Taxable Goods` | 28 |
| `Diamond` | 5 |
| `None` | 1 |

### `vendor`

| Value | Count |
|---|---:|
| `GP` | 67,334 |
| `Vendor_IN` | 6,057 |
| `Vendor_INT` | 2,259 |

### `offer_type`

| Value | Count |
|---|---:|
| `Loose Gemstone` | 75,706 |
| `Ring` | 19,926 |
| `Pendant` | 9,105 |
| `Bracelet` | 3,842 |
| `Brooch` | 3,075 |
| `Necklace` | 1,896 |
| `Engagement Ring` | 1,822 |
| `Earrings` | 1,282 |
| `Service` | 8 |
| `Chain` | 3 |

### `product_type`

| Value | Count |
|---|---:|
| `Single Stone` | 74,632 |
| `Ring` | 24,411 |
| `Pendant` | 9,743 |
| `Bracelet` | 4,651 |
| `Brooch` | 3,075 |
| `Necklace` | 1,896 |
| `Earrings` | 1,282 |
| `Rough` | 570 |
| `Pair` | 455 |
| `Custom Jewelry` | 449 |
| `Beads` | 135 |
| `Gemstone Set` | 57 |
| `Necklace Layouts` | 45 |
| `Gemstone Lot` | 5 |
| `Pending Classification` | 3 |
| `Chain` | 3 |
| `Layouts` | 1 |

### `product_category_type`

| Value | Count |
|---|---:|
| `MP` | 67,166 |
| `P` | 23,364 |
| `SP` | 1,059 |
| `UP` | 3 |

### `gemstone2_type`

| Value | Count |
|---|---:|
| `3 - Semi-Precious` | 34,437 |
| `2 - Mid-Precious` | 30,210 |
| `1 - Precious` | 30,086 |
| `0 - Ultra-Luxury` | 1,171 |

### `certification`

| Value | Count |
|---|---:|
| `Free Lab Certificate` | 49,706 |
| `ITLGR Certified` | 28,107 |
| `AGR Certified` | 26,071 |
| `IGI Certified` | 4,053 |
| `GEMTRUE Certified` | 3,828 |
| `JBN Certified` | 2,574 |
| `IIGJ Certified` | 2,061 |
| `IGITL Certified` | 1,011 |
| `No` | 918 |
| `GRS Certified` | 837 |
| `ITLGJ Certified` | 373 |
| `SHRI ZAVERI MAHAJAN` | 366 |
| `GSI Certified` | 356 |
| `BELLEROPHON Certified` | 220 |
| `GIA Certified` | 214 |
| `G.I.I Certified` | 177 |
| `ICA GEMLAB Certified` | 151 |
| `AIGS Certified` | 100 |
| `GJSPC Certified` | 86 |
| `ISKON Certified` | 69 |

### `return_policy`

| Value | Count |
|---|---:|
| `10 Day Money-Back Returns*` | 76,146 |
| `10 Day Replacements*` | 45,343 |
| `30 Day Replacements*` | 40 |
| `No` | 35 |
| `30 Day Money-Back Returns*` | 6 |
| `No Return/No Refund` | 3 |

### `dimension_type`

| Value | Count |
|---|---:|
| `Not Calibrated` | 53,691 |
| `Calibrated` | 22,340 |

### `cut`

| Value | Count |
|---|---:|
| `Faceted` | 85,040 |
| `Cabochon` | 33,952 |
| `Rough` | 634 |
| `Mixed Cuts` | 400 |
| `Carved` | 313 |
| `Checkerboard` | 121 |
| `Mixed Cut` | 103 |
| `Irregular` | 21 |
| `Pending Classification` | 12 |

### `shape`

| Value | Count |
|---|---:|
| `Oval` | 82,174 |
| `Octagonal` | 12,593 |
| `Cushion` | 8,168 |
| `Round` | 6,094 |
| `Pear` | 5,101 |
| `Triangular` | 1,186 |
| `No` | 1,053 |
| `Cylinder` | 861 |
| `Rectangle` | 847 |
| `Irregular(Rough)` | 640 |
| `Baroque` | 607 |
| `Marquise` | 330 |
| `Carving` | 288 |
| `Square` | 270 |
| `Mixed Shapes` | 268 |
| `Sugarloaf` | 262 |
| `Heart` | 241 |
| `Fancy` | 233 |
| `Semi Baroque` | 89 |
| `Drop` | 68 |

### `hsn_code`

| Value | Count |
|---|---:|
| `71039990` | 16,410 |
| `71039120` | 15,245 |
| `71039949` | 10,077 |
| `9999999` | 9,902 |
| `71179090` | 9,834 |
| `71039130` | 7,497 |
| `71039110` | 6,446 |
| `71131915` | 5,468 |
| `71131919` | 4,710 |
| `71131120` | 4,073 |
| `71131145` | 4,070 |
| `96019040` | 3,188 |
| `71039939` | 3,166 |
| `71131149` | 2,925 |
| `71039951` | 2,421 |
| `71131940` | 2,337 |
| `71131930` | 1,959 |
| `71039911` | 1,777 |
| `71012200` | 1,582 |
| `71039921` | 1,324 |

### `dispatch_days`

| Value | Count |
|---|---:|
| `0 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 65,593 |
| `7 Business Days` | 24,066 |
| `8 Business Days` | 16,348 |
| `3 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 6,065 |
| `4 Business Days` | 2,525 |
| `9 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 2,309 |
| `1 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 1,647 |
| `6 Business Days` | 1,357 |
| `15 Business Days` | 921 |
| `4 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 192 |
| `2 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 141 |
| `5 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 110 |
| `3 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold Items)` | 91 |
| `13 Business Days` | 27 |
| `4 Business Days (+12 Days if Customized Jewellery)` | 19 |
| `7 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 13 |
| `10 Business Days (+5 days for typical Jewellery; +14 days for Bracelet/Gold/CZ/Diamond Items)` | 5 |
| `5 Business Days` | 3 |
| `10 Business Days` | 3 |
| `3 Business Days` | 2 |

### `offers`

| Value | Count |
|---|---:|
| `Express Dispatch` | 67,116 |
| `Call for Price` | 2,953 |
| `Coming Soon` | 124 |

## Numeric Ranges
| Field | Count | Min | Max | Bad values |
|---|---:|---:|---:|---:|
| `carat_weight` | 111,758 | 0 | 2445 | 0 |
| `weight_ratti` | 75,798 | 0 | 2716.67 | 0 |
| `shipping_days` | 121,479 | 0 | 16 | 0 |
| `price` | 121,571 | 0.0000 | 1368600.0000 | 0 |
| `special_price` | 33 | 750.0000 | 27670.0000 | 0 |
| `weight_carat` | 112,653 | 0.0000 | 2445.0000 | 0 |
| `price_per_carat` | 78,639 | 0.0000 | 1709677.0000 | 0 |
| `weight_sort1` | 121,104 | 0.0000 | 244500.0000 | 0 |
| `qty` | 121,573 | -3345.0000 | 99999986.0000 | 0 |
| `specific_gravity` | 78,838 | 0 | 5.6 | 0 |
| `price_range` | 73,161 | 0 | 3113700 | 2,458 |

## Engineering Decisions Taken From This Profile
- The export model is locked to the exact 90-column order from this file.
- `attribute_set_id` is a label in this model, not the old `_attribute_set` field.
- CSV export must preserve old spellings: `comment_explation`, `promotion_baseprice_jewlery`, and `gemstone_benifits_new`.
- Existing catalogue data contains legacy gaps, so validator supports `create` mode and `legacy_audit` mode. Create mode blocks missing core fields; legacy audit reports warnings for existing-data cleanup.
- `qty` can be negative in the legacy catalogue, so it is allowed in audit/update mode but create-mode workflows should normally prevent publish until stock is corrected.
- `origin` is important but missing in many existing rows; new loose gemstone creation should still require it because it drives GemPundit filtering, SEO, trust, and pricing.
