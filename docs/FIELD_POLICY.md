# Field Policy

## Staff fields

These are allowed in clean upload templates:

```text
sku
sku_for_vendor_product
name
gemstone
origin
treatment
carat_weight
shape
colour
cut
cutting_style
dimensions
dimension_type
certification
certificate_number1
price
special_price
qty
vendor
vendor_id
hsn_code
dispatch_days
shipping_days
return_policy
main_image
gallery_images
verified_certificateimage
automatic_video_link
short_description
description
meta_title
meta_description
url_key
classification
product_category_type
gemstone_benifits_new
```

## Auto fields

These are generated:

```text
weight_ratti
weight_carat
weight_sort1
price_per_carat
price_range
price_per_carat_range
is_in_stock
image
small_image
thumbnail
url_path
meta_title
meta_description
short_description
description
```

## Admin-only fields

These should not be manually filled by normal staff:

```text
attribute_set_id
tax_class_id
status
visibility
quality_config_gem
redirect_select_for_quality
select_for_quality
mainproduct_forjewlrypage
metal_config
ideal_design
promotion_baseprice_jewlery
promotion_discount_price
show_pricing_table
callfor_price_wanto_show
call_for_price_text
```

## GemPundit-specific rules

- `weight_ratti = carat_weight / 0.91`
- `price_per_carat = price / carat_weight`
- `is_in_stock = 1` if `qty > 0`, else `0`
- SEO URL should include gemstone, carat, origin, and SKU
- Certificate and image mapping should be visible in review before publish
- Keep `gemstone_benifits_new` spelling for Magento compatibility
