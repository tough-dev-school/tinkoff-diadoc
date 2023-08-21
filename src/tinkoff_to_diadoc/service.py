from functools import cached_property
import os

from dotenv import load_dotenv
import sentry_sdk

from app.models import LegalEntity
from diadoc.client import DiadocClient
from diadoc.exceptions import DiadocHTTPException
from diadoc.models import DiadocPartner
from tinkoff_business.client import TinkoffBusinessClient
from tinkoff_business.exceptions import TinkoffBusinessException
from tinkoff_business.models import TinkoffBankAccount
from tinkoff_to_diadoc.exceptions import TinkoffToDiadocException

load_dotenv()


class TinkoffToDiadoc:
    def __init__(self) -> None:
        self.tinkoff = TinkoffBusinessClient()
        self.diadoc = DiadocClient()
        self.message_to_acquire = os.getenv("MESSAGE_TO_ACQUIRE_COUNTERAGENT")

    @cached_property
    def my_company(self) -> DiadocPartner:
        tinkoff_company = self.tinkoff.get_company()
        diadoc_companies = self.diadoc.get_my_organizations()

        for diadoc_company in diadoc_companies:
            if diadoc_company.inn_kpp == tinkoff_company.inn_kpp:
                return diadoc_company

        raise TinkoffToDiadocException("Did not find in Diadoc's my organizations same company as in Tinkoff")

    @property
    def bank_accounts(self) -> list[TinkoffBankAccount]:
        return self.tinkoff.get_bank_accounts()

    def get_counteragents(self, my_company: DiadocPartner) -> list[DiadocPartner]:
        return self.diadoc.get_counteragents(my_company.diadoc_id)

    def get_recent_distinct_payers(self, bank_accounts: list[TinkoffBankAccount], my_company: DiadocPartner) -> set[LegalEntity]:
        distinct_payers: set[LegalEntity] = set()

        for bank_account in bank_accounts:
            distinct_payers.update(self.tinkoff.get_payers_with_non_empty_inn(account_number=bank_account.account_number))

        distinct_payers.discard(my_company)
        return distinct_payers

    def exclude_payers_in_partners(self, payers: set[LegalEntity], counteragents: list[DiadocPartner]) -> list[LegalEntity]:
        partners_already_inn_kpp = {counteragent.inn_kpp for counteragent in counteragents if counteragent.in_partners}

        return [payer for payer in payers if payer.inn_kpp not in partners_already_inn_kpp]

    def get_distinct_partners_from_payers(self, payers: list[LegalEntity]) -> set[DiadocPartner]:
        distinct_partners: set[DiadocPartner] = set()

        for payer in payers:
            distinct_partners.update(self.diadoc.get_organizations_by_inn_kpp(inn=payer.inn, kpp=payer.kpp))

        return distinct_partners

    def exclude_partners_not_needed_to_invite(self, partners: set[DiadocPartner], counteragents: list[DiadocPartner]) -> list[DiadocPartner]:
        not_needed_to_invite_diadoc_ids = {counteragent.diadoc_id for counteragent in counteragents if counteragent.invite_not_needed}

        to_invite: list[DiadocPartner] = []

        for partner in partners:
            if partner.is_active and partner.diadoc_id not in not_needed_to_invite_diadoc_ids:
                to_invite.append(partner)

        return to_invite

    def send_invites(self, my_company: DiadocPartner, partners: list[DiadocPartner]) -> None:
        for partner in partners:
            self.diadoc.acquire_counteragent(my_company.diadoc_id, partner.diadoc_id, self.message_to_acquire)

    def act(self) -> None:
        try:
            counteragents = self.get_counteragents(self.my_company)

            recent_payers = self.get_recent_distinct_payers(self.bank_accounts, self.my_company)
            payers_not_in_partners = self.exclude_payers_in_partners(recent_payers, counteragents)

            partners_from_payers = self.get_distinct_partners_from_payers(payers_not_in_partners)
            partners_to_invite = self.exclude_partners_not_needed_to_invite(partners_from_payers, counteragents)

            self.send_invites(self.my_company, partners_to_invite)
        except (TinkoffBusinessException, DiadocHTTPException) as exc:
            sentry_sdk.capture_exception(exc)
