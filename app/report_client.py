__author__ = 'brighamhausman'
import logging

"""command line client that takes a string argument
    and gathers report requirements based on the value
    of the string argument.
    uses pygal to dump an svg returned by the JSON_reporter
    @see sunglasses notebook page 142 for original sketch"""
import data_manager as dm
from report import Report
import pygal
from yattag import Doc #@see http://www.yattag.org/
from models.card import Card
from models.daily_tt import Daily_TT

class Reportclient:
    __report_data__ = None
    __data_manager = dm.DataManager()

    # externally referenced constants
    # report config props
    CONFIG_REPORT_TYPE = 'report_type'
    CONFIG_REPORT_FORMAT = 'report_format'
    CONFIG_START_DATE = 'start_date'
    CONFIG_END_DATE = 'end_date'
    CONFIG_REPORT_NAME = 'report_name'

    # data keys
    REPORT_TERM_SUIT = 'suit'
    REPORT_TERM_RANK = 'rank'
    REPORT_TERM_REVERSE = 'reversed'
    REPORT_TERM_SUIT_RANK_DATE = 'suit_rank_date'
    REPORT_TERM_DATE = 'date'

    # report types
    REPORT_TITLE_SUITS = 'Count by Suit'
    REPORT_TITLE_REVERSE = 'Count of Reverses'
    REPORT_TITLE_SUIT_RANK_DATE = 'Suits by Rank Over Time'
    REPORT_TYPES = {REPORT_TERM_SUIT: REPORT_TITLE_SUITS,
                    REPORT_TERM_REVERSE: REPORT_TITLE_REVERSE,
                    REPORT_TERM_SUIT_RANK_DATE: REPORT_TITLE_SUIT_RANK_DATE
                    }

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(message)s')
        logging.basicConfig(filename='tarottracker.log', level=logging.DEBUG)
        self.__report_data__ = self.__data_manager.get_cache()

    def get_daily_tt_list(self):
        data = self.get_report_data()
        daily_tt_list = []
        for daily_tt_id in data:
            daily_tt_list.append(data[daily_tt_id])
        # sort objects by date
        daily_tt_list.sort(key=lambda x: x['date'])
        return daily_tt_list

    # returns all members of data_set whose dates
    # are within the range defined by start_date and end_date
    def filter_by_date(self, start_date, end_date, data_set={}):
        from datetime import date
        filtered_data = {}
        sd = None  # start_date
        ed = None  # end_date

        # assumes input format: mm/dd/yyyy
        # returns (yyyy, mm, dd)
        def get_date_vals(date_str):
            dtlst = date_str.split('/')
            return (int(dtlst[2]), int(dtlst[0]), int(dtlst[1]))

        # loop data_set and then by filter dates
        for daily_key in data_set:
            test_date = None
            daily = None
            if self.REPORT_TERM_DATE in data_set[daily_key]:
                daily = data_set[daily_key]
                test_date = daily[self.REPORT_TERM_DATE]

                try:

                    # convert start to datetime
                    if sd is None:
                        (y, m, d) = get_date_vals(start_date)
                        sd = date(y, m, d)

                    # convert end_date to datetime
                    if ed is None:
                        (y, m, d) = get_date_vals(end_date)
                        ed = date(y, m, d)

                    # convert test_date to date time
                    (y, m, d) = get_date_vals(test_date)
                    test_date = date(y, m, d)

                except ValueError as verr:
                    print('date input error: y - {} m - {} d - {}'.format(y, m, d))
                    print('db id: {}'.format(daily_key))
                    print('data model: {}'.format(str(daily)))
                    raise verr

                # true if start_date <= test <= end_date
                if sd <= test_date <= ed:
                    filtered_data[daily_key] = daily

        return filtered_data

    def get_report_data(self):
        return self.__report_data__

    def set_report_data(self, new_data):
        self.__report_data__ = new_data

    # TODO: make these generic: get bar chart, get piechart
    # get chart of a specific number by date
    # specific card by date

    # returns a reference to a generated bar chart in svg format
    def get_suit_chart(self, config):
        data = self.get_report_data()
        chart_title = "Number of each suit for entire date range of the data set"
        if self.CONFIG_START_DATE in config:
            data = self.filter_by_date(config[self.CONFIG_START_DATE], config[self.CONFIG_END_DATE], data)
            chart_title = "Number of each suit for the date range of {} -- {}".format(config[self.CONFIG_START_DATE],
                                                                                      config[self.CONFIG_END_DATE])
        daily_tt_list = []
        for daily_tt_id in data:
            daily_tt_list.append(data[daily_tt_id])
        # sort objects by date
        daily_tt_list.sort(key=lambda x: x['date'])
        suit_count = {}

        # loop the objects and build a count of suits
        for daily_tt in daily_tt_list:
            # get daily_tt date
            daily_date = daily_tt[self.REPORT_TERM_DATE]

            if self.REPORT_TERM_SUIT in daily_tt:
                if daily_tt[self.REPORT_TERM_SUIT] in suit_count:
                    suit_count[daily_tt[self.REPORT_TERM_SUIT]] += 1
                else:
                    suit_count[daily_tt[self.REPORT_TERM_SUIT]] = 1

        # prep data set for the pygal chgart
        chart = pygal.Bar()
        chart.title = chart_title
        for suit in suit_count:
            chart.add(suit, suit_count[suit])
        path_to_chart = 'suit_pie_chart.svg'
        chart.render_to_file(path_to_chart)
        return path_to_chart

    # returns a reference to a pie chart of reverses v upright in svg format
    def get_reverse_chart(self, config):
        path_to_chart = ''
        daily_tt_data = self.get_report_data()
        key_rev = 'reversed'
        key_up = 'upright'
        reversed_count = {key_rev: 0,
                          key_up: 0}

        chart_title = "Number of each suit for entire date range of the data set"
        if self.CONFIG_START_DATE in config:
            daily_tt_data = self.filter_by_date(config[self.CONFIG_START_DATE], config[self.CONFIG_END_DATE],
                                                daily_tt_data)
            chart_title = "Number of each suit for the date range of {} -- {}".format(config[self.CONFIG_START_DATE],
                                                                                      config[self.CONFIG_END_DATE])

        # loop the objects and build a count of reverses
        for daily_tt_key in daily_tt_data:
            testme = daily_tt_data[daily_tt_key]
            if self.REPORT_TERM_REVERSE in testme:
                if testme[self.REPORT_TERM_REVERSE] == 't':
                    reversed_count[key_rev] += 1
                else:
                    reversed_count[key_up] += 1

        # prep data set for the pygal chgart
        chart = pygal.Pie()
        chart.title = chart_title
        for card_align in reversed_count:
            chart.add(card_align, reversed_count[card_align])
        path_to_chart = 'reversed_chart.svg'
        chart.render_to_file(path_to_chart)
        return path_to_chart

    # x is date
    # y is rank
    # group by suit
    def get_suit_rank_date_chart(self, config):
        path_to_chart = 'suit_rank_date_chart'
        daily_tt_data = self.get_report_data()
        chart_title = "Suit/Rank Clustering by Date"
        if self.CONFIG_START_DATE in config:
            daily_tt_data = self.filter_by_date(config[self.CONFIG_START_DATE], config[self.CONFIG_END_DATE],
                                                daily_tt_data)
            chart_title = "Suit and Rank Plot for the Date Range of {} -- {}".format(config[self.CONFIG_START_DATE],
                                                                                     config[self.CONFIG_END_DATE])

        # each suit is a key in a dict, each val is a list containing these as items:
        # (datetime(2013, 1, 2), 300)
        #           (yyyy,m,d), rank
        chart_data_set = {}
        for dtt in daily_tt_data:
            data = daily_tt_data[dtt]

            (month, day, year) = data['date'].split("/")
            # datetime and card obj
            import datetime
            dailytt_date = datetime.date(int(year), int(month), int(day))
            card = Card()
            try:
                card.suit = data[self.REPORT_TERM_SUIT]
                card.rank = int(data[self.REPORT_TERM_RANK])
            except KeyError as kex:
                print('caught bad key {} for data {} with id {}'.format(kex, data, dtt))
            dt = Daily_TT(dailytt_date, card)
            chart_keys = chart_data_set.keys()
            if card.suit in chart_keys:
                chart_data_set[card.suit].append((dt.date, dt.card.rank))
            else:
                chart_data_set[card.suit] = [(dt.date, dt.card.rank)]

        logging.info('suits by date data looks like: {}'.format(str(chart_data_set)))

        return self.get_date_xy_chart(data=chart_data_set)

    def get_date_xy_chart(self, **kwargs):
        default_data = {}
        default_path = 'date_xy_chart.svg'
        data = kwargs.pop('data', default_data)
        path = kwargs.pop('path', default_path)
        datetimechart = pygal.DateTimeLine(stroke=False, dots_size=10)
        for category in data:
            datetimechart.add(category, data[category])

        datetimechart.render_to_file(path)

        return path



    def get_pie_chart(self, config):
        pass

    def get_bar_chart(self):
        pass

    def get_line_chart(self):
        pass

    # takes a report class object and generates a pdf file
    def get_pdf(self, report):
        pass

    def get_html(self, report):
        doc, tag, text = Doc().tagtext()
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('body'):
                with tag('h1'):
                    text(report.title)

                #loop report sections and output
                for section in report.sections:
                    if section.title:
                        with tag('h4'):
                            text(section.title)

                    if section.media:
                        with tag('figure'):
                            doc.stag('embed', type='image/svg+xml', src=section.media)

                    if section.comments:
                        with tag('div'):
                            for comment in section.comments:
                                text(comment)
                                doc.stag('br')



        return doc.getvalue()


    # returns a report object that can be rendered in various formats
    def get_report(self, config={}):

        report = Report()
        report.title = 'no config or report type requested'

        if self.CONFIG_REPORT_TYPE in config:
            report_section = {}
            if config[self.CONFIG_REPORT_TYPE] == self.REPORT_TERM_SUIT:
                report.title = self.REPORT_TITLE_SUITS
                chart = self.get_suit_chart(config)
                report_section['comments'] = ['Distribution of suits.']
                report_section['media'] = chart
                report.make_section(report_section)  # return {'message': message}
            elif config[self.CONFIG_REPORT_TYPE] == self.REPORT_TERM_REVERSE:
                report.title = self.REPORT_TITLE_REVERSE
                rev_chart = self.get_reverse_chart(config)
                report_section['comments'] = ['Distribution of reverse v upright cards.']
                report_section['media'] = rev_chart
                report.make_section(report_section)
            elif config[self.CONFIG_REPORT_TYPE] == self.REPORT_TERM_SUIT_RANK_DATE:
                report.title = self.REPORT_TITLE_SUIT_RANK_DATE
                srd_chart = self.get_suit_rank_date_chart(config)
                report_section['comments'] = ['Distribution of suits over time.']
                report_section['media'] = srd_chart
                report.make_section(report_section)
            else:
                report.title = 'report type ' + config[self.CONFIG_REPORT_TYPE] + ' not found'
        return report


