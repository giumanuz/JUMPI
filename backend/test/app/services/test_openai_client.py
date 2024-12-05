import openai
import pytest
from openai.types.chat import ChatCompletionMessage
from openai.types.chat.chat_completion import ChatCompletion, Choice
from pytest_mock import MockerFixture

# noinspection PyProtectedMember
from app.services.openai_client import OpenaiClient, _get_content_from_response, _get_encoded_user_messages


@pytest.fixture(scope='module', autouse=True)
def setup_config():
    """Setup the configuration for the application."""
    import app.config as config
    config.APP_CONFIG = config.Config(
        OPENAI_API_KEY="",
        ELASTIC_URL="",
    )


@pytest.fixture
def mock_openai_client(mocker: MockerFixture):
    """Fixture to initialize OpenaiClient with mock parameters."""
    mock_openai = mocker.patch.object(openai.OpenAI, '__new__')
    mock_openai.return_value = mocker.Mock()
    client = OpenaiClient(
        system_prompt="Test system prompt",
        max_tokens=100,
        temperature=0.7,
        model="gpt-3.5-turbo"
    )
    return client


def test_get_completion(mocker: MockerFixture, mock_openai_client):
    """Test the `get_completion` method."""
    mock_get_encoded_user_messages = mocker.patch(
        'app.services.openai_client._get_encoded_user_messages',
        return_value=[{"role": "user", "content": "Test message"}]
    )
    mock_chat_completion = mock_openai_client._client.chat.completions.create
    mock_chat_completion.return_value = mocker.Mock(choices=_choices_from_content("Mocked response"))

    result = mock_openai_client.get_completion("Test message")
    assert result == "Mocked response"
    mock_get_encoded_user_messages.assert_called_once_with(["Test message", ])
    mock_chat_completion.assert_called_once()


# noinspection PyUnresolvedReferences
def test_get_user_messages_as_list():
    """Test the static method `_get_user_messages_as_list`."""
    # Test with string input
    assert OpenaiClient._OpenaiClient__get_user_messages_as_list("Message") == ["Message"]

    # Test with list input
    assert OpenaiClient._OpenaiClient__get_user_messages_as_list(["Message1", "Message2"]) == ["Message1", "Message2"]


def test_get_response(mocker: MockerFixture, mock_openai_client):
    """Test the private method `_get_response`."""
    mock_chat_completion = mock_openai_client._client.chat.completions.create
    mock_chat_completion.return_value = mocker.Mock(choices=_choices_from_content("Mocked content"))

    user_messages = ["Test message"]
    response = mock_openai_client._OpenaiClient__get_response(user_messages)
    assert response == mock_chat_completion.return_value
    mock_chat_completion.assert_called_once_with(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Test system prompt"},
            {"role": "user", "content": "Test message"}
        ],
        max_tokens=100,
        temperature=0.7
    )


def test_get_content_from_response():
    """Test the `_get_content_from_response` helper function."""
    mock_response = _chat_completion_from_content("Test content")
    content = _get_content_from_response(mock_response)
    assert content == "Test content"


def _chat_completion_from_content(content: str) -> ChatCompletion:
    """Create a ChatCompletion object from a list of choices."""
    return ChatCompletion(created=0, id="", model="", object="chat.completion",
                          choices=_choices_from_content(content))


def _choices_from_content(content: str) -> list[Choice]:
    """Create a list of Choice objects from a list of content."""
    return [Choice(message=ChatCompletionMessage(content=content, role="assistant"), finish_reason="stop", index=0)]


def test_get_encoded_user_messages():
    """Test the `_get_encoded_user_messages` helper function."""
    user_messages = ["Message 1", "Message 2"]
    encoded = _get_encoded_user_messages(user_messages)
    assert encoded == [
        {"role": "user", "content": "Message 1"},
        {"role": "user", "content": "Message 2"}
    ]
