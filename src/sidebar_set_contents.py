from anki.stats import CardStats
from anki.lang import _
from aqt import mw

from .card_deck_properties import current_card_deck_properties
from .cardstats import (
    card_stats_as_in_browser,
    mini_card_stats,
    mini_card_stats_with_ord
)
from .deckoptions import long_deck_options, text_for_short_options
from .schedulercomparison import text_for_scheduler_comparison
from .config import gc
from .helper_functions import (
    deck_name_and_source_for_filtered,
    sidebar_style
)
from .revlog import revlogData_mod


def update_contents_of_sidebar(self):
    if not self.shown:
        return
    txt = ""
    card = self.mw.reviewer.card
    if card:
        if gc('show total cards studied today'):
            cutoff = (mw.col.sched.dayCutoff - 86400) * 1000
            sqlstring = f"select count(id) from revlog where id > {cutoff}"
            total_today = mw.col.db.first(sqlstring)[0]
            txt += f'<div style="font-size:85%; text-align:left;"><b>{total_today}</b> cards studied today.</div>'

        p = current_card_deck_properties(card)

        txt += _("<h3>Current Card</h3>")

        if gc('try_to_show_origvmod_scheduler'):
            # txt += _('<h4>Scheduler Comparison</h4>')
            txt += text_for_scheduler_comparison(card, p)
            txt += "<hr>"

        # txt += _("<h4>Deck Options</h4>")
        if gc('deck_options', "brief") == "brief":
            txt += text_for_short_options(card, p)
            txt += "<hr>"

        if gc('show_deck_names', True):
            txt += deck_name_and_source_for_filtered(card, p)

        if gc('deck_options', "brief") == "long":
            txt += long_deck_options(card, p)

        if gc('card_stats') == "detailed":
            txt += card_stats_as_in_browser(card, p)
        elif gc('card_stats') == "brief_with_ord":
            txt += mini_card_stats_with_ord(card, p, True)
        else:
            txt += mini_card_stats(card, p, True)
        txt += "<p>"
        txt += revlogData_mod(self, card, gc('num_of_revs', 3))

    lc = self.mw.reviewer.lastCard()
    if lc:
        txt += "<hr>"
        txt += _("<h3>Last Card</h3>")
        if gc('show_detailed_card_stats_for_current_card'):
            txt += self.mw.col.cardStats(lc)
        else:
            lp = current_card_deck_properties(lc)
            txt += mini_card_stats(lc, lp, False)
        txt += "<p>"
        txt += revlogData_mod(self, lc, gc('num_of_revs', 3))
    if mw.state != 'review':
        txt = _("No Card")
    if self.night_mode_on:
        style = sidebar_style("styling_dark.css")
    else:
        style = sidebar_style("styling.css")
    self.web.setHtml("""
<html>
<head>
<style>
%s
</style>
</head>
<body>
<center>
%s
</center>
</body>
</html>""" % (style, txt))
