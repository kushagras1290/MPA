# Sample CSV Profile

Source file: `samples/Final_Catalog_22-04-2026.csv`

## Shape

- Rows: `52`
- Columns: `157`

## Important observations

- `_attribute_set` is consistently `Gemstones`.
- `_type` is consistently `simple`.
- `_product_websites` is consistently `base`.
- `a` appears to be an internal numeric source/vendor/product ID.
- `a.1` appears to be the source image path.
- `a.2` appears to be the automatic video filename.
- `image`, `small_image`, and `thumbnail` are blank in the sample, while `a.1` contains image paths.
- `status` is `2`, which fits disabled/draft behavior.
- `tax_class_id` is `2`.
- `qty` is `1`.
- `is_in_stock` is `1`.
- `vendor` includes `GP` and `Vendor_IN`.
- `offers` includes `Express Dispatch` and `Call for Price`.
- `gemstone_benifits_new` is present with the legacy spelling.


## Validation result against current strict loose-gemstone rules

The sample file is mostly clean, but strict validation flags 8 rows where `origin` is blank:

```text
GP159138
GP159139
GP159140
GP159141
GP159142
GP159143
GP159144
GP159145
```

This is deliberate. Origin is a pricing/filter/trust field for GemPundit-style gemstone products. Admin can relax this rule in `backend/app/domain/field_policy.py` if needed.

## Detected gemstone values

```text
Amethyst
Blue Topaz
Citrine
Emerald
Red Coral
Ruby
White Sapphire
Yellow Sapphire
```

## Detected origin values

```text
Brazil
Italy
Myanmar (Burma)
Sri Lanka (Ceylon)
Zambia
```

## Detected certification values

```text
AGR Certified
Free Lab Certificate
IIGJ Certified
ITLGR Certified
```

## Detected shape values

```text
Cushion
Cylinder
Octagonal
Oval
Round
Triangular
```

## Detected treatment values

```text
All Blue Topaz worldwide is always Irradiated
Unheated and Untreated (No Indications Observed)
Unheated and Untreated (Oiling Only)
```

Full machine-readable profile is stored at:

```text
samples/column_profile.json
```
