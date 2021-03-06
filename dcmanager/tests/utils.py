# Copyright (c) 2015 Ericsson AB
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#
# Copyright (c) 2017 Wind River Systems, Inc.
#
# The right to copy, distribute, modify, or otherwise make use
# of this software may be licensed only pursuant to the terms
# of an applicable Wind River license agreement.
#

import eventlet
import os
import random
import sqlalchemy
import string
import uuid

from oslo_config import cfg
from oslo_db import options

from dcmanager.common import context
from dcmanager.db import api as db_api


get_engine = db_api.get_engine


class UUIDStub(object):
    def __init__(self, value):
        self.value = value

    def __enter__(self):
        self.uuid4 = uuid.uuid4
        uuid_stub = lambda: self.value
        uuid.uuid4 = uuid_stub

    def __exit__(self, *exc_info):
        uuid.uuid4 = self.uuid4


UUIDs = (UUID1, UUID2, UUID3, UUID4, UUID5) = sorted([str(uuid.uuid4())
                                                     for x in range(5)])


def random_name():
    return ''.join(random.choice(string.ascii_uppercase)
                   for x in range(10))


def setup_dummy_db():
    options.cfg.set_defaults(options.database_opts, sqlite_synchronous=False)
    options.set_defaults(cfg.CONF, connection="sqlite://")
    engine = get_engine()
    db_api.db_sync(engine)
    engine.connect()


def reset_dummy_db():
    engine = get_engine()
    meta = sqlalchemy.MetaData()
    meta.reflect(bind=engine)

    for table in reversed(meta.sorted_tables):
        if table.name == 'migrate_version':
            continue
        engine.execute(table.delete())


def dummy_context(user='test_username', tenant='test_project_id',
                  region_name=None):
    return context.RequestContext.from_dict({
        'auth_token': 'abcd1234',
        'user': user,
        'project': tenant,
        'is_admin': True,
        'region_name': region_name
    })


def wait_until_true(predicate, timeout=60, sleep=1, exception=None):
    with eventlet.timeout.Timeout(timeout, exception):
        while not predicate():
            eventlet.sleep(sleep)


def get_current_cfg():
    f_name = os.environ['CURRENT_CFG_FILE']
    cfg = ''
    with open(f_name) as f:
        cfg = f.readline()
    return cfg


def get_data_filepath(db, table):
    cfg = get_current_cfg()
    return "%s/%s/%s.json" % (cfg, db, table)


def create_subcloud_dict(data_list):
    return {'id': data_list[0],
            'name': data_list[1],
            'description': data_list[2],
            'location': data_list[3],
            'software-version': data_list[4],
            'management-state': data_list[5],
            'availability-status': data_list[6],
            'management-subnet': data_list[7],
            'management-gateway-ip': data_list[8],
            'management-start-ip': data_list[9],
            'management-end-ip': data_list[10],
            'systemcontroller-gateway-ip': data_list[11],
            'audit-fail-count': data_list[12],
            'reserved-1': data_list[13],
            'reserved-2': data_list[14],
            'created-at': data_list[15],
            'updated-at': data_list[16],
            'deleted-at': data_list[17],
            'deleted': data_list[18]}


def create_route_dict(data_list):
    return {'created-at': data_list[0],
            'updated-at': data_list[1],
            'deleted-at': data_list[2],
            'id': data_list[3],
            'uuid': data_list[4],
            'family': data_list[5],
            'network': data_list[6],
            'prefix': data_list[7],
            'gateway': data_list[8],
            'metric': data_list[9],
            'interface-id': data_list[10]}


def create_endpoint_dict(data_list):
    return {'id': data_list[0],
            'legacy_endpoint_id': data_list[1],
            'interface': data_list[2],
            'service_id': data_list[3],
            'url': data_list[4],
            'extra': data_list[5],
            'enabled': data_list[6],
            'region_id': data_list[7]}
