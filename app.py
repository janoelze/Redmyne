import urllib
import json
import urllib2
from optparse import OptionParser


BASE_URL = 'http://cos.gfedev.de/'
API_KEY = ''


def l(m): print '| %s' % m


def get_opts():
    parser = OptionParser()
    parser.add_option("-k", "--key", dest="key",
                      help="Your Redmine API Key.", metavar="KEY")
    return parser.parse_args()


def get_percentage(ratio):
    i = (int(ratio))
    max = 10
    return '[%s%s] %s%%' % ('#' * (i / 10), ' ' * (max - i / 10), i)


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


def print_issue(issue):
    l('ISSUE #%s' % (issue['id']))
    l('\t>> %s @ %s' % (issue['subject'], issue['project_name']))
    l('\tDue: %s' % issue['due_date'])
    l('\tEstimated Hours: %s' % (issue['estimated_hours']))
    l('\tProgress: %s' % (get_percentage(issue['done_ratio'])))
    l('')


def format_issues(json_string):
    print json_string
    response = json.loads(json_string)
    l("You've got %s open issues:\n|" % (response['total_count']))
    for issue in response['issues']:
        if issue['subject'] != '':
            
            default = '-'
            
            issue_f = {
                'id': issue.get('id', default),
                'subject': issue.get('subject', default),
                'project_name': issue['project'].get('name', default),
                'due_date': issue.get('due_date', default),
                'estimated_hours': issue.get('estimated_hours', default),
                'done_ratio': issue.get('done_ratio', default)
            }
            print_issue(issue_f)


if __name__ == "__main__":
    (opts, args) = get_opts()
    API_KEY = opts.key
    format_issues(get_issues())
