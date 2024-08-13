from dataclasses import dataclass, field

import pytest
from pytest_mock import MockerFixture

from pycqs import Query, QueryBus, QueryHandler, QueryResult


@dataclass
class FakeQuery(Query):
    input_data: dict[str, str] = field(default_factory=dict)


@dataclass
class FakeQueryResult(QueryResult):
    output_data: dict[str, str]


class FakeQueryHandler(QueryHandler[FakeQuery, FakeQueryResult]):
    async def execute(self, query: FakeQuery) -> FakeQueryResult:
        return FakeQueryResult(output_data=query.input_data)


@pytest.mark.anyio(scope='class')
@pytest.mark.describe(QueryBus.__name__)
class TestQueryBus:
    @pytest.mark.it('Should execute the query handler')
    async def test_execute_handler(self, mocker: MockerFixture) -> None:
        # arrange
        query = FakeQuery()
        query_handler = FakeQueryHandler()
        execute_spy = mocker.spy(query_handler, 'execute')

        # and
        sut = QueryBus()
        sut.register_handler(FakeQuery, query_handler)

        # act
        query_result: FakeQueryResult = await sut.execute(query)

        # assert
        assert isinstance(query_result, FakeQueryResult)

        # and
        assert query_result.output_data == {}

        # and
        execute_spy.assert_awaited_once_with(query)

    @pytest.mark.it(
        'Should raise an error if no handler is defined for a query',
    )
    async def test_execute_raise_value_error(
        self,
        mocker: MockerFixture,
    ) -> None:
        # arrange
        query = FakeQuery()
        query_handler = FakeQueryHandler()
        execute_spy = mocker.spy(query_handler, 'execute')

        # and
        sut = QueryBus()

        # act/assert
        with pytest.raises(ValueError, match='No query handler defined'):
            await sut.execute(query)

        # and
        execute_spy.assert_not_awaited()