def self_test():
    rc = Reportclient()
    print('testing client exits:\n\t' + str(rc))
    print('testing get_report default:\n\t' + str(rc.get_report()))
    print('testing report of unknown type:\n\t' + str(rc.get_report({rc.CONFIG_REPORT_TYPE: 'balderdash'})))
    print('testing get_report with suit type:\n\t' + str(rc.get_report({rc.CONFIG_REPORT_TYPE: rc.REPORT_TITLE_SUITS})))
    print('testing get_report with reverse type:\n\t' + str(rc.get_report({rc.CONFIG_REPORT_TYPE: rc.REPORT_TITLE_REVERSE})))


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Builds svg, html and pdf reports')
    parser.add_argument('-r', '--report', help='get a report',
                        nargs='?', const='tarot-report')
    parser.add_argument('-t', '--type', help='set report type',
                        action='store')
    parser.add_argument('-f', '--format', help='set format of output, defaults to pdf')
    parser.add_argument('-dr', '--daterange', help="set a date range: 'mm/dd/yyyy|mm/dd/yyyy'")
    parser.add_argument('-s', '--show', help='show report types', action='store_true')

    args = parser.parse_args()
    if args.report:
        if args.type:
            rc = Reportclient()
            # build config obj
            cfg = {}
            cfg[rc.CONFIG_REPORT_TYPE] = args.type
            cfg[rc.CONFIG_REPORT_NAME] = args.report
            if args.daterange:
                (start, end) = args.daterange.split('|')
                cfg[rc.CONFIG_START_DATE] = start
                cfg[rc.CONFIG_END_DATE] = end
            report = rc.get_report(cfg)
            # display outcome
            print('report title: ', report.title)
            report_sections = report.sections
            for section in report_sections:
                print(section)

            # user accessible reports
            if args.format and args.format == 'html':
                # get html report and give path to the index
                html_doc = rc.get_html(report)
                print(html_doc)
                output_html_file = "{}.html".format(args.report)
                with open(output_html_file, 'w') as report_doc:
                    report_doc.write(html_doc)
                print('html printed to {}'.format(output_html_file))
            elif args.format and args.format == 'pdf':
                # get pdf report and path to file
                print('this will show path to a pdf file')

        else:
            print('type of report required, run with -s')

    elif args.show:
        rc = Reportclient()
        types = rc.REPORT_TYPES
        print('available types')
        for type in types:
            print('{} -- {}'.format(type, types[type]))

    else:
        print('use -h for help with this script')
    return 1


if __name__ == '__main__':
    import sys

    sys.exit(main())
