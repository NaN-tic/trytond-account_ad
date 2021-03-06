# This file is part account_ad module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.tests.test_tryton import ModuleTestCase, with_transaction
from trytond.modules.company.tests import create_company, set_company
from trytond.pool import Pool


def create_chart(company, tax=False):
    pool = Pool()
    AccountTemplate = pool.get('account.account.template')
    ModelData = pool.get('ir.model.data')
    CreateChart = pool.get('account.create_chart', type='wizard')
    Account = pool.get('account.account')

    template = AccountTemplate(ModelData.get_id(
            'account_ad', 'pgc_0'))

    session_id, _, _ = CreateChart.create()
    create_chart = CreateChart(session_id)
    create_chart.account.account_template = template
    create_chart.account.company = company
    create_chart.transition_create_account()
    receivable, = Account.search([
            ('type.receivable', '=', True),
            ('company', '=', company.id),
            ],
        limit=1)
    payable, = Account.search([
            ('code', '=', '400'),
            ('type.payable', '=', True),
            ('company', '=', company.id),
            ],
        limit=1)
    create_chart.properties.company = company
    create_chart.properties.account_receivable = receivable
    create_chart.properties.account_payable = payable
    create_chart.transition_create_properties()


class AccountAdTestCase(ModuleTestCase):
    'Test Account Ad module'
    module = 'account_ad'

    @with_transaction()
    def test_account_chart(self):
        'Test creation of minimal chart of accounts'
        company = create_company()
        with set_company(company):
            create_chart(company, tax=True)

del ModuleTestCase
