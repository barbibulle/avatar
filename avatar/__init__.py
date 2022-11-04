# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Avatar is a scalable multi-platform Bluetooth testing tool capable of running
any Bluetooth test cases virtually and physically.
"""

__version__ = "0.0.1"


import asyncio

from threading import Thread
from mobly import base_test


# Keep running an event loop is a separate thread,
# which is then used to:
#   * Schedule Bumble(s) IO & gRPC server.
#   * Schedule asynchronous tests.
loop = asyncio.new_event_loop()
thread = Thread(target=loop.run_forever, daemon=True)
thread.start()


# Convert an asynchronous test function to a synchronous one by
# executing it's code within our loop
def asynchronous(test):
    def wrapper(self: base_test.BaseTestClass):
        return asyncio.run_coroutine_threadsafe(test(self), loop).result()
    return wrapper
