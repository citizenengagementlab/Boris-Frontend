import os
import sys
import string
import ConfigParser
import logging

import newrelic.core.log_file

import newrelic.api.settings
import newrelic.api.import_hook
import newrelic.api.exceptions
import newrelic.api.web_transaction
import newrelic.api.background_task
import newrelic.api.database_trace
import newrelic.api.external_trace
import newrelic.api.function_trace
import newrelic.api.memcache_trace
import newrelic.api.name_transaction
import newrelic.api.error_trace
import newrelic.api.profile_trace
import newrelic.api.object_wrapper
import newrelic.api.application

__all__ = [ 'initialize', 'filter_app_factory' ]

_logger = logging.getLogger('newrelic.config')

# Register our importer which implements post import hooks for
# triggering of callbacks to monkey patch modules before import
# returns them to caller.

sys.meta_path.insert(0, newrelic.api.import_hook.ImportHookFinder())

# Names of configuration file and deployment environment. This
# will be overridden by the load_configuration() function when
# configuration is loaded.

_config_file = None
_environment = None
_ignore_errors = True

# This is the actual internal settings object. Options which
# are read from the configuration file will be applied to this.

_settings = newrelic.api.settings.settings()

# Use the raw config parser as we want to avoid interpolation
# within values. This avoids problems when writing lambdas
# within the actual configuration file for options which value
# can be dynamically calculated at time wrapper is executed.
# This configuration object can be used by the instrumentation
# modules to look up customised settings defined in the loaded
# configuration file.

_config_object = ConfigParser.RawConfigParser()

# Cache of the parsed global settings found in the configuration
# file. We cache these so can dump them out to the log file once
# all the settings have been read.

_cache_object = []

# Define some mapping functions to convert raw values read from
# configuration file into the internal types expected by the
# internal configuration settings object.

_LOG_LEVEL = {
    'CRITICAL' : logging.CRITICAL,
    'ERROR' : logging.ERROR,
    'WARNING': logging.WARNING,
    'INFO' : logging.INFO,
    'DEBUG' : logging.DEBUG,
}

_RECORD_SQL = {
    "off": newrelic.api.settings.RECORDSQL_OFF,
    "raw": newrelic.api.settings.RECORDSQL_RAW,
    "obfuscated": newrelic.api.settings.RECORDSQL_OBFUSCATED,
}

def _map_log_level(s):
    return _LOG_LEVEL[s.upper()]

def _map_app_name(s):
    return s.split(';')[0].strip() or "Python Application"

def _map_ignored_params(s):
    return s.split()

def _map_include_environ(s):
    return s.split()

def _map_transaction_threshold(s):
    if s == 'apdex_f':
        return None
    return float(s)

def _map_record_sql(s):
    return _RECORD_SQL[s]

def _map_ignore_errors(s):
    return s.split()

def _map_function_trace(s):
    return s.split()

# Processing of a single setting from configuration file.

def _raise_configuration_error(section, option=None):
    _logger.error('CONFIGURATION ERROR')
    if section:
        _logger.error('Section = %s' % section)

    if option is None:
        options = _config_object.options(section)

        _logger.error('Options = %s' % options)
        _logger.exception('Exception Details')

        if not _ignore_errors:
            if section:
                raise newrelic.api.exceptions.ConfigurationError(
                        'Invalid configuration for section "%s". '
                        'Check New Relic agent log file for further '
                        'details.' % section)
            else:
                raise newrelic.api.exceptions.ConfigurationError(
                        'Invalid configuration. Check New Relic agent '
                        'log file for further details.')

    else:
        _logger.error('Option = %s' % option)
        _logger.exception('Exception Details')

        if not _ignore_errors:
            if section:
                raise newrelic.api.exceptions.ConfigurationError(
                        'Invalid configuration for option "%s" in '
                        'section "%s". Check New Relic agent log '
                        'file for further details.' % (option, section))
            else:
                raise newrelic.api.exceptions.ConfigurationError(
                        'Invalid configuration for option "%s". '
                        'Check New Relic agent log file for further '
                        'details.' % option)

def _process_setting(section, option, getter, mapper):
    try:
        # The type of a value is dictated by the getter
        # function supplied.

        value = getattr(_config_object, getter)(section, option)

        # The getter parsed the value okay but want to
        # pass this through a mapping function to change
        # it to internal value suitable for internal
        # settings object. This is usually one where the
        # value was a string.

        if mapper:
            value = mapper(value)

        # Now need to apply the option from the
        # configuration file to the internal settings
        # object. Walk the object path and assign it.

        target = _settings
        fields = string.splitfields(option, '.', 1) 

        while True:
            if len(fields) == 1:
                setattr(target, fields[0], value)
                break
            else:
                target = getattr(target, fields[0])
                fields = string.splitfields(fields[1], '.', 1)

        # Cache the configuration so can be dumped out to
        # log file when whole main configuraiton has been
        # processed. This ensures that the log file and log
        # level entries have been set.

        _cache_object.append((option, value))

    except ConfigParser.NoOptionError:
        pass

    except:
        _raise_configuration_error(section, option)

# Processing of all the settings for specified section except
# for log file and log level which are applied separately to
# ensure they are set as soon as possible.

def _process_configuration(section):
    _process_setting(section, 'app_name',
                     'get', _map_app_name)
    _process_setting(section, 'license_key',
                     'get', None)
    _process_setting(section, 'host',
                     'get', None)
    _process_setting(section, 'port',
                     'getint', None)
    _process_setting(section, 'proxy_host',
                     'get', None)
    _process_setting(section, 'proxy_port',
                     'getint', None)
    _process_setting(section, 'proxy_user',
                     'get', None)
    _process_setting(section, 'proxy_pass',
                     'get', None)
    _process_setting(section, 'monitor_mode',
                     'getboolean', None)
    _process_setting(section, 'capture_params',
                     'getboolean', None)
    _process_setting(section, 'ignored_params',
                     'get', _map_ignored_params)
    _process_setting(section, 'capture_environ',
                     'getboolean', None)
    _process_setting(section, 'include_environ',
                     'get', _map_include_environ)
    _process_setting(section, 'transaction_tracer.enabled',
                     'getboolean', None)
    _process_setting(section, 'transaction_tracer.transaction_threshold',
                     'get', _map_transaction_threshold)
    _process_setting(section, 'transaction_tracer.record_sql',
                     'get', _map_record_sql)
    _process_setting(section, 'transaction_tracer.stack_trace_threshold',
                     'getfloat', None)
    _process_setting(section, 'transaction_tracer.explain_enabled',
                     'getboolean', None)
    _process_setting(section, 'transaction_tracer.explain_threshold',
                     'getfloat', None)
    _process_setting(section, 'transaction_tracer.function_trace',
                     'get', _map_function_trace)
    _process_setting(section, 'error_collector.enabled',
                     'getboolean', None),
    _process_setting(section, 'error_collector.capture_source',
                     'getboolean', None),
    _process_setting(section, 'error_collector.ignore_errors',
                     'get', _map_ignore_errors)
    _process_setting(section, 'browser_monitoring.auto_instrument',
                     'getboolean', None)
    _process_setting(section, 'rum.enabled',
                     'getboolean', None)
    _process_setting(section, 'rum.load_episodes_file',
                     'getboolean', None)
    _process_setting(section, 'slow_sql.enabled',
                     'getboolean', None)
    _process_setting(section, 'local_daemon.socket_path',
                     'get', None)
    _process_setting(section, 'local_daemon.synchronous_startup',
                     'getboolean', None)
    _process_setting(section, 'debug.dump_metric_table',
                     'getboolean', None)
    _process_setting(section, 'debug.sql_statement_parsing',
                     'getboolean', None)
    _process_setting(section, 'transaction_metrics.overflow_minimum',
                     'getint', None)
    _process_setting(section, 'transaction_metrics.overflow_maximum',
                     'getint', None)
    _process_setting(section, 'transaction_metrics.overflow_threshold',
                     'getfloat', None)
    _process_setting(section, 'agent_limits.transaction_traces_nodes',
                     'getint', None)
    _process_setting(section, 'agent_limits.sql_query_length_maximum',
                     'getint', None)
    _process_setting(section, 'agent_limits.slow_sql_stack_trace',
                     'getint', None)
    _process_setting(section, 'agent_limits.sql_explain_plans',
                     'getint', None)

