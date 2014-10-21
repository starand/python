import os
import ConfigParser
import wdutils


_defaults = {
    'watchdog' : {
        'pidfile' : 'pid'
    },

    'subprocess' : {
        'name' : '',
        'binary' : '',
        'statefile' : 'state',
        'exit_error_message_file' : 'error_file',
        'max_stop_timeout' : 10,
        'stderr_file' : 'stderr_file'
    },

    'pg' : {
        'check_interval_sec' : 1
    },
}


class Config(object):
    def __init__(self):
        self.configFile = os.path.join(wdutils.getScriptDir(), 'watchdog.ini')
        self.parser = ConfigParser.SafeConfigParser()
        self.parser.read(self.configFile)

    def getOptionFromStorage(self, section, key, storage):
        result = None
        if section in storage:
            values = storage[section]
            if key in values:
                result = values[key]
        return result

    def getOption(self, section, key):
        value = self.getOptionFromStorage(section, key, self.parser._sections)
        if not value:
            value = self.getOptionFromStorage(section, key, _defaults)
        return value

cfg = Config()
