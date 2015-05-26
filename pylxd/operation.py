# Copyright (c) 2015 Canonical Ltd
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

import datetime

from . import connection

class LXDOperation(object):
    def __init__(self):
        self.connection = connection.LXDConnection()

    def operation_list(self):
        (state, data) = self.connection.get_object('GET', '/1.0/operations')
        return [operation.split('/1.0/operations/')[-1]
                for operation in data['metadata']]

    def operation_show(self, operation):
        (state, data) = self.connection.get_object('GET', '/1.0/operations/%s'
                                                   % operation)
        return {
            'operation_create_time': self.operation_create_time(operation, data.get('metadata')),
            'operation_update_time': self.operation_update_time(operation, data.get('metadata')),
            'operation_status_code': self.operation_status_code(operation, data.get('metadata'))
        }

    def operation_create_time(self, operation, data):
        if data is None:
            (state, data) = self.connection.get_object('GET', '/1.0/Ooperations/%s'
                                                       % operation)
            data = data.get('metadata')
        return datetime.datetime.fromtimestamp(data['created_at']) \
                    .strftime('%Y-%m-%d %H:%M:%S')

    def operation_update_time(self, operation, data):
        if data is None:
            (state, data) = self.connection.get_object('GET', '/1.0/Ooperations/%s'
                                                       % operation)
            data = data.get('metadata')
        return datetime.datetime.fromtimestamp(data['updated_at']) \
                    .strftime('%Y-%m-%d %H:%M:%S')

    def operation_status_code(self, operation, data):
        if data is None:
            (state, data) = self.connection.get_object('GET', '/1.0/Ooperations/%s'
                                                       % operation)
            data = data.get('metadata')
        return data['status']

    def operation_wait(self, operation, status_code, timeout):
        return self.connection.get_status('GET', '/1.0/operations/%s/wait?status_code=%s&timeout=%s'
                                            % (operation, status_code, timeout))

    def operation_delete(self, operation):
        return self.connection.get_status('DELETE', '/1.0/operations/%s'
                                          % operation)

