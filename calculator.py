#!/usr/bin/env python3
import sys
import csv

class Args(object):

    def __init__(self):
        self.args = sys.argv[1:]
        self._config = self.args[self.args.index('-c') + 1]
        self._data = self.args[self.args.index('-d') + 1]
        self._out = self.args[self.args.index('-o') + 1]
    
class Config(object):

    def __init__(self, _config):
        self.config = self._read_config(_config)

    def _read_config(self, _config):
        config = {}
        with open(_config) as f:
            for line in f:
                name, value = line.split('=')
                config[name.strip()] = float((value.strip())
        return config

class UserData(object):

    def __init__(self, _data):
        self.userdata = self._read_users_data(_data)

    def _read_users_data(self, _data):
        userdata = []
        with open(_data) as f:
            for line in f:
                _id, _wage = line.split(',')
                userdata.append((_id, _wage))
        return userdata

class IncomeTaxCalculator(object):

    @classmethod
    def calc_for_all_userdata(cls, _config, _data):
        out = []
        sb_para = _config['YangLao'] + _config['YiLiao'] + _config['ShiYe'] + \
                _config['GongShang'] + _config['ShengYu'] + _config['GongJiJin']
        for u in _data:
            _id = u[0]
            _wage = u[1]
            tax = 0
            sb = _wage * sb_para
            if _wage < _config['JiShuL']:
                sb = _config['JiShuL'] * sb_para
            elif _wage > _config['JiShuH']:
                sb = _config['JiShuH'] * sb_para
            tax_in = _wage - sb - 5000
            if tax_in <= 0:
                tax = 0
            elif tax_in > 0 and tax_in <= 3000:
                tax = tax_in * 0.03
            elif tax_in > 3000 and tax_in <= 12000:
                tax = tax_in * 0.10 - 210
            elif tax_in > 12000 and tax_in <= 25000:
                tax = tax_in * 0.20 - 1410                                
            elif tax_in > 25000 and tax_in <= 35000:
                tax = tax_in * 0.25 - 2660
            elif tax_in > 35000 and tax_in <= 55000:
                tax = tax_in * 0.30 - 4410
            elif tax_in > 55000 and tax_in <= 80000:
                tax = tax_in * 0.35 - 7160
            elif tax_in > 80000:
                tax = tax_in * 0.45 - 15160
            wage_aftax = _wage - sb - tax
            out.append('{},{},{:.2f},{:.2f},{:.2f}'.format(_id, _wage, sb, tax, wage_aftax))
        return out

    @classmethod
    def export(cls, _config, _data, _out, default='csv'):
        result = cls.calc_for_all_userdata(_config, _data)
        with open(_out, 'w') as f:
            writer = csv.writer(f)
            writer.writerows(result)


if __name__ == '__main__':
    args = Args()
    config = Config(args._config)
    userdata = UserData(args._data)
    IncomeTaxCalculator.export(config.config, userdata.userdata, args._out)