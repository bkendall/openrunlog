
import env
import logging
from openrunlog import models, constants
import redis
import setproctitle
import tornadoredis
import mongoengine


def main(r, asyncr):
    while True:
        key, userid = r.blpop(constants.calculate_streaks)
        if userid == 'all':
            users = models.User.objects()
        else:
            users = [models.User.objects(id=userid).first()]
        for user in users:
            calculate_streaks(user, asyncr)
            logging.info(
                'computed streaks for {}'.format(user.display_name))
            logging.info(user.streaks)


def calculate_streaks(user, asyncr):
    if not user:
        return

    user.calculate_streaks(asyncr)

if __name__ == '__main__':
    config = env.prefix('ORL_')
    if 'db_uri' not in config or config['db_uri'] == '':
        config['db_uri'] = 'mongodb://' + env.environ['MONGO_PORT_27017_TCP_ADDR'] + '/openrunlog'
    if config['debug'] == 'True':
        config['debug'] = True
    else:
        config['debug'] = False
    config['ORL_REDIS_URI'] = env.environ['REDIS_PORT_6379_TCP_ADDR']
    r = tornadoredis.Client(host=config['ORL_REDIS_URI'])
    mongoengine.connect(
        config['db_name'],
        host=config['db_uri'])
    r = redis.StrictRedis(host=config['ORL_REDIS_URI'], port=6379)
    asyncr = tornadoredis.Client(host=config['ORL_REDIS_URI'])
    asyncr.connect()

    logging.basicConfig(level=logging.INFO)
    setproctitle.setproctitle('orl.workers.streak')

    main(r, asyncr)
