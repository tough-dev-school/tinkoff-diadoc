from functools import cached_property
import os

from app.models import BankAccount
from app.models import LegalEntity
from diadoc.client import DiadocClient
from diadoc.models import DiadocLegalEntity
from tinkoff_business.client import TinkoffBusinessClient
from tinkoff_to_diadoc.exceptions import TinkoffToDiadocException


class TinkoffToDiadoc:
    def __init__(self) -> None:
        self.tinkoff = TinkoffBusinessClient()
        self.diadoc = DiadocClient()
        self.message_to_acquire = os.getenv("MESSAGE_TO_ACQUIRE_COUNTERAGENT")

    @cached_property
    def my_company(self) -> DiadocLegalEntity:
        tinkoff_entity = self.tinkoff.get_company()
        diadoc_entities = self.diadoc.get_my_organizations()

        for diadoc_entity in diadoc_entities:
            if diadoc_entity.inn_kpp == tinkoff_entity.inn_kpp:
                return diadoc_entity

        raise TinkoffToDiadocException("Did not find in Diadoc's my organizations same company as in Tinkoff")

    @property
    def bank_accounts(self) -> list[BankAccount]:
        return self.tinkoff.get_bank_accounts()

    def get_counteragents(self, my_company: DiadocLegalEntity) -> list[DiadocLegalEntity]:
        return self.diadoc.get_counteragents(my_company.diadoc_id)

    def get_recent_distinct_payers(self, bank_accounts: list[BankAccount], my_company: DiadocLegalEntity) -> set[LegalEntity]:
        payers: list[LegalEntity] = []

        for bank_account in bank_accounts:
            payers += self.tinkoff.get_payers(account_number=bank_account.account_number, exclude_payer_inn=my_company.inn)

        return set(payers)

    def exclude_payers_in_partners(self, payers: set[LegalEntity], counteragents: list[DiadocLegalEntity]) -> list[LegalEntity]:
        partners_already_inn_kpp = {counteragent.inn_kpp for counteragent in counteragents if counteragent.in_partners}

        return [payer for payer in payers if payer.inn_kpp not in partners_already_inn_kpp]

    def get_diadoc_entities_from_payers(self, payers: list[LegalEntity]) -> list[DiadocLegalEntity]:
        diadoc_entities: list[DiadocLegalEntity] = []
        for payer in payers:
            diadoc_entities += self.diadoc.get_organizations_by_inn_kpp(inn=payer.inn, kpp=payer.kpp)

        return diadoc_entities

    def filter_diadoc_entities_to_invite(self, diadoc_entities: list[DiadocLegalEntity], counteragents: list[DiadocLegalEntity]) -> list[DiadocLegalEntity]:
        invite_not_needed_diadoc_ids = {counteragent.diadoc_id for counteragent in counteragents if counteragent.invite_not_needed}

        to_invite: list[DiadocLegalEntity] = []

        for diadoc_entity in diadoc_entities:
            if diadoc_entity.is_active and diadoc_entity.diadoc_id not in invite_not_needed_diadoc_ids:
                to_invite.append(diadoc_entity)

        return to_invite

    def send_invites(self, diadoc_entities: list[DiadocLegalEntity]) -> None:
        for entity in diadoc_entities:
            self.diadoc.acquire_counteragent(diadoc_id=entity.diadoc_id, message=self.message_to_acquire)

    def act(self) -> None:
        counteragents = self.get_counteragents(self.my_company)

        recent_payers = self.get_recent_distinct_payers(self.bank_accounts, self.my_company)
        payers_not_in_partners = self.exclude_payers_in_partners(recent_payers, counteragents)

        entities_from_payers = self.get_diadoc_entities_from_payers(payers_not_in_partners)
        entities_to_invite = self.filter_diadoc_entities_to_invite(entities_from_payers, counteragents)

        self.send_invites(entities_to_invite)
