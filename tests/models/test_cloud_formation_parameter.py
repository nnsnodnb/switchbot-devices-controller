import pytest

from models import CloudFormationParameter


@pytest.mark.parametrize(
    "value",
    ["SampleValue", None],
    ids=["value is not None", "value is None"],
)
def test_to_dict_value(value) -> None:
    cfn_param = CloudFormationParameter(
        key="SampleKey",
        value=value,
    )

    actual = cfn_param.to_dict()

    assert actual["ParameterKey"] == "SampleKey"
    if value is not None:
        assert len(actual.keys()) == 2
        assert actual["ParameterValue"] == value
    else:
        assert len(actual.keys()) == 1
        assert "ParameterValue" not in actual


@pytest.mark.parametrize(
    "use_previous_value",
    [None, True, False],
    ids=["None", "True", "False"],
)
def test_to_dict(use_previous_value) -> None:
    cfn_param = CloudFormationParameter(
        key="SampleKey",
        value=None,
        use_previous_value=use_previous_value,
    )

    actual = cfn_param.to_dict()

    assert actual["ParameterKey"] == "SampleKey"
    if use_previous_value is not None:
        assert len(actual.keys()) == 2
        assert actual["UsePreviousValue"] == use_previous_value
    else:
        assert len(actual.keys()) == 1
        assert "ParameterValue" not in actual
        assert "UsePreviousValue" not in actual
