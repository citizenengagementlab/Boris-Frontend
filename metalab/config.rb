require 'active_support/core_ext/hash/indifferent_access'
require 'compass'
require 'yaml'

Slim::Engine.set_default_options :pretty => true, :tabsize => 2


# Methods defined in the helpers block are available in templates
helpers do



  # Padrino label_tag helper, here to remove stupid trailing colon on the caption.
  def label_tag(name, options={}, &block)
    options.reverse_merge!(:caption => name.to_s.humanize.titleize, :for => name)
    super
  end

  def text_field_tag(name, options={})
    options.reverse_merge!(:id => name)
    super
  end

  def check_box_tag(name, options={})
    options.reverse_merge!(:id => name)
    super
  end

  def select_options(name)
    @select_values ||= YAML.load_file(File.join(settings.root, 'data', 'select_values.yml')).with_indifferent_access
    @select_values[name]
  end

  def select_tag(name, options={})
    if options[:options].nil? && !select_options(name).nil?
      options.reverse_merge!(:options => select_options(name), :id => name)
    end
    super
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