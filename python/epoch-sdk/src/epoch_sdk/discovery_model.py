"""Serialization policy shared by generated Platform wire models."""
from pydantic import BaseModel, ConfigDict


class DiscoveryModel(BaseModel):
    # `schema` is a wire name but a reserved Python method; generated fields use
    # schema_ with an alias. All nested wire serialization must keep that alias.
    model_config = ConfigDict(serialize_by_alias=True, extra="forbid", frozen=True,
                              allow_inf_nan=False, revalidate_instances="always")
