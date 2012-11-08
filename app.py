import urllib
import json
import urllib2
from optparse import OptionParser


BASE_URL = 'http://cos.gfedev.de/'
API_KEY = ''
M1 = '\033[1;35m'
M2 = '\033[1;m'


def get_opts():
    parser = OptionParser()
    parser.add_option("-k", "--key", dest="key", help="Your Redmine API Key.", metavar="KEY")
    return parser.parse_args()


def get_issues():
    params = {
        'assigned_to_id': 'me',
        'key': API_KEY,
        'set_filter': '1',
        'sort': 'priority%3Adesc%2Cupdated_on%3Adesc'
    }
    path = 'issues.json?%s' % urllib.urlencode(params)
    r = urllib2.urlopen('%s%s' % (BASE_URL, path))
    return r.read()

def l(m): print '| %s' % m


def format_issues(json_string):
    response = json.loads(json_string)
    l("You've got %s open isssues:\n|" % (response['total_count']))
    for issue in response['issues']:
        if issue['subject'] != '':
            l('ISSUE #%s - Prio: %s' % (issue['id'], issue['priority']['name'])) 
            l('\t>> %s @ %s' % (issue['subject'], issue['project']['name'])) 
            l('\tDue: %s' % issue['due_date']) 
            l('\tEstimated Hours: %s' % (issue['estimated_hours'])) 

if __name__ == "__main__":
    (opts, args) = get_opts()
    API_KEY = opts.key
    format_issues(get_issues())