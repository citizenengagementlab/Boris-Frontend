
require 'compass'


# Change Compass configuration
# compass_config do |config|
#   config.output_style = :compact
# end


# Automatic image dimensions on image_tag helper
# activate :automatic_image_sizes

###
# Page command
###

# Per-page layout changes:
# 
# With no layout
# page "/path/to/file.html", :layout => false
# 
# With alternative layout
# page "/path/to/file.html", :layout => :otherlayout
# 
# A path which all have the same layout
# with_layout :admin do
#   page "/admin/*"
# end

# Proxy (fake) files
# page "/this-page-has-no-template.html", :proxy => "/template-file.html" do
#   @which_fake_page = "Rendering a fake page with a variable"
# end

###
# Helpers
###

# Methods defined in the helpers block are available in templates
helpers do

  # Padrino label_tag helper, here to remove stupid trailing colon on the caption.
  def label_tag(name, options={}, &block)
    # original
    # options.reverse_merge!(:caption => "#{name.to_s.humanize}: ", :for => name)
    options.reverse_merge!(:caption => name.to_s.humanize.titleize, :for => name)
    caption_text = options.delete(:caption)
    caption_text << "<span class='required'>*</span> " if options.delete(:required)
    if block_given? # label with inner content
      label_content = caption_text + capture_html(&block)
      concat_content(content_tag(:label, label_content, options))
    else # regular label
      content_tag(:label, caption_text, options)
    end
  end
end



# Build-specific configuration
configure :build do
  # For example, change the Compass output style for deployment
  # activate :minify_css
  
  # Minify Javascript on build
  # activate :minify_javascript
  
  # Enable cache buster
  # activate :cache_buster
  
  # Use relative URLs
  activate :relative_assets
  
  # Compress PNGs after build
  # First: gem install middleman-smusher
  # require "middleman-smusher"
  # activate :smusher
  
  # Or use a different image path
  # set :http_path, "/Content/images/"
end