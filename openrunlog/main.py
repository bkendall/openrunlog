
import env
import futures
import sys
import mongoengine
import os
import setproctitle
from tornado import web, ioloop, process
from tornado.options import define, options, parse_command_line
import tornadoredis
import tornadotinyfeedback

import home
import login
import dashboard
import data
import racelog
import runs
import groups
import calendar


config = env.prefix('ORL_')
print config
if config['debug'] == 'True':
    config['debug'] = True
else:
    config['debug'] = False

settings = {
        'debug': config['debug'],
        'cookie_secret': config['cookie_secret'],
        'template_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates"),
        'static_path': os.path.join(os.path.dirname(os.path.abspath(__file__)), "static"),
        'login_url': '/login',
}

server_settings = {
    "xheaders" : True,
}

application = web.Application([
    (r'/', home.HomeHandler),
    (r'/login', login.LoginHandler),
    (r'/logout', login.LogoutHandler),
    (r'/register', login.RegisterHandler),
    (r'/settings', login.SettingsHandler),
    (r'/settings/dailymile/noexport', login.DailyMileLogoutHandler),
    (r'/auth/dailymile', login.DailyMileHandler),
    (r'/auth/facebook', login.FacebookHandler),
    (r'/u/([a-zA-Z0-9_]+)', dashboard.ProfileHandler),
    (r'/u/([a-zA-Z0-9_]+)/calendar', calendar.CalendarHandler),
    (r'/u/([a-zA-Z0-9_]+)/calendar/miles', calendar.CalendarMilesHandler),
    (r'/u/([a-zA-Z0-9_]+)/races', racelog.AllRacesHandler),
    (r'/u/([a-zA-Z0-9_]+)/races/([A-Za-z0-9]{24})', racelog.ShowRaceHandler),
    (r'/u/([a-zA-Z0-9_]+)/runs', runs.AllRunsHandler),
    (r'/u/([a-zA-Z0-9_]+)/run/([A-Za-z0-9]{24})', runs.ShowRunHandler),
    (r'/g', groups.GroupDashboardHandler),
    (r'/g/([a-zA-Z0-9_]+)', groups.GroupHandler),
    (r'/add', runs.AddRunHandler),
    (r'/remove', runs.RemoveRunHandler),
    (r'/data/([A-Za-z0-9]{24})/this_week', data.ThisWeekHandler),
    (r'/data/([A-Za-z0-9]{24})/recent', data.RecentRunsHandler),
    (r'/data/([A-Za-z0-9]{24})/mileage/weekly', data.WeeklyMileageHandler),
    (r'/data/([A-Za-z0-9]{24})/runs/weekday', data.WeekdayRunsHandler),
    (r'/data/([A-Za-z0-9]{24})/runs/year', data.DailyRunsHandler),
    (r'/data/([A-Za-z0-9]{24})/runs/month', data.MonthRunsHandler),
], **settings)

application.config = config
application.thread_pool = futures.ThreadPoolExecutor(max_workers=3)
application.tf = tornadotinyfeedback.Client('openrunlog')
application.redis = tornadoredis.Client()

application.redis.connect()


if __name__ == '__main__':
    define('port', default=11000, help='TCP port to listen on')
    parse_command_line()
    setproctitle.setproctitle('orl.app')

    mongoengine.connect(
            config['db_name'], 
            host=config['db_uri'])

    if not config['debug']:
        process.fork_processes(process.cpu_count()*2 + 1)
    application.listen(options.port, **server_settings)
    ioloop.IOLoop.instance().start()

