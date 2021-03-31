#!/usr/bin/env python

# Copyright 2016 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def run_quickstart():
    # [START speech_quickstart]
    import io
    import os

    proxy = 'http://cn-north-1.coia.hcvpc.io:9400'

    os.environ['http_proxy'] = proxy
    os.environ['HTTP_PROXY'] = proxy
    os.environ['https_proxy'] = proxy
    os.environ['HTTPS_PROXY'] = proxy

    # Imports the Google Cloud client library
    # [START speech_python_migration_imports]
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    # [END speech_python_migration_imports]

    from google.oauth2 import service_account
    credentials = service_account.Credentials.from_service_account_file('E:\\15d4072c1e77.json')

    # Instantiates a client
    # [START speech_python_migration_client]
    client = speech.SpeechClient(credentials=credentials)
    # [END speech_python_migration_client]

    # The name of the audio file to transcribe
    file_name_gs = "gs://cloud_storage_01/YsMl4m6bsBp49W8kuaBtApRFSAgZntNbqv3Hlmdv.mp3（副本）"
    file_name = os.path.join(
        os.path.dirname(__file__),
        'resources',
        'audio.raw')

    # Loads the audio into memory
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)

    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US')

    # Detects speech in the audio file
    response = client.recognize(config, audio)

    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))
    # [END speech_quickstart]


def transcribe_streaming(stream_file):
    """Streams transcription of the given audio file."""
    import io
    import os
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    from google.oauth2 import service_account

    # proxies = {
    #     'http': 'socks5://127.0.0.1:1080',
    #     'https': 'socks5://127.0.0.1:1080'
    # }
    # proxy = 'http://127.0.0.1:1082'
    #
    # os.environ['http_proxy'] = proxy
    # os.environ['HTTP_PROXY'] = proxy
    # os.environ['https_proxy'] = proxy
    # os.environ['HTTPS_PROXY'] = proxy

    credentials = service_account.Credentials.from_service_account_file('E:\\15d4072c1e77.json')
    # client = speech.SpeechClient()
    client = speech.SpeechClient(credentials=credentials)

    with io.open(stream_file, 'rb') as audio_file:
        content = audio_file.read()

    # In practice, stream should be a generator yielding chunks of audio data.
    stream = [content]
    requests = (types.StreamingRecognizeRequest(audio_content=chunk)
                for chunk in stream)

    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=44100,
        language_code='en-US')
    streaming_config = types.StreamingRecognitionConfig(config=config)

    # streaming_recognize returns a generator.
    responses = client.streaming_recognize(streaming_config, requests)

    for response in responses:
        # Once the transcription has settled, the first result will contain the
        # is_final result. The other results will be for subsequent portions of
        # the audio.
        for result in response.results:
            print('Finished: {}'.format(result.is_final))
            print('Stability: {}'.format(result.stability))
            alternatives = result.alternatives
            # The alternatives are ordered from most likely to least.
            for alternative in alternatives:
                print('Confidence: {}'.format(alternative.confidence))
                print(u'Transcript: {}'.format(alternative.transcript))


if __name__ == '__main__':
    import os
    # run_quickstart()

    # root_dir = "C:\\Users\\z003nh3w\\Desktop\\CYS01\\"
    # audio_list = os.listdir(root_dir)
    # for audio_index in range(0, len(audio_list)):
    #     need_translate_audio = os.path.join(root_dir, audio_list[audio_index])
    #     transcribe_streaming(need_translate_audio)
    #     print(audio_list[audio_index])

    need_translate_audio = "C:\\Users\\z003nh3w\\Desktop\\CYS01\\20190227-13022401-1-32000.flac"
    transcribe_streaming(need_translate_audio)