# Loading of configuration from specified file and for specified
# deployment environment. Can also indicate whether configuration
# and instrumentation errors should raise an exception or not.

_configuration_done = False

def _load_configuration(config_file=None, environment=None,
        ignore_errors=True, log_file=None, log_level=None):

    global _configuration_done

    global _config_file
    global _environment
    global _ignore_errors

    # Check whether initialisation has been done previously. If
    # it has then raise a configuration error if it was against
    # a different configuration. Otherwise just return. We don't
    # check at this time if an incompatible configuration has
    # been read from a different sub interpreter. If this occurs
    # then results will be undefined. Use from different sub
    # interpreters of the same process is not recommended.

    if _configuration_done:
        if _config_file != config_file or _environment != environment:
          raise newrelic.api.exceptions.ConfigurationError(
                    'Configuration has already been done against '
                    'differing configuration file or environment. '
                    'Prior configuration file used was "%s" and '
                    'environment "%s".' % (_config_file, _environment))
        else:
            return

    _configuration_done = True

    # Update global variables tracking what configuration file and
    # environment was used, plus whether errors are to be ignored.

    _config_file = config_file
    _environment = environment
    _ignore_errors = ignore_errors

    # If no configuration file then nothing more to be done.

    if not config_file:

        _logger.debug("no agent configuration file")

        # Force initialisation of the logging system now in case
        # setup provided by environment variables.

        newrelic.core.log_file.initialize()

        return

    _logger.debug("agent configuration file was %s" % config_file)

    # Now read in the configuration file. Cache the config file
    # name in internal settings object as indication of succeeding.

    if not _config_object.read([config_file]):
        raise newrelic.api.exceptions.ConfigurationError(
                 'Unable to open configuration file %s.' % config_file)

    _settings.config_file = config_file

    # Must process log file entries first so that errors with
    # the remainder will get logged if log file is defined.

    _process_setting('newrelic', 'log_file', 'get', None)

    if environment:
        _process_setting('newrelic:%s' % environment,
                         'log_file', 'get', None)

    if log_file is not None:
        _settings.log_file = log_file

    _process_setting('newrelic', 'log_level', 'get', _map_log_level)

    if environment:
        _process_setting('newrelic:%s' % environment ,
                         'log_level', 'get', _map_log_level)

    if log_level is not None:
        _settings.log_level = log_level


    # Force initialisation of the logging system now that we
    # have the log file and log level.

    newrelic.core.log_file.initialize()

    # Now process the remainder of the global configuration
    # settings.

    _process_configuration('newrelic')

    # And any overrides specified with a section corresponding
    # to a specific deployment environment.

    if environment:
        _settings.environment = environment
        _process_configuration('newrelic:%s' % environment)

    # Log details of the configuration options which were
    # read and the values they have as would be applied
    # against the internal settings object.

    for option, value in _cache_object:
        _logger.debug("agent config %s = %s" % (option, repr(value)))

    # Now do special processing to handle the case where the
    # application name was actually a semicolon separated list
    # of names. In this case the first application name is the
    # primary and the others are linked applications the application
    # also reports to. What we need to do is explicitly retrieve
    # the application object for the primary application name
    # and link it with the other applications. When activating the
    # application the linked names will be sent along to the
    # core application where the association will be created if the
    # do not exist.

    def _process_app_name(section):
        try:
            value = _config_object.get(section, 'app_name')
        except ConfigParser.NoOptionError:
            return False
        else:
            name = value.split(';')[0] or 'Python Application'

            linked = []
            for altname in value.split(';')[1:]:
                altname = altname.strip()
                if altname:
                    linked.append(altname)

            if linked:
                application = newrelic.api.application.application(name)
                for altname in linked:
                    _logger.debug("link to %s" % ((name, altname),))
                    application.link_to_application(altname)

                # Add linked applications into global settings
                # configuration so sent back to core application.

                # FIXME Do this is a try/except for now as will
                # fail when using C version of agent code.

                try:
                    _settings.linked_applications = linked
                except:
                    pass

            return True

    if environment:
        if not _process_app_name('newrelic:%s' % environment):
            _process_app_name('newrelic')
    else:
        _process_app_name('newrelic')

    # Instrument with function trace and callables supplied by the
    # user in the configuration.

    for function in _settings.transaction_tracer.function_trace:
        try:
            (module, object_path) = string.splitfields(function, ':', 1)

            name = None
            group = 'Function'

            _logger.debug("register function-trace %s" %
                    ((module, object_path, name, group),))

            hook = _function_trace_import_hook(object_path, name, group)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section=None,
                    option='transaction_tracer.function_trace')

