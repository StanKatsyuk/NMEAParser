import os
import matplotlib.pyplot as plt

from config import Config
from logger import setup_logger
from reader import NMEAReader
from sentence_parser import NMEAParser


class NMEADataPlotter:
    def __init__(self, filepath):
        self.nmea_file_lines = NMEAReader(filepath)
        self.logger = setup_logger()

    def gather_plot_data(self):
        ttff_by_talker = {}
        talkers_tracked = {}
        talkers = set()
        for sentence in self.nmea_file_lines.get_raw_sentences():
            parsed_sentence = NMEAParser(sentence)
            msg_timestamp = parsed_sentence.get_log_timestamp()
            sat_name = parsed_sentence.get_talker_type()
            locked = parsed_sentence.get_is_sat_fixed()
            talkers.add(sat_name)

            talkers_tracked[msg_timestamp] = len(talkers)

            if locked:
                if sat_name not in ttff_by_talker.values():
                    self.logger.debug(f'{sat_name} fixed at: {msg_timestamp}')
                    ttff_by_talker[msg_timestamp] = sat_name
                else:
                    ttff = {v: k for k, v in ttff_by_talker.items()}[sat_name]  # Perform inverse lookup on ttff data
                    self.logger.debug(f'{sat_name} already fixed {ttff}')
            else:
                self.logger.debug(f'{sat_name} does not appear to be fixed yet in [{sentence.strip()}]')

        return [ttff_by_talker, talkers_tracked]

    def draw_talkers_tracked_bar(self):
        """
        Draw bar graph from satellite data
        """
        import matplotlib.patches as mpatches

        data = self.gather_plot_data()
        self.logger.debug(f'Plot data: {data}')
        ttff_data = data[0]
        talkers_tracked = data[1]

        plt.bar(
            range(len(talkers_tracked)),
            list(talkers_tracked.values()),
            align=Config.bar_alignment,
            width=Config.bar_width
        )
        plt.xticks(range(len(talkers_tracked)), list(talkers_tracked.keys()), fontsize=Config.bar_y_axis_font_size)
        plt.tick_params(axis='x', which=Config.bar_tick_params, labelsize=Config.bar_y_axis_font_size)
        plt.xlabel(Config.bar_x_axis_label)
        plt.ylabel(Config.bar_y_axis_label)
        plt.gca().yaxis.get_major_locator().set_params(integer=True)  # Force Y-axis labels to ints

        handles = [mpatches.Patch(label=f'{v}: {k}') for k, v in ttff_data.items()]

        ax = plt.gcf()
        ax.legend(handles=handles,
                  loc=Config.bar_legend_location,
                  title=Config.bar_legend_title,
                  handlelength=0,
                  handletextpad=0)

        plt.show()

    def draw_ttff_plot(self):
        """
        Draw scatter plot from satellite data
        """
        data = self.gather_plot_data()
        self.logger.debug(f'Plot data dict: {data}')
        ttff_by_talker = data[0]

        for x, y in ttff_by_talker.items():
            plt.scatter(x, y)

        plt.legend(
            ttff_by_talker.keys(),
            fontsize=Config.plot_legend_font_size,
            title=Config.plot_legend_title,
            loc=Config.plot_legend_location,
        )
        plt.show()


if __name__ == "__main__":
    plot = NMEADataPlotter(os.path.join(os.getcwd(), 'resources', 'NMEALog.txt'))
    plot.draw_talkers_tracked_bar()
    # plot.draw_ttff_plot()  # Call optionally if you want to see TTFF scatter plot
