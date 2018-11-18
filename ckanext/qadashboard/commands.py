from ckanext.qadashboard import model as plugin_model
import ckan.plugins as plugins
import logging

log = logging.getLogger(__name__)

class QADashboardCommands (plugins.toolkit.CkanCommand):

    '''
    Creates needed plugin tables
    Use:
        paster qadashboard initdb -c /etc/ckan/default/production.ini
    '''

    summary = __doc__.split('\n')[0]
    usage = __doc__
    min_args = 0
    max_args = 2
    
    
    def command(self):
        if not self.args or self.args[0] in ['--help', '-h', 'help']:
            print self.usage
            sys.exit(1)

        cmd = self.args[0]
        self._load_config()

        if cmd == 'initdb':
            self.initdb()
        else:
            self.log.error('Command %s not recognized' % (cmd,))


    def initdb():
        
        plugin_model.init_tables()
        self.log.info('All tables created.')