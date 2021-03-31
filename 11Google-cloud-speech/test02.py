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

    # scoped_credentials = credentials.with_scopes(
    #     ['https://www.googleapis.com/auth/cloud-platform'])

    # Instantiates a client
    # [START speech_python_migration_client]
    client = speech.SpeechClient(credentials=credentials)
    # [END speech_python_migration_client]

    # The name of the audio file to transcribe
    file_name = "D:\\YsMl4m6bsBp49W8kuaBtApRFSAgZntNbqv3Hlmdv.mp3"

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


if __name__ == '__main__':
    run_quickstart()
