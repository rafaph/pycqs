import pytest
from pytest_mock import MockerFixture

from pycqs import Command, CommandBus, CommandHandler


class FakeCommand(Command): ...


class FakeCommandHandler(CommandHandler[FakeCommand]):
    async def execute(self, command: FakeCommand) -> None: ...


@pytest.mark.anyio(scope='class')
@pytest.mark.describe(CommandBus.__name__)
class TestCommandBus:
    @pytest.mark.it('Should execute the command handler')
    async def test_execute_handler(self, mocker: MockerFixture) -> None:
        # arrange
        command = FakeCommand()
        command_handler = FakeCommandHandler()
        execute_spy = mocker.spy(command_handler, 'execute')

        # and
        sut = CommandBus()
        sut.register_handler(FakeCommand, command_handler)

        # act
        await sut.execute(command)

        # assert
        execute_spy.assert_awaited_once_with(command)

    @pytest.mark.it(
        'Should raise an error if no handler is defined for a command',
    )
    async def test_execute_raise_value_error(
        self,
        mocker: MockerFixture,
    ) -> None:
        # arrange
        command = FakeCommand()
        command_handler = FakeCommandHandler()
        execute_spy = mocker.spy(command_handler, 'execute')

        # and
        sut = CommandBus()

        # act
        with pytest.raises(ValueError, match='No command handler defined'):
            await sut.execute(command)

        # assert
        execute_spy.assert_not_awaited()

    @pytest.mark.it('Should not register the same handler twice')
    async def test_not_register_handler_twice(
        self,
        mocker: MockerFixture,
    ) -> None:
        # arrange
        command = FakeCommand()
        command_handler = FakeCommandHandler()
        execute_spy = mocker.spy(command_handler, 'execute')

        # and
        sut = CommandBus()
        sut.register_handler(FakeCommand, command_handler)
        sut.register_handler(FakeCommand, command_handler)

        # act
        await sut.execute(command)

        # assert
        execute_spy.assert_awaited_once_with(command)
