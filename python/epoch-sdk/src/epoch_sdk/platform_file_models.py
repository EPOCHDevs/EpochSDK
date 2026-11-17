"""Closed bindings for Platform's file contract; native file fields stay native."""

from __future__ import annotations

import json
import re
from importlib.resources import files
from typing import Annotated, Literal

from pydantic import AfterValidator, BaseModel, ConfigDict, Field
from stratifyx.types import UserFileDescriptor

_contract = json.loads(files("epoch_sdk").joinpath("data/platform-files.openapi.json").read_text())
_file_pattern = _contract["components"]["schemas"]["FileDescriptor"]["properties"]["file_ref"][
    "pattern"
]
_original_pattern = _contract["components"]["schemas"]["FileVersion"]["properties"][
    "original_file_ref"
]["pattern"]


def _file_ref(value: str) -> str:
    if not re.fullmatch(_file_pattern, value) or (
        value.startswith("file-version:") and int(value.split(":")[2]) > 2**53 - 1
    ):
        raise ValueError("Provide an exact file reference")
    return value


type FileRef = Annotated[str, Field(pattern=_file_pattern), AfterValidator(_file_ref)]
type OriginalFileRef = Annotated[str, Field(pattern=_original_pattern)]
type Digest = Annotated[str, Field(pattern=r"^[0-9a-f]{64}$")]


class FileModel(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)


class PlatformFileDescriptor(UserFileDescriptor):
    model_config = ConfigDict(extra="forbid", strict=True, frozen=True)
    detected_media_type: str | None = None
    category: Literal["dataset", "document", "other"] | None = None


class StringCell(FileModel):
    type: Literal["string"]
    value: str


class NumberCell(FileModel):
    type: Literal["number"]
    value: str


class BooleanCell(FileModel):
    type: Literal["boolean"]
    value: bool


class NullCell(FileModel):
    type: Literal["null"]


type CellValue = Annotated[
    StringCell | NumberCell | BooleanCell | NullCell, Field(discriminator="type")
]


class CellChange(FileModel):
    row: Annotated[int, Field(ge=0, le=9_999_999)]
    column: Annotated[str, Field(min_length=1, max_length=255)]
    value: CellValue
    sheet: str | None = None


type FileFormat = Literal["csv", "tsv", "jsonl", "parquet", "xlsx"]


class GridOptions(FileModel):
    format: FileFormat
    sheet: str | None = None
    header: bool = True
    delimiter: str = ","
    null_values: list[str] = Field(default_factory=lambda: [""])


class CellEdit(GridOptions):
    kind: Literal["cells"]
    changes: Annotated[list[CellChange], Field(min_length=1, max_length=10_000)]


class TextEdit(FileModel):
    kind: Literal["text"]
    content: str


class FileEditRequest(FileModel):
    schema_version: Literal[1] = 1
    request_id: Annotated[str, Field(min_length=1, max_length=128)]
    base_version: Annotated[int, Field(ge=0)]
    base_content_sha256: Digest
    edit: Annotated[CellEdit | TextEdit, Field(discriminator="kind")]


class CellGridRequest(GridOptions):
    schema_version: Literal[1] = 1
    offset: Annotated[int, Field(ge=0, le=100_000)] = 0
    limit: Annotated[int, Field(ge=1, le=100)] = 100


class FileVersion(FileModel):
    original_file_ref: OriginalFileRef
    version: Annotated[int, Field(ge=0)]
    file: PlatformFileDescriptor
    saved_at: str
    limitations: list[str]


class FileVersionPage(FileModel):
    items: list[FileVersion]
    next_before: Annotated[int, Field(ge=1)] | None = None


class FileEditLimits(FileModel):
    max_file_bytes: int
    max_request_bytes: int
    max_rows: int
    max_columns: int
    max_cells: int
    max_changes: int
    max_expanded_bytes: int


class EditOptionsBase(FileModel):
    schema_version: Literal[1]
    latest: FileVersion
    limits: FileEditLimits


class TextEditOptions(EditOptionsBase):
    kind: Literal["text"]


class CellEditOptions(EditOptionsBase):
    kind: Literal["cells"]
    format: FileFormat
    formula_cells_editable: Literal[False]
    formula_recalculation: Literal[False]


class UnavailableEditOptions(EditOptionsBase):
    kind: Literal[None]  # noqa: PYI061 - Pydantic discriminators require Literal, including null.
    reason: str


type FileEditOptions = Annotated[
    TextEditOptions | CellEditOptions | UnavailableEditOptions, Field(discriminator="kind")
]


class GridColumn(FileModel):
    name: str
    native_type: str
    nullable: bool
    edit_type: Literal["string", "number", "boolean"]


class GridCell(FileModel):
    value: CellValue
    read_only: bool


class FileEditGrid(FileModel):
    schema_version: Literal[1]
    file_ref: FileRef
    source_sha256: Digest
    offset: int
    total_rows: int
    sheets: list[str]
    sheet: str | None = None
    limitations: list[str]
    columns: list[GridColumn]
    rows: list[list[GridCell]]


class PreviewNone(FileModel):
    state: Literal["none"]


class PreviewPending(FileModel):
    state: Literal["pending"]


class PreviewFailed(FileModel):
    state: Literal["failed"]
    reason: str


class PreviewReady(FileModel):
    state: Literal["ready"]
    media_type: Literal["application/pdf"]
    size_bytes: int
    converter_version: str


type FilePreview = Annotated[
    PreviewNone | PreviewPending | PreviewFailed | PreviewReady, Field(discriminator="state")
]


class ImagePreviewPage(FileModel):
    page: int
    width: int
    height: int
    size_bytes: int
    content_sha256: Digest


class ImagePreviewReady(FileModel):
    state: Literal["ready"]
    media_type: Literal["image/png"]
    converter_version: str
    size_bytes: int
    pages: list[ImagePreviewPage]


type FileImagePreview = Annotated[
    PreviewNone | PreviewPending | PreviewFailed | ImagePreviewReady, Field(discriminator="state")
]
