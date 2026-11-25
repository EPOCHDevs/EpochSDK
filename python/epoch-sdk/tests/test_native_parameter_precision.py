"""The exposed tool schema and wire validator retain native int64 limits."""
from __future__ import annotations

import pytest
from pydantic import ValidationError

from epoch_sdk import RunParameters


def test_native_integer_bounds_remain_exact_in_public_parameter_schema() -> None:
    execution = RunParameters.model_json_schema()["properties"]["execution"]["properties"]
    rules = execution["futures_tick_snapshot"]["properties"]["rules"]["items"]["properties"]
    for field in (execution["cash"], rules["effective_from_ns"], rules["effective_to_ns"]):
        assert field["minimum"] == -(2**63)
        assert field["maximum"] == 2**63 - 1


def test_native_cash_int64_endpoint_survives_validation_and_serialization() -> None:
    value = 2**63 - 1
    parameters = RunParameters.model_validate({"execution": {"cash": value}})
    assert parameters.to_wire() == {"execution": {"cash": value}}


@pytest.mark.parametrize("value", [-(2**63) - 1, 2**63, 9223372036854776000])
def test_native_cash_rejects_values_outside_signed_int64(value: int) -> None:
    with pytest.raises(ValidationError):
        RunParameters.model_validate({"execution": {"cash": value}})


@pytest.mark.parametrize("name", ["period", "execution"])
def test_unset_native_parameter_owners_require_omission_not_null(name: str) -> None:
    assert RunParameters.model_json_schema()["properties"][name]["type"] == "object"
    with pytest.raises(ValidationError):
        RunParameters.model_validate({name: None})