# Generic error reporting functions.

def _raise_instrumentation_error(type, locals):
    _logger.error('INSTRUMENTATION ERROR')
    _logger.error('Type = %s' % type)
    _logger.error('Locals = %s' % locals)
    _logger.exception('Exception Details')

    if not _ignore_errors:
        raise newrelic.api.exceptions.InstrumentationError(
                'Failure when instrumenting code. Check New Relic '
                'agent log file for further details.')

# Registration of module import hooks defined in configuration file.

def _module_import_hook(module, function):
    def _instrument(target):
        _logger.debug("instrument module %s" %
                ((target, module, function),))

        try:
            getattr(newrelic.api.import_hook.import_module(module),
                    function)(target)
        except:
            _raise_instrumentation_error('import-hook', locals())

    return _instrument

def _process_module_configuration():
    for section in _config_object.sections():
        if not section.startswith('import-hook:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            execute = _config_object.get(section, 'execute')
            fields = string.splitfields(execute, ':', 1)
            module = fields[0]
            function = 'instrument'
            if len(fields) != 1:
                function = fields[1]

            target = string.splitfields(section, ':', 1)[1]

            _logger.debug("register module %s" %
                    ((target, module, function),))

            hook = _module_import_hook(module, function)
            newrelic.api.import_hook.register_import_hook(target, hook)
        except:
            _raise_configuration_error(section)

# Setup wsgi application wrapper defined in configuration file.

def _wsgi_application_import_hook(object_path, application):
    def _instrument(target):
        _logger.debug("wrap wsgi-application %s" %
                ((target, object_path, application),))

        try:
            newrelic.api.web_transaction.wrap_wsgi_application(
                    target, object_path, application)
        except:
            _raise_instrumentation_error('wsgi-application', locals())

    return _instrument

def _process_wsgi_application_configuration():
    for section in _config_object.sections():
        if not section.startswith('wsgi-application:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            application = None

            if _config_object.has_option(section, 'application'):
                application = _config_object.get(section, 'application')

            _logger.debug("register wsgi-application %s" %
                    ((module, object_path, application),))

            hook = _wsgi_application_import_hook(object_path, application)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup background task wrapper defined in configuration file.

def _background_task_import_hook(object_path, application, name, group):
    def _instrument(target):
        _logger.debug("wrap background-task %s" %
                ((target, object_path, application, name, group),))

        try:
            newrelic.api.background_task.wrap_background_task(
                    target, object_path, application, name, group)
        except:
            _raise_instrumentation_error('background-task', locals())

    return _instrument

def _process_background_task_configuration():
    for section in _config_object.sections():
        if not section.startswith('background-task:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            application = None
            name = None
            group = 'Function'

            if _config_object.has_option(section, 'application'):
                application = _config_object.get(section, 'application')
            if _config_object.has_option(section, 'name'):
                name = _config_object.get(section, 'name')
            if _config_object.has_option(section, 'group'):
                group = _config_object.get(section, 'group')

            if name and name.startswith('lambda '):
                vars = { "callable_name":
                         newrelic.api.object_wrapper.callable_name }
                name = eval(name, vars)

            _logger.debug("register background-task %s" %
                    ((module, object_path, application, name, group),))

            hook = _background_task_import_hook(object_path,
                  application, name, group)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup database traces defined in configuration file.

def _database_trace_import_hook(object_path, sql):
    def _instrument(target):
        _logger.debug("wrap database-trace %s" %
                ((target, object_path, sql),))

        try:
            newrelic.api.database_trace.wrap_database_trace(
                    target, object_path, sql)
        except:
            _raise_instrumentation_error('database-trace', locals())

    return _instrument

def _process_database_trace_configuration():
    for section in _config_object.sections():
        if not section.startswith('database-trace:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            sql = _config_object.get(section, 'sql')

            if sql.startswith('lambda '):
                vars = { "callable_name":
                         newrelic.api.object_wrapper.callable_name }
                sql = eval(sql, vars)

            _logger.debug("register database-trace %s" %
                    ((module, object_path, sql),))

            hook = _database_trace_import_hook(object_path, sql)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup external traces defined in configuration file.

def _external_trace_import_hook(object_path, library, url):
    def _instrument(target):
        _logger.debug("wrap external-trace %s" %
                ((target, object_path, library, url),))

        try:
            newrelic.api.external_trace.wrap_external_trace(
                    target, object_path, library, url)
        except:
            _raise_instrumentation_error('external-trace', locals())

    return _instrument

def _process_external_trace_configuration():
    for section in _config_object.sections():
        if not section.startswith('external-trace:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            library = _config_object.get(section, 'library')
            url = _config_object.get(section, 'url')

            if url.startswith('lambda '):
                vars = { "callable_name":
                          newrelic.api.object_wrapper.callable_name }
                url = eval(url, vars)

            _logger.debug("register external-trace %s" %
                    ((module, object_path, library, url),))

            hook = _external_trace_import_hook(object_path, library, url)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup function traces defined in configuration file.

def _function_trace_import_hook(object_path, name, group):
    def _instrument(target):
        _logger.debug("wrap function-trace %s" %
                ((target, object_path, name, group),))

        try:
            newrelic.api.function_trace.wrap_function_trace(
                    target, object_path, name, group)
        except:
            _raise_instrumentation_error('function-trace', locals())

    return _instrument

def _process_function_trace_configuration():
    for section in _config_object.sections():
        if not section.startswith('function-trace:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            # FIXME Temporary work around to exclude Django stuff
            # that was given as example in early agent configuration
            # file but now being included by default.

            if function in ['django.template:NodeList.render_node',
                    'django.template.debug:DebugNodeList.render_node']:
                  continue

            name = None
            group = 'Function'

            if _config_object.has_option(section, 'name'):
                name = _config_object.get(section, 'name')
            if _config_object.has_option(section, 'group'):
                group = _config_object.get(section, 'group')

            if name and name.startswith('lambda '):
                vars = { "callable_name":
                         newrelic.api.object_wrapper.callable_name }
                name = eval(name, vars)

            _logger.debug("register function-trace %s" %
                    ((module, object_path, name, group),))

            hook = _function_trace_import_hook(object_path, name, group)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup memcache traces defined in configuration file.

def _memcache_trace_import_hook(object_path, command):
    def _instrument(target):
        _logger.debug("wrap memcache-trace %s" %
                ((target, object_path, command),))

        try:
            newrelic.api.memcache_trace.wrap_memcache_trace(
                    target, object_path, command)
        except:
            _raise_instrumentation_error('memcache-trace', locals())

    return _instrument

def _process_memcache_trace_configuration():
    for section in _config_object.sections():
        if not section.startswith('memcache-trace:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            command = _config_object.get(section, 'command')

            if command.startswith('lambda '):
                vars = { "callable_name":
                         newrelic.api.object_wrapper.callable_name }
                command = eval(command, vars)

            _logger.debug("register memcache-trace %s" %
                    ((module, object_path, command),))

            hook = _memcache_trace_import_hook(object_path, command)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup name transaction wrapper defined in configuration file.

def _name_transaction_import_hook(object_path, name, group):
    def _instrument(target):
        _logger.debug("wrap name-transaction %s" %
                ((target, object_path, name, group),))

        try:
            newrelic.api.name_transaction.wrap_name_transaction(
                    target, object_path, name, group)
        except:
            _raise_instrumentation_error('name-transaction', locals())

    return _instrument

def _process_name_transaction_configuration():
    for section in _config_object.sections():
        if not section.startswith('name-transaction:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            name = None
            group = 'Function'

            if _config_object.has_option(section, 'name'):
                name = _config_object.get(section, 'name')
            if _config_object.has_option(section, 'group'):
                group = _config_object.get(section, 'group')

            if name and name.startswith('lambda '):
                vars = { "callable_name":
                         newrelic.api.object_wrapper.callable_name }
                name = eval(name, vars)

            _logger.debug("register name-transaction %s" %
                    ((module, object_path, name, group),))

            hook = _name_transaction_import_hook(object_path, name,
                                                 group)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup error trace wrapper defined in configuration file.

def _error_trace_import_hook(object_path, ignore_errors):
    def _instrument(target):
        _logger.debug("wrap error-trace %s" %
                ((target, object_path, ignore_errors),))

        try:
            newrelic.api.error_trace.wrap_error_trace(
                    target, object_path, ignore_errors)
        except:
            _raise_instrumentation_error('error-trace', locals())

    return _instrument

def _process_error_trace_configuration():
    for section in _config_object.sections():
        if not section.startswith('error-trace:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            ignore_errors = []

            if _config_object.has_option(section, 'ignore_errors'):
                ignore_errors = _config_object.get(section,
                        'ignore_errors').split()

            _logger.debug("register error-trace %s" %
                  ((module, object_path, ignore_errors),))

            hook = _error_trace_import_hook(object_path, ignore_errors)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

# Setup function profiler defined in configuration file.

def _function_profile_import_hook(object_path, depth):
    def _instrument(target):
        _logger.debug("wrap function-profile %s" %
                ((target, object_path, depth),))

        try:
            newrelic.api.profile_trace.wrap_function_profile(target,
                    object_path, depth)
        except:
            _raise_instrumentation_error('function-profile', locals())

    return _instrument

def _process_function_profile_configuration():
    for section in _config_object.sections():
        if not section.startswith('function-profile:'):
            continue

        enabled = False

        try:
            enabled = _config_object.getboolean(section, 'enabled')
        except ConfigParser.NoOptionError:
            pass
        except:
            _raise_configuration_error(section)

        if not enabled:
            continue

        try:
            function = _config_object.get(section, 'function')
            (module, object_path) = string.splitfields(function, ':', 1)

            depth = 5

            if _config_object.has_option(section, 'depth'):
                depth = _config_object.getint(section, 'depth')

            _logger.debug("register function-profile %s" %
                    ((module, object_path, depth),))

            hook = _function_profile_import_hook(object_path, depth)
            newrelic.api.import_hook.register_import_hook(module, hook)
        except:
            _raise_configuration_error(section)

def _process_module_definition(target, module, function='instrument'):
    enabled = True
    execute = None

    try:
        section = 'import-hook:%s' % target
        if _config_object.has_section(section):
            enabled = _config_object.getboolean(section, 'enabled')
    except ConfigParser.NoOptionError:
        pass
    except:
        _raise_configuration_error(section)

    try:
        if _config_object.has_option(section, 'execute'):
            execute = _config_object.get(section, 'execute')

        if enabled and not execute:
            _logger.debug("register module %s" %
                    ((target, module, function),))

            newrelic.api.import_hook.register_import_hook(target,
                    _module_import_hook(module, function))
    except:
        _raise_configuration_error(section)

def _process_module_builtin_defaults():
    _process_module_definition('django.core.handlers.base',
            'newrelic.hooks.framework_django',
            'instrument_django_core_handlers_base')
    _process_module_definition('django.core.handlers.wsgi',
            'newrelic.hooks.framework_django',
            'instrument_django_core_handlers_wsgi')
    _process_module_definition('django.core.urlresolvers',
            'newrelic.hooks.framework_django',
            'instrument_django_core_urlresolvers')
    _process_module_definition('django.template',
            'newrelic.hooks.framework_django',
            'instrument_django_template')
    _process_module_definition('django.template.loader_tags',
            'newrelic.hooks.framework_django',
            'instrument_django_template_loader_tags')
    _process_module_definition('django.core.servers.basehttp',
            'newrelic.hooks.framework_django',
            'instrument_django_core_servers_basehttp')
    _process_module_definition('django.contrib.staticfiles.views',
            'newrelic.hooks.framework_django',
            'instrument_django_contrib_staticfiles_views')
    _process_module_definition('django.contrib.staticfiles.handlers',
            'newrelic.hooks.framework_django',
            'instrument_django_contrib_staticfiles_handlers')
    _process_module_definition('django.views.debug',
            'newrelic.hooks.framework_django',
            'instrument_django_views_debug')
    _process_module_definition('django.http.multipartparser',
            'newrelic.hooks.framework_django',
            'instrument_django_http_multipartparser')

    _process_module_definition('flask.app',
            'newrelic.hooks.framework_flask')
    _process_module_definition('flask.templating',
            'newrelic.hooks.framework_flask')

    _process_module_definition('gluon.compileapp',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_compileapp')
    _process_module_definition('gluon.restricted',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_restricted')
    _process_module_definition('gluon.main',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_main')
    _process_module_definition('gluon.template',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_template')
    _process_module_definition('gluon.tools',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_tools')
    _process_module_definition('gluon.http',
            'newrelic.hooks.framework_web2py',
            'instrument_gluon_http')

    _process_module_definition('gluon.contrib.feedparser',
            'newrelic.hooks.external_feedparser')
    _process_module_definition('gluon.contrib.memcache.memcache',
            'newrelic.hooks.memcache_memcache')

    _process_module_definition('pylons.wsgiapp',
            'newrelic.hooks.framework_pylons')
    _process_module_definition('pylons.controllers.core',
            'newrelic.hooks.framework_pylons')
    _process_module_definition('pylons.templating',
            'newrelic.hooks.framework_pylons')

    _process_module_definition('bottle',
            'newrelic.hooks.framework_bottle')

    _process_module_definition('cherrypy._cpdispatch',
            'newrelic.hooks.framework_cherrypy',
            'instrument_cherrypy_cpdispatch')
    _process_module_definition('cherrypy._cpwsgi',
            'newrelic.hooks.framework_cherrypy',
            'instrument_cherrypy_cpwsgi')
    _process_module_definition('cherrypy._cptree',
            'newrelic.hooks.framework_cherrypy',
            'instrument_cherrypy_cptree')

    _process_module_definition('tornado.wsgi',
            'newrelic.hooks.adapter_tornado',
            'instrument_tornado_wsgi')

    _process_module_definition('gunicorn.app.base',
            'newrelic.hooks.adapter_gunicorn',
            'instrument_gunicorn_app_base')

    _process_module_definition('cx_Oracle',
            'newrelic.hooks.database_dbapi2')
    _process_module_definition('MySQLdb',
            'newrelic.hooks.database_dbapi2')
    _process_module_definition('postgresql.interface.proboscis.dbapi2',
            'newrelic.hooks.database_dbapi2')
    _process_module_definition('pyodbc',
            'newrelic.hooks.database_dbapi2')

    _process_module_definition('psycopg2',
            'newrelic.hooks.database_dbapi2')
    _process_module_definition('psycopg2.extensions',
            'newrelic.hooks.database_psycopg2',
            'instrument_psycopg2_extensions')

    _process_module_definition('pysqlite2.dbapi2',
            'newrelic.hooks.database_sqlite')
    _process_module_definition('sqlite3.dbapi2',
            'newrelic.hooks.database_sqlite')

    _process_module_definition('memcache',
            'newrelic.hooks.memcache_memcache')
    _process_module_definition('pylibmc',
            'newrelic.hooks.memcache_pylibmc')

    _process_module_definition('jinja2.environment',
            'newrelic.hooks.template_jinja2')

    _process_module_definition('mako.runtime',
            'newrelic.hooks.template_mako',
            'instrument_mako_runtime')
    _process_module_definition('mako.template',
            'newrelic.hooks.template_mako',
            'instrument_mako_template')

    _process_module_definition('genshi.template.base',
            'newrelic.hooks.template_genshi')

    _process_module_definition('httplib',
            'newrelic.hooks.external_httplib')

    _process_module_definition('httplib2',
            'newrelic.hooks.external_httplib2')

    _process_module_definition('urllib',
            'newrelic.hooks.external_urllib')
    _process_module_definition('urllib2',
            'newrelic.hooks.external_urllib2')

    _process_module_definition('urllib3.request',
            'newrelic.hooks.external_urllib3')

    _process_module_definition('requests.api',
            'newrelic.hooks.external_requests')

    _process_module_definition('feedparser',
            'newrelic.hooks.external_feedparser')

    _process_module_definition('xmlrpclib',
            'newrelic.hooks.external_xmlrpclib')

    _process_module_definition('pysolr',
            'newrelic.hooks.solr_pysolr')

    _process_module_definition('solr',
            'newrelic.hooks.solr_solrpy')

    _process_module_definition('pymongo.connection',
            'newrelic.hooks.nosql_pymongo',
            'instrument_pymongo_connection')
    _process_module_definition('pymongo.collection',
            'newrelic.hooks.nosql_pymongo',
            'instrument_pymongo_collection')

    _process_module_definition('redis.connection',
            'newrelic.hooks.nosql_redis',
            'instrument_redis_connection')
    _process_module_definition('redis.client',
            'newrelic.hooks.nosql_redis',
            'instrument_redis_client')

    _process_module_definition('piston.resource',
            'newrelic.hooks.component_piston',
            'instrument_piston_resource')
    _process_module_definition('piston.doc',
            'newrelic.hooks.component_piston',
            'instrument_piston_doc')

    _process_module_definition('celery.task.base',
            'newrelic.hooks.application_celery',
            'instrument_celery_app_task')
    _process_module_definition('celery.app.task',
            'newrelic.hooks.application_celery',
            'instrument_celery_app_task')
    _process_module_definition('celery.worker',
            'newrelic.hooks.application_celery',
            'instrument_celery_worker')
    _process_module_definition('celery.concurrency.processes',
            'newrelic.hooks.application_celery',
            'instrument_celery_worker')
    _process_module_definition('celery.execute.trace',
            'newrelic.hooks.application_celery',
            'instrument_celery_execute_trace')

    _process_module_definition('flup.server.cgi',
            'newrelic.hooks.adapter_flup',
            'instrument_flup_server_cgi')
    _process_module_definition('flup.server.ajp_base',
            'newrelic.hooks.adapter_flup',
            'instrument_flup_server_ajp_base')
    _process_module_definition('flup.server.fcgi_base',
            'newrelic.hooks.adapter_flup',
            'instrument_flup_server_fcgi_base')
    _process_module_definition('flup.server.scgi_base',
            'newrelic.hooks.adapter_flup',
            'instrument_flup_server_scgi_base')

    _process_module_definition('pywapi',
            'newrelic.hooks.external_pywapi',
            'instrument_pywapi')

    _process_module_definition('meinheld.server',
            'newrelic.hooks.adapter_meinheld',
            'instrument_meinheld_server')

    _process_module_definition('waitress.server',
            'newrelic.hooks.adapter_waitress',
            'instrument_waitress_server')

    #_process_module_definition('pyramid.router',
    #        'newrelic.hooks.framework_pyramid',
    #        'instrument_pyramid_router')

    #_process_module_definition('twisted.web.server',
    #        'newrelic.hooks.framework_twisted',
    #        'instrument_twisted_web_server')
    #_process_module_definition('twisted.web.http',
    #        'newrelic.hooks.framework_twisted',
    #        'instrument_twisted_web_http')
    #_process_module_definition('twisted.web.resource',
    #        'newrelic.hooks.framework_twisted',
    #        'instrument_twisted_web_resource')
    #_process_module_definition('twisted.internet.defer',
    #        'newrelic.hooks.framework_twisted',
    #        'instrument_twisted_internet_defer')

_instrumentation_done = False

def _setup_instrumentation():

    global _instrumentation_done

    if _instrumentation_done:
        return

    _instrumentation_done = True

    _process_module_configuration()
    _process_module_builtin_defaults()

    _process_wsgi_application_configuration()
    _process_background_task_configuration()

    _process_database_trace_configuration()
    _process_external_trace_configuration()
    _process_function_trace_configuration()
    _process_memcache_trace_configuration()

    _process_name_transaction_configuration()

    _process_error_trace_configuration()

    _process_function_profile_configuration()

def initialize(config_file=None, environment=None, ignore_errors=True,
            log_file=None, log_level=None):

    _load_configuration(config_file, environment, ignore_errors,
            log_file, log_level)

    if _settings.monitor_mode: 
        _setup_instrumentation()

def filter_app_factory(app, global_conf, config_file, environment=None):
    initialize(config_file, environment)
    return newrelic.api.web_transaction.WSGIApplicationWrapper(app)
