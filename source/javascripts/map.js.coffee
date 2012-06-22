$select = $ "#state"

$("#map").vectorMap
  backgroundColor: "transparent"
  borderColor:     "#C1BFBE"
  borderOpacity:   1
  borderWidth:     1
  color:           "#FFF"
  enableZoom:      false
  map:             "usa_en"
  selectedColor:   "#21CB00"
  showTooltip:     true
  onRegionClick:   (el, code, region) -> $select.val code.toUpperCase()

