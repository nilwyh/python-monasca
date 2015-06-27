# Copyright 2015 CMU
# Author: Yihan Wang <wangff9@gmail.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.


def calc_value(func, data_list):
    """Calc float values according to 5 functions."""
    ops = {'SUM': sum,
           'AVG': lambda x: sum(x) / len(x),
           'MAX': max,
           'MIN': min,
           'COUNT': len}
    if len(data_list) == 0 or func not in ops:
        return None
    else:
        return ops[func](data_list)


def compare_thresh(values, op, thresh):
    """Check if value from metrics exceeds thresh.

    Only the value in each period meet thresh, the alarm state can be 'ALARM'.

    For example, the alarm definition defines 3 periods, values = [a,b,c].
    If the value in any period doesn't meet thresh,
    then alarm state must be 'OK';
    If some values are None (means no metrics in that period)
    but all other values meet thresh,
    we still don't know if the alarm can be triggered,
    so it's 'UNDETERMINED';
    otherwise, the state can be 'ALARM'
    """

    state = 'OK'
    for value in values:
        if value:
            if op == 'GT' and value <= thresh:
                return state
            elif op == 'LT' and value >= thresh:
                return state
            elif op == 'LTE' and value > thresh:
                return state
            elif op == 'GTE' and value < thresh:
                return state
    state = 'ALARM'
    for value in values:
        if value is None:
            state = 'UNDETERMINED'
    return state


def calc_logic(logic_operator, subs):
    """Calc overall state of an alarm expression.

    'OK' means False;
    'ALARM' means True;
    'UNDETERMINED' means either True or False.
    """
    if logic_operator == 'AND':
        state = 'ALARM'
        for o in subs:
            if o == 'OK':
                return 'OK'
            elif o == 'UNDETERMINED':
                state = 'UNDETERMINED'
        return state
    elif logic_operator == 'OR':
        state = 'OK'
        for o in subs:
            if o == 'ALARM':
                return 'ALARM'
            elif o == 'UNDETERMINED':
                state = 'UNDETERMINED'
        return state
    else:
        return 'UNDETERMINED'
