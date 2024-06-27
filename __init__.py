PLUGIN_NAME = "BroadcastDates"
PLUGIN_AUTHOR = ""
PLUGIN_DESCRIPTION = '''
Add metadata containing broadcast and streaming dates

Began as a fork of https://github.com/avh4/picard-recordingdate
'''
PLUGIN_VERSION = '0.1.0'
PLUGIN_API_VERSIONS = ['2.7']
PLUGIN_LICENSE = "MIT"
PLUGIN_LICENSE_URL = "https://opensource.org/licenses/MIT"

from picard import config, log
from picard.metadata import (register_track_metadata_processor, register_album_metadata_processor)
from picard.plugin import PluginPriority

def process_track(album, metadata, track, release):
    if track.get("recording"):
        # It's a track from a release
        recording = track["recording"]
    else:
        # It's a standalone recording
        recording = track

    dates = []

    def on_result(response, reply, error):
        if not error:
            for item in response['relations']:
                if 'url' in item['target-type']:
                    dates.append(item['begin'])
                if 'broadcast' in item['type']:
                    dates.append(item['begin'])

            if dates:
                metadata['Dates'] = dates

        album._requests -= 1
        album._finalize_loading(error)

    album._requests += 1
    album.tagger.webservice.get(
        config.setting["server_host"],
        config.setting["server_port"],
        "/ws/2/%s/%s" % ('recording', recording["id"]),
        on_result,
        queryargs={"inc": "label-rels+url-rels"},
    )

register_track_metadata_processor(process_track, priority=PluginPriority.HIGH)
