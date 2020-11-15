import json
import os
from datetime import datetime

from django.conf import settings
from django.http import HttpResponse, FileResponse
from django.utils import timezone
from django.views.generic import ListView

from bots_management.mixins import ModeratorRequiredMixin
from bots_management.models import Channel
from bots_management.services import get_channel_by_slug, get_bot_to_channel
from subscribers.services import (
    get_num_of_subs_to_messenger
)
from .forms import BotAnalyticsForm, GeneralAnalyticsForm
from .services import (
    count_msgs_in_bot, get_msgs_statistics, create_list_of_dates,
    calculate_bot_efficiency, validate_dates, get_efficiency_statistics,
    count_subs_in_bot_in_date, calculate_subs_efficiency,
    count_all_subs_in_bot_lte_date, count_inactive_subs_in_bot_in_date,
    generate_excel
)


class GeneralAnalyticsView(ModeratorRequiredMixin, ListView):
    template_name = "analytics/general.html"

    def get_queryset(self):
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = GeneralAnalyticsForm(
            initial={"get_params": self.request.GET}
        )

        channel = get_channel_by_slug(self.kwargs["slug"])
        context["channel"] = channel

        date_from, date_to = validate_dates(
            date_from=self.request.GET.get("date_from"),
            date_to=self.request.GET.get("date_to")
        )
        context["date_from"], context["date_to"] = date_from, date_to
        analytics_type = self.request.GET.get("analytics_type", "bot")

        all_data = self.get_general_statistics(
            date_from=date_from, date_to=date_to,
            channel=channel, analytics_type=analytics_type
        )
        context["bots"] = [bot["bot"] for bot in all_data[0]["bots_stats"]]
        context["all_data"] = json.dumps(all_data)

        return context

    @staticmethod
    def get_general_statistics(date_from: datetime, date_to: datetime,
                               channel: Channel, analytics_type: str) -> list:
        """
        Creates list(generator) of each date in
        period [`date_from`; `date_to`]. Counts messages/subs in this date,
        counts messages/subs in the same date of previous period or day before,
        counts efficiency.
        Returns list of dicts. Dict:
        {"date": certain datetime,
        "num": Number of ALL messages/subs this date(mb in future only
        non-menu messages for bot),
        "efficiency": Counted efficiency,
        "analytics_type": analytics' type
        "bot_stats": [{"num": Number of msgs/subs for current bot,
                      "efficiency": eff,
                      "bot": messenger name}]}
        """
        now_period_dates = create_list_of_dates(date_from, date_to)
        result = []
        for date in now_period_dates:
            prev_date = date - timezone.timedelta(days=1)
            result.append({"date": date.timestamp() + date.utcoffset().seconds,
                           "analytics_type": analytics_type,
                           "bots_stats": []})
            has_efficiency = True
            for bot in channel.bots.all():
                if analytics_type == "bot":
                    num: int = count_msgs_in_bot(date=date,
                                                 bot=bot)
                    prev_num: int = count_msgs_in_bot(date=prev_date,
                                                      bot=bot)
                    subs_num: int = count_all_subs_in_bot_lte_date(date=date,
                                                                   bot=bot)
                    efficiency: float = calculate_bot_efficiency(num,
                                                                 prev_num,
                                                                 subs_num)
                elif analytics_type == "subs_increase":
                    # если нужно будет эффективность за весь период
                    # то prev_date = date -
                    # timedelta(days=(date_to-date_from).days)
                    num: int = count_subs_in_bot_in_date(date=date,
                                                         bot=bot)
                    prev_num: int = count_subs_in_bot_in_date(date=prev_date,
                                                              bot=bot)
                    efficiency: float = calculate_subs_efficiency(num,
                                                                  prev_num)
                elif analytics_type == "subs_decrease":
                    num: int = count_inactive_subs_in_bot_in_date(
                        date=date, bot=bot
                    )
                    prev_num: int = count_inactive_subs_in_bot_in_date(
                        date=prev_date, bot=bot
                    )
                    efficiency: float = calculate_subs_efficiency(num,
                                                                  prev_num)
                else:  # elif analytics_type == "subs"
                    num: int = count_all_subs_in_bot_lte_date(date=date,
                                                              bot=bot)
                    prev_num: count_all_subs_in_bot_lte_date(date=prev_date,
                                                             bot=bot)
                    efficiency = None
                    has_efficiency = False
                bot_data = dict(
                    num=num,
                    efficiency=efficiency,
                    bot=bot.messenger
                )
                result[-1]["bots_stats"].append(bot_data)
            result[-1].update(
                num=sum([bot["num"] for bot in result[-1]["bots_stats"]])
            )
            if has_efficiency:
                result[-1].update(
                    efficiency=sum(
                        [bot["efficiency"] for bot in result[-1]["bots_stats"]]
                    )
                )
            else:
                result[-1].update(efficiency=None)
        return result


class BotAnalyticsView(ModeratorRequiredMixin, ListView):
    template_name = "analytics/bot.html"

    def get_queryset(self):
        return None

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = BotAnalyticsForm(
            initial={"get_params": self.request.GET})

        channel = get_channel_by_slug(self.kwargs["slug"])
        context["channel"] = channel

        analytics_type = self.request.GET.get("analytics_type", "number")
        date_from, date_to = validate_dates(
            date_from=self.request.GET.get("date_from"),
            date_to=self.request.GET.get("date_to")
        )
        context["date_from"], context["date_to"] = date_from, date_to

        messenger = self.request.GET.get("messenger", "viber")
        bot = get_bot_to_channel(channel.slug, messenger)

        order = self.request.GET.get("order", "desc")

        # create QuerySet of {'text': Our non-menu message,
        #                     'num_msgs': Number of messages}
        params = dict(date_from=date_from, date_to=date_to,
                      order=order, bot=bot)
        msgs_statistics = get_msgs_statistics(**params)

        if analytics_type == "number":
            # if just numbers for analytics return our QS
            context["analytics_number"] = msgs_statistics

        elif analytics_type == "efficiency":
            # if efficiency for analytics, need to
            # compare messages' number in the chosen period
            # with previous one. If messages' number was
            # 0 in prev and >0 in now => efficiency = 100.0 %.
            subs_num: int = get_num_of_subs_to_messenger(
                channel=channel, messenger=messenger
            )
            analytics_efficiency = get_efficiency_statistics(
                subs_num=subs_num, now_msgs_statistics=msgs_statistics,
                params=params
            )
            context["analytics_efficiency"] = analytics_efficiency
        return context


def download_analytics(request, slug):
    if request.method == "POST":
        general_data = request.POST.get("general_data")
        if general_data:
            general_data = json.loads(general_data)

            channel_name = '_'.join(slug.split('-'))
            gd_first = general_data[0]
            first_date = timezone.datetime.fromtimestamp(
                gd_first["date"]
            ).strftime(settings.DATE_FORMAT)
            last_date = timezone.datetime.fromtimestamp(
                general_data[-1]["date"]
            ).strftime(settings.DATE_FORMAT)
            file_name = "%s_analytics_%s_%s_%s.xlsx" % (
                gd_first['analytics_type'], channel_name, first_date, last_date
            )

            generate_excel(general_data=general_data, file_name=file_name)
            response = FileResponse(open(file_name, "rb"))
            os.remove(file_name)
            return response
        return HttpResponse(status=404)
    return HttpResponse(status=404)
