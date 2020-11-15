import logging
from datetime import datetime
from typing import Generator
import xlsxwriter

from django.conf import settings
from django.db.models import Count, QuerySet
from django.utils import timezone

from bots_management.models import Bot
from keyboards.models import Button
from subscribers.models import Message, Subscriber

logger = logging.getLogger(__name__)


def count_msgs_in_bot(date: datetime, bot: Bot) -> int:
    """
    Returns number of messages for a certain date in certain bot.
    """
    result = Message.objects.filter(
        sender__messengers_bot=bot, created__date=date.date()
    ).aggregate(Count("id"))
    return result["id__count"]


def count_subs_in_bot_in_date(date: datetime, bot: Bot) -> int:
    """
    Returns number of subscribers for a certain date in certain bot.
    """
    result = Subscriber.objects.filter(
        messengers_bot=bot, created__date=date.date(), is_active=True
    ).aggregate(Count("id"))
    return result["id__count"]


def count_inactive_subs_in_bot_in_date(date: datetime, bot: Bot) -> int:
    """
    Returns number of inactive subscribers for a certain date in certain bot.
    """
    result = Subscriber.objects.filter(
        messengers_bot=bot, updated__date=date.date(), is_active=False
    ).aggregate(Count("id"))
    return result["id__count"]


def count_all_subs_in_bot_lte_date(date: datetime, bot: Bot) -> int:
    """
    Returns number of subscribers in certain bot that was created before.
    """
    result = Subscriber.objects.filter(
        messengers_bot=bot, created__date__lte=date.date(), is_active=True
    ).aggregate(Count("id"))
    return result["id__count"]


def get_msgs_statistics(date_from: datetime, date_to: datetime,
                        order: str, bot: Bot) -> QuerySet:
    """
    date_from & date_to is our range(included)

    Returns table with columns ['text', 'num_msgs']
    'text' is our tag, that user writes to get non-menu data.
    """
    msg_texts = Button.objects.filter(
        action__is_menu_action=False
    ).values("text")
    # need to return qs with all available non-menu messages
    # no idea how to improve
    msgs = Message.objects.filter(
        text__in=msg_texts,
        created__range=[date_from, date_to],
        sender__messengers_bot=bot
    ).values('text')
    zero_num_msgs = Button.objects.filter(
        text__in=msg_texts, keyboard__channel=bot.channel
    ).exclude(text__in=msgs).values("text").annotate(
        num_msgs=Count('id')-Count('id')
    )
    msgs = msgs.annotate(num_msgs=Count('id'))

    result_qs = zero_num_msgs.union(msgs).order_by(
        "num_msgs" if order == "asc" else "-num_msgs"
    )
    return result_qs


def create_list_of_dates(date_from: datetime,
                         date_to: datetime) -> Generator[datetime, None, None]:
    """
    Returns generator of dates in range [date_from, date_to].
    """
    for x in range(0, (date_to - date_from).days + 1):
        yield date_from + timezone.timedelta(days=x)


def calculate_bot_efficiency(num_msg_now: int, num_msg_prev: int,
                             subs_num: int) -> float:
    if num_msg_now == num_msg_prev == 0:
        return 0.0
    try:
        result = ((num_msg_now - num_msg_prev) / subs_num) * 100.0
        return round(result, 2)
    except ZeroDivisionError as e:
        logger.info(f"There was 0 subscribers day before ({e})")
        return 100.0


def calculate_subs_efficiency(num_subs_now: int, num_subs_prev: int) -> float:
    if num_subs_now == 0 and num_subs_prev == 0:
        return 0.0
    elif num_subs_prev != 0 and num_subs_now == 0:
        return -num_subs_prev * 100.0
    try:
        result = (num_subs_now / num_subs_prev) * 100.0
        return round(result, 2)
    except ZeroDivisionError as e:
        logger.info(f"There was 0 subscribers day before ({e})")
        return num_subs_now * 100.0


def set_default_datetime() -> tuple:
    """
    Returns date_from as yyyy.mm.dd 00:00:00
    date_to as now
    """
    time_now = timezone.localtime(timezone.now())
    date_from = (time_now - timezone.timedelta(days=1)).replace(
        hour=0, minute=0, second=0
    )
    date_to = time_now
    # TODO datetime(hour=0, ..., tzinfo=Europe/Kiev +03:00)
    return date_from, date_to


def get_previous_dates(date_from: datetime, date_to: datetime) -> tuple:
    """
    Returns same dates' period but previous
    now [2020-09-26; 2020-09-31]
    prev [2020-09-20; 2020-09-25]
    """
    period_difference = date_to - date_from
    prev_date_from = date_from - period_difference
    prev_date_to = date_to - period_difference

    return prev_date_from, prev_date_to


def validate_dates(date_from: str, date_to: str) -> tuple:
    try:
        date_to = timezone.make_aware(timezone.datetime.strptime(
            date_to, settings.DATE_FORMAT
        )).replace(hour=23, minute=59, second=59)
        date_from = timezone.make_aware(timezone.datetime.strptime(
            date_from, settings.DATE_FORMAT
        )).replace(hour=0, minute=0, second=0)
    except (ValueError, TypeError):
        date_from, date_to = set_default_datetime()

    if date_from > date_to:
        date_from, date_to = set_default_datetime()

    return date_from, date_to


def create_efficiency_list_for_messenger(now_period_result: QuerySet,
                                         prev_period_result: QuerySet,
                                         subs_num: int) -> list:
    efficiency_statistics = []
    prev_period_result = list(prev_period_result)
    for message in now_period_result:
        prev_period_msg = list(filter(
            lambda msgs: msgs["text"] == message["text"],
            prev_period_result
        ))
        efficiency = calculate_bot_efficiency(
            num_msg_now=message["num_msgs"],
            num_msg_prev=prev_period_msg[0]['num_msgs'],
            subs_num=subs_num
        )
        data = dict(
            efficiency=efficiency,
            text=message["text"]
        )
        efficiency_statistics.append(data)

    return efficiency_statistics


def get_efficiency_statistics(subs_num: int,
                              now_msgs_statistics: QuerySet,
                              params: dict) -> list:
    prev_date_from, prev_date_to = get_previous_dates(
        date_from=params["date_from"], date_to=params["date_to"]
    )
    params.update(date_from=prev_date_from, date_to=prev_date_to)
    prev_msgs_statistics = get_msgs_statistics(**params)

    efficiency_res = create_efficiency_list_for_messenger(
        now_period_result=now_msgs_statistics,
        prev_period_result=prev_msgs_statistics,
        subs_num=subs_num
    )
    return efficiency_res


def generate_excel(general_data, file_name) -> None:
    workbook = xlsxwriter.Workbook(file_name)
    worksheet = workbook.add_worksheet()

    row, column = 1, 0

    _data_example = general_data[0]
    has_efficiency = _data_example["efficiency"]

    worksheet.write(0, 0, 'Дата')
    worksheet.write(0, 1, 'Загальна кілкість')
    if has_efficiency is not None:
        worksheet.write(0, 2, 'Загальна ефетивність')
    for i, bot in enumerate(_data_example["bots_stats"]):
        if has_efficiency is not None:
            worksheet.write(0, i*2+3, bot["bot"] + " кількість")
            worksheet.write(0, i*2+4, bot["bot"] + " ефективність")
        else:
            worksheet.write(0, i+2, bot["bot"] + " кількість")

    for data_for_date in general_data:
        worksheet.write(row, column, timezone.datetime.fromtimestamp(
            data_for_date["date"]
        ).strftime("%Y-%m-%d"))
        worksheet.write(row, column+1, data_for_date["num"])

        if has_efficiency is not None:
            worksheet.write(row, column+2, data_for_date["efficiency"])

        for i, bot in enumerate(data_for_date["bots_stats"]):
            if has_efficiency is not None:
                worksheet.write(row, i*2+3, bot["num"])
                worksheet.write(row, i*2+4, bot["efficiency"])
            else:
                worksheet.write(row, i+2, bot["num"])

        row += 1

    workbook.close()
