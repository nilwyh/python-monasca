# Copyright 2015 CMU
# Author: Yihan Wang <wangff9@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from monasca.common import alarm_expr_calculator as calculator
from monasca.openstack.common import log
from monasca import tests
import random
import time


LOG = log.getLogger(__name__)


class TestAlarmExprCalculator(tests.BaseTestCase):
    def setUp(self):
        super(TestAlarmExprCalculator, self).setUp()

    def test_calc_value(self):
        self.assertEqual(0, calculator.calc_value('MAX', [0]))
        data = []
        random.seed(time.time())
        for i in range(0, 30, 1):
            data.append(random.uniform(0, 1000))
        self.assertEqual(max(data), calculator.calc_value('MAX', data))
        self.assertEqual(sum(data), calculator.calc_value('SUM', data))
        self.assertEqual(len(data), calculator.calc_value('COUNT', data))

    def test_compare_thresh(self):
        values = [501, 500, 4999]
        op = 'GTE'
        thresh = 500
        self.assertEqual('ALARM',
                         calculator.compare_thresh(values, op, thresh))
        op = 'GT'
        thresh = 500
        self.assertEqual('OK', calculator.compare_thresh(values, op, thresh))
        values = [501, 500, 4999, None]
        op = 'GT'
        thresh = 50
        self.assertEqual('UNDETERMINED',
                         calculator.compare_thresh(values, op, thresh))
        values = [501, 500, 4999, None]
        op = 'GT'
        thresh = 500
        self.assertEqual('OK', calculator.compare_thresh(values, op, thresh))

    def test_calc_logic(self):
        op = 'AND'
        subs = ['ALARM', 'OK', 'ALARM', 'UNDETERMINED']
        self.assertEqual('OK', calculator.calc_logic(op, subs))
        subs = ['ALARM', 'UNDETERMINED', 'ALARM', 'UNDETERMINED']
        self.assertEqual('UNDETERMINED', calculator.calc_logic(op, subs))
        subs = ['ALARM', 'ALARM', 'ALARM']
        self.assertEqual('ALARM', calculator.calc_logic(op, subs))
        op = 'OR'
        subs = ['ALARM', 'OK', 'ALARM', 'UNDETERMINED']
        self.assertEqual('ALARM', calculator.calc_logic(op, subs))
        subs = ['UNDETERMINED', 'OK', 'UNDETERMINED']
        self.assertEqual('UNDETERMINED', calculator.calc_logic(op, subs))
        subs = ['OK', 'OK', 'OK']
        self.assertEqual('OK', calculator.calc_logic(op, subs))
