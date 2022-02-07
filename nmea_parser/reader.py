from logger import get_logger


class NMEAReader:
    def __init__(self, filepath):
        self.filepath = filepath
        self.logger = get_logger()

    def get_raw_sentences(self):
        """
        Read from file and return a raw list of lines in file
        """
        self.logger.debug(f"Attempting to open file from: {self.filepath}")
        try:
            with open(self.filepath, 'r') as file:
                return file.readlines()
        except FileNotFoundError as e:
            self.logger.error(e)
            exit(1)

    def get_sanitized_sentences(self):
        """
        Sanitize data to omit anything not confirming to expected NMEA 0183 sentence syntax
        """
        sanitized = []
        for line in self.get_raw_sentences():
            start = line.find('$')
            if start == -1:  # Line is not analysable
                self.logger.error(f"Line '{line.strip()}' is not analysable")
                self.logger.error("Omitting line")
                continue
            sanitized.append(line[start:].strip() if start > 0 else line.strip())
        return sanitized

    def get_split_sanitized_sentences(self):
        """
        Get sanitized lines, split by comma
        """
        return [sentence.split(",") for sentence in self.get_sanitized_sentences()]
