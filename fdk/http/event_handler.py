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

import io
import logging

from fdk import constants
from fdk import customer_code
from fdk import runner

logger = logging.getLogger(__name__)


def event_handle(handle_code: customer_code.Function):
    """
    Performs HTTP request-response procedure
    :param handle_code: customer's code
    :type handle_code: fdk.customer_code.Function
    :return: None
    """
    async def pure_handler(request):
        logger.info("in pure_handler")
        func_response = await runner.handle_request(
            handle_code, constants.HTTPSTREAM,
            headers=dict(request.headers), data=io.BytesIO(request.body))
        logger.info("request execution completed")
        return func_response

    return pure_handler
