import django, threading, time, datetime
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
from django.utils.module_loading import import_string

class Command(BaseCommand):
    def create_container(self):
        klass = import_string(settings.NOTASQUARE_URAD_CONTAINER)
        container = klass()
        container.build()
        return container
    def get_current_time(self):
        return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
    def spawn_consumer(self, consumer_name):
        container = self.create_container()
        klass = import_string(consumer_name)
        consumer = klass()
        consumer.set_container(container)
        thread_name = threading.currentThread().getName()

        ctime = self.get_current_time()
        container.get_logger().info(ctime + ' | Spawn consumer (' + str(consumer_name) + " - " + thread_name + "): START")
        consumer.execute()
        ctime = self.get_current_time()
        container.get_logger().info(ctime + ' | Spawn consumer (' + str(consumer_name) + " - " + thread_name + "): DONE")
    def check_schedule(self, scheduler, current_time):
        ctime = datetime.datetime.fromtimestamp(current_time)
        (cyear, cmon, cdate, chour, cmin, csec, cwday, cyday, cisdst) = ctime.timetuple()

        if 'minutes' in scheduler:
            if not cmin in scheduler['minutes']:
                return False
        if 'hours' in scheduler:
            if not chour in scheduler['hours']:
                return False
        if 'dates' in scheduler:
            if not cdate in scheduler['dates']:
                return False
        if 'weekdays' in scheduler:
            if not cwday in scheduler['weekdays']:
                return False
        return True
    def handle(self, *args, **options):
        klass = import_string(settings.NOTASQUARE_CONSUMERS_CONFIG_CLASS)
        consumers = klass.CONSUMER_SCHEDULERS
        # Spawn always consumer first
        i = 0
        for consumer in consumers:
            if consumer['schedule'] == 'always':
                print "Spawn " + consumer['consumer']
                t = threading.Thread(name='consumer-' + str(i), target=lambda: self.spawn_consumer(consumer['consumer']))
                i = i + 1
                t.start()
        # Spawn scheduled-based consumer
        current_time = time.time()
        for consumer in consumers:
            if consumer['schedule'] == 'cron':
                if self.check_schedule(consumer['scheduler'], current_time):
                    print "Spawn " + consumer['consumer']
                    t = threading.Thread(name='consumer-' + str(i), target=lambda: self.spawn_consumer(consumer['consumer']))
                    i = i + 1
                    t.start()
        # Sleep 30s
        time.sleep(30)
        
