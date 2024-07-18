import re


class vin_detector:
    def __init__(self):
        # Define pattern detecting for 17-character VINS (Excluding I, O, and Q)
        self.vin_pattern_17 = re.compile(r'\b[A-HJ-NPR-Z0-9]{17}\b')
        # Same again but for 8 character
        self.vin_pattern_8 = re.compile(r'\b[A-HJ-NPR-Z0-9]{8}\b')
        # Define pattern for detecting 18-character VINS with an extra character
        self.vin_pattern_18 = re.compile(r'\b[A-HJ-NPR-Z0-9]{18}\b')
        # Same again but for 9 character
        self.vin_pattern_9 = re.compile(r'\b[A-HJ-NPR-Z0-9]{9}\b')

    def detect(self, file_content):
        vins = []
        for line in file_content:
            matches_17 = self.vin_pattern_17.findall(line)
            matches_8 = self.vin_pattern_8.findall(line)
            matches_18 = self.vin_pattern_18.findall(line)
            matches_9 = self.vin_pattern_9.findall(line)

            vins.extend(matches_17)
            vins.extend(matches_8)
            for match in matches_18:
                vins.append(match[:-1])  # Remove the last character
            for match in matches_9:
                vins.append(match[:-1])  # Remove the last character
        return vins