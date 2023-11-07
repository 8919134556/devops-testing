import subprocess
import struct

class MediaData:
    def __init__(self, hex_data):
        
        self.raw_data = bytes.fromhex(hex_data.strip())
        self.media_type, self.channel, self.timestamp, self.media_content = self.decode()

    def decode(self):
        media_type, channel, timestamp = struct.unpack('!HHQ', self.raw_data[:12])
        media_content = self.raw_data[12:]
        return media_type, channel, timestamp, media_content

    def video_encoding(self):
        type_byte = self.media_content[4]
        return 'H265' if type_byte in [0x40, 0x42, 0x44, 0x4E, 0x26, 0x02] else 'H264'

    def __str__(self):
        return f"MediaType: {self.media_type}, Channel: {self.channel}, Timestamp: {self.timestamp}"


def convert_g726(input_file, output_format):
    output_file = f"output.{output_format}"
    command = [
        "ffmpeg", "-y", "-f", "g726le", "-code_size", "5", 
        "-i", input_file, "-ar", "8000", "-ac", "1", "-f", output_format, output_file
    ]
    subprocess.run(command)


if __name__ == "__main__":
    SAMPLE_DATA = '48011100e41e00000100010000476a78bd750500000000016742001495a85825900000000168ce3c8'
    #SAMPLE_DATA = '48011100e41e00000100010000476a78bd75'
    media = MediaData(SAMPLE_DATA)
    print(media)
    print(f"Video Encoding: {media.video_encoding()}")

    convert_g726("m072218.g726", "wav")
    convert_g726("m072218.g726", "pcm")
