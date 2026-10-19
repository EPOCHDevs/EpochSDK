"""Deterministic handoff from declared output IDs to native saved artifacts."""

from stratifyx.types.dashboard_schema import DashboardSchema

from .contracts import DomainError, OutputRequest, TableOutputRequest, TextOutputRequest
from .errors import EpochError
from .saved_outputs import (
    JsonBinding,
    OutputBinding,
    SavedOutputManifest,
    TableBinding,
    TextBinding,
)


def output_manifest(
    schema: DashboardSchema,
    *,
    execution_id: str,
    study_id: str,
    declarations: list[OutputRequest],
    category: str = "ALL",
) -> SavedOutputManifest:
    """Bind exact stable IDs emitted for the accepted SDK request.

    Table ids come from native exhibit_id; producer Markdown ids identify text
    and raw JSON. The builder must emit the declared column labels in order.
    Missing or ambiguous IDs never become a title-based or model guess.
    """

    def invalid(message: str) -> EpochError:
        return EpochError(
            DomainError(code="OUTPUT_VALIDATION_FAILED", message=message, retryable=False),
            execution_id=execution_id,
        )

    if not declarations or len({item.name for item in declarations}) != len(declarations):
        raise invalid("Declare each named output exactly once.")
    bindings: list[OutputBinding] = []
    for declaration in declarations:
        if isinstance(declaration, TableOutputRequest):
            matches = [
                item
                for item in schema.tables
                if item.id == declaration.name and item.category == category
            ]
            if len(matches) != 1 or not matches[0].data_id:
                raise invalid(
                    f"Output {declaration.name}: exact native table id is missing or ambiguous."
                )
            table = matches[0]
            if [item.name for item in table.columns] != [item.name for item in declaration.columns]:
                raise invalid(
                    f"Output {declaration.name}: native ordered column labels differ from the accepted declaration."
                )
            bindings.append(
                TableBinding(
                    name=declaration.name,
                    type="table",
                    category=category,
                    table_index=table.index,
                    field_ids=[item.id for item in table.columns],
                )
            )
        else:
            content = schema.content
            if content is None or category not in {
                item.native_category or item.id for item in content.categories
            }:
                raise invalid("The declared producer Markdown category is unavailable.")
            matches = [item for item in content.markdown if item.id == declaration.name]
            if len(matches) != 1:
                raise invalid(
                    f"Output {declaration.name}: exact producer Markdown id is missing or ambiguous."
                )
            if isinstance(declaration, TextOutputRequest):
                bindings.append(
                    TextBinding(
                        name=declaration.name,
                        type="text",
                        category=category,
                        markdown_id=declaration.name,
                        format=declaration.format,
                    )
                )
            else:
                bindings.append(
                    JsonBinding(
                        name=declaration.name,
                        type="json",
                        category=category,
                        markdown_id=declaration.name,
                    )
                )
    return SavedOutputManifest(
        execution_id=execution_id, study_id=study_id, declarations=declarations, bindings=bindings
    )
