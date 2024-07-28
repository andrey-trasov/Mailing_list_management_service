from datetime import datetime
import pytz
from django.conf import settings

from mailings.models import Newsletter
from django.utils import timezone

def send_mailing():
    """
    :return:
    """
    sorted_mailings()








def sorted_mailings():
    time_zone = pytz.timezone(settings.TIME_ZONE)
    time_now = datetime.now(time_zone)
    mailings = Newsletter.objects.filter(status__in=['создана', 'запущена'])
    print(mailings)
    if len(mailings) > 0:
        for mailing in mailings:
            if mailing.status == 'created' and mailing.start_time >= time_now:
                mailing.status = 'запущена'
                mailing.save()
            elif mailing.status == 'запущена' and mailing.end_time >= time_now:
                mailing.status = 'завершена'
                mailing.save()





    print(mailings)
    print()

    # #нынешнее время
    # time_zone = pytz.timezone(settings.TIME_ZONE)
    # now = datetime.now(time_zone)
    # print(now)







    # posts = Newsletter.objects.all()
    # print(posts)
    # print()
    #
    # for i in posts:
    #     i.periodicity = 'раз в месяц'
    #     i.save()
    #
    # print(posts)
    # print()
    # print()
    # print()




    # time_zone = pytz.timezone(settings.TIME_ZONE)
    # now = datetime.now(time_zone)
    # print(now)



    #
    # posts = Newsletter.objects.all()
    #
    # a = posts[0]
    # print(a.start_time)
    # print()
    # print()
    # print()
    # if a.start_time.days >= 7:
    #     print('yes')
    # else:
    #     print('no')

    # mailing.periodicity == 'weekly' and delta.days >= 7
    #
    # print(a.start_time.days += 1)

    # now.days += 1

    # print(timezone)
    # print()
    # print(now + timezone.timedelta(days=1))