import pytest
from unittest.mock import patch

# Mocking the sapperchain and resetquery functions
@pytest.fixture
def mock_sapperchain(mocker):
    return mocker.patch('sapperchain.sapperchain')

@pytest.fixture
def mock_resetquery(mocker):
    return mocker.patch('DeployCodeTemp.resetquery')

# Mocking the GenCode module
@pytest.fixture
def mock_gencode(mocker):
    return mocker.patch('DeployCodeTemp.GenCode.sapper')

@pytest.mark.parametrize(
    "sapper_request, gencode_response, expected_output",
    [
        # Happy path test cases
        (
            {"OpenaiKey": "valid_key"},
            {"query": {"output": "Expected output"}, "initrecord": "init"},
            {"Answer": "Expected output"},
            id="happy_path_valid_key"
        ),
        (
            {"OpenaiKey": "another_valid_key"},
            {"query": {"output": "Another output"}, "initrecord": "init"},
            {"Answer": "Another output"},
            id="happy_path_another_valid_key"
        ),
        # Edge case test cases
        (
            {"OpenaiKey": ""},
            {"query": {"output": ""}, "initrecord": "init"},
            {"Answer": ""},
            id="edge_case_empty_key"
        ),
        (
            {"OpenaiKey": "valid_key"},
            {"query": {"output": None}, "initrecord": "init"},
            {"Answer": None},
            id="edge_case_none_output"
        ),
        # Error case test cases
        (
            {"OpenaiKey": None},
            {"query": {"output": "Error output"}, "initrecord": "init"},
            {"Answer": "Error output"},
            id="error_case_none_key"
        ),
    ]
)
def test_sapper(mock_sapperchain, mock_resetquery, mock_gencode, sapper_request, gencode_response, expected_output):
    # Arrange
    mock_gencode.return_value = gencode_response

    # Act
    result = sapper(sapper_request)

    # Assert
    assert result == expected_output
    mock_sapperchain.assert_called_once_with(sapper_request["OpenaiKey"])
    mock_resetquery.assert_called_once_with(gencode_response["query"], gencode_response["initrecord"])
