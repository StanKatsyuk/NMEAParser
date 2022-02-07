from os import path, mkdir
from dataclasses import dataclass
from datetime import datetime
from packaging import version
from logging import DEBUG


@dataclass
class Config:
    # Project metadata
    project_name: str = "NMEA_Parser"
    author: str = "stankatsyuk@gmail.com"
    version: version = "1.0"

    # Logging config
    log_dir: path = path.join(path.curdir, "logs")
    log_format: str = '[%(asctime)s] - %(levelname)s - %(filename)s: %(funcName)s :%(lineno)d - %(message)s'
    log_filepath: path = path.join(log_dir, datetime.now().strftime('%Y_%m_%d_%H_%M_%S.log'))
    logging_level = DEBUG

    # NMEADataPlotter.draw_ttff_plot() config
    plot_legend_font_size: str = "medium"
    plot_legend_title: str = "TTFF"
    plot_legend_location: str = "best"
    plot_x_axis_label: str = "Time"
    plot_y_axis_label: str = "Talker Count"

    # NMEADataPlotter.draw_talkers_tracked_bar() config
    bar_width: float = 0.5
    bar_alignment: str = "center"
    bar_y_axis_font_size: str = "x-small"
    bar_legend_location: str = "upper left"
    bar_x_axis_label: str = "Time"
    bar_y_axis_label: str = "Talkers Tracked"
    bar_legend_title: str = "TTFF"
    bar_tick_params: str = "major"
