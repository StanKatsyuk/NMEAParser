import re

from logger import get_logger


class NMEAParser:

    def __init__(self, sentence):
        self.sentence = sentence.strip()
        self.logger = get_logger()
        self.talker_type = self.get_talker_type()

    def get_talker_type(self):
        """
        Get "talker" (sat name) from string
        """
        _regex = r"\$(\D{5})"
        name = re.search(_regex, self.sentence)
        if name:
            return name.group(1)
        self.logger.info(f'Unable to parse talker type from sentence: [{self.sentence}]')
        return

    def get_lat_coordinates(self):
        """
        Get latitude coordinates from string
        """
        _regex = r"(\d{2})(\d{2}\.\d+),([NS])"
        lat = re.search(_regex, self.sentence)
        if lat:
            return lat.group(0)

        self.logger.info(f'Unable to parse latitude from sentence: [{self.sentence}]')
        return

    def get_lon_coordinates(self):
        """
        Get longitude coordinates from string
        """
        _regex = r"(\d{3})(\d{2}\.\d+),([EW])"
        lon = re.search(_regex, self.sentence)
        if lon:
            return lon.group(0)

        self.logger.info(f'Unable to parse longitude from sentence: [{self.sentence}]')
        return

    def get_log_timestamp(self):
        """
        Get log timestamp of message, e.g "t=10"
        """
        _regex = r"(\w)=(\d*.?\d),?\s?"
        timestamp = re.search(_regex, self.sentence)
        if timestamp == 0:
            return int(timestamp.group(2))
        elif timestamp:
            return float(timestamp.group(2))

        self.logger.info(f'Unable to parse log timestamp from sentence: [{self.sentence}]')
        return

    def get_sentence_timestamp(self):
        """
        Get NMEA 0183 format timestamp from sentence
        """
        _regex = r"\d{2}\d{2}\d{2}\.\d+"
        talkers_with_timestamps = ['GPRMC', 'GPGGA']

        if self.talker_type in talkers_with_timestamps:  # Check if we expect a timestamp to be present in sentence
            _sentence_timestamp = re.search(_regex, self.sentence)
            if _sentence_timestamp:
                return _sentence_timestamp.group(0)

        self.logger.info(f'Unable to parse if sat: {self.talker_type} is fixed in sentence: [{self.sentence}]')
        return

    def get_is_sat_fixed(self):
        """
        http://aprs.gids.nl/nmea/
        Parse string for a fix (i.e locked) indicator based on talker type:
            GPGGA = 0=invalid; 1=GPS fix; 2=Diff
            GPRMC = A = data valid or V = data not valid
            GPGSA = Field 3 - Mode: 1 = Fix not available; 2 = 2D; 3 = 3D
            GNGSA = Field 3 - Mode: 1 = Fix not available; 2 = 2D; 3 = 3D
        """

        if self.talker_type == "GPGGA":
            lon = self.get_lon_coordinates()  # Use longitude substring to find lock (index(Longitude) + 1)
            if lon and int(self.sentence.split(lon)[1][1]) > 0:
                return True

        if self.talker_type == "GPRMC":
            timestamp = self.get_sentence_timestamp()  # Use timestamp substring to find lock (index(timestamp) + 1)
            if timestamp and self.sentence.split(timestamp)[1][1] == 'A':
                return True

        if self.talker_type == "GPGSA":
            # Use talker type substring to find lock (index(talker) + 2)
            if int(self.sentence.split(self.talker_type)[1][3]) > 1:
                return True

        if self.talker_type == "GNGSA":
            # Use talker type substring to find lock (index(talker) + 2)
            if int(self.sentence.split(self.talker_type)[1][3]) > 1:
                return True

        self.logger.info(f'Unable to parse if sat: {self.talker_type} is fixed in sentence: [{self.sentence}]')
        return False
