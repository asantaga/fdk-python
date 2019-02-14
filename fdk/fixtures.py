# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import datetime as dt

from fdk import constants
from fdk import headers as hs
from fdk import runner


async def process_response(fn_call_coro):
    new_headers = {}
    resp = await fn_call_coro
    response_data = resp.body()
    response_status = resp.status()
    response_headers = resp.context().GetResponseHeaders()
    for k, v in response_headers.items():
        new_headers.update({
            k.lstrip(constants.FN_HTTP_PREFIX): v
        })
    print(response_headers)
    resp_headers = hs.decap_headers(response_headers)
    del resp_headers[constants.FN_HTTP_STATUS]

    return response_data, response_status, resp_headers


class fake_request(object):

    def __init__(self):
        self.headers = setup_headers()
        self.body = b''


class code(object):

    def __init__(self, fn):
        self.fn = fn

    def handler(self):
        return self.fn


def setup_headers(deadline=None, headers=None,
                  request_url="/", method="POST"):
    new_headers = {}
    if headers is not None:
        for k, v in headers.items():
            new_headers.update({constants.FN_HTTP_PREFIX + k: v})

    if deadline is None:
        now = dt.datetime.now(dt.timezone.utc).astimezone()
        now += dt.timedelta(0, float(constants.DEFAULT_DEADLINE))
        deadline = now.isoformat()

    new_headers.update({
        constants.FN_DEADLINE: deadline,
        constants.FN_HTTP_REQUEST_URL: request_url,
        constants.FN_HTTP_METHOD: method,
    })
    return new_headers


async def setup_fn_call(
        handle_func, request_url="/",
        method="POST", headers=None,
        content=None, deadline=None):

    new_headers = setup_headers(
        deadline=deadline, headers=headers,
        method=method, request_url=request_url
    )

    return process_response(runner.handle_request(
        code(handle_func), constants.HTTPSTREAM,
        headers=new_headers, data=content,
    ))
