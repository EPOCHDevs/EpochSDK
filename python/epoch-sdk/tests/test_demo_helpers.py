"""Example helpers preserve native identity, paging and parameter boundaries."""

from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest
from test_supervisor import job

from epoch_sdk import date_range
from epoch_sdk.research import ExecutionAccepted, ResearchAccepted, ResearchCompleted
from epoch_sdk.responses import ResponseTablePage
from epoch_sdk.supervisor import ChosenExecution, SavedStudy

DEMOS = Path(__file__).resolve().parents[3] / "examples/notebooks/demos"
sys.path.insert(0, str(DEMOS))
import demo_helpers as demos


def completed(review, *, source=None):
    outputs = []
    for declaration in review.request.outputs:
        if declaration.type == "table":
            outputs.append(
                {
                    "name": declaration.name,
                    "type": "table",
                    "schema": [column.to_wire() for column in declaration.columns],
                    "source": {
                        "execution_id": "exec-one",
                        "table": "annual_values",
                        "field_ids": [column.name for column in declaration.columns],
                        "row_count": 3,
                    },
                }
            )
        else:
            assert declaration.type == "text"
            outputs.append(
                {
                    "name": declaration.name,
                    "type": "text",
                    "format": declaration.format,
                    "value": "Synthetic test brief.",
                }
            )
    request_id = "req-variant" if source else "req-base"
    return ResearchCompleted.model_validate(
        {
            "request_id": request_id,
            "operation_id": review.operation_id,
            "reusable_study": {
                "study_id": "study-one",
                "source_execution_id": "exec-one",
                "thread_id": "thread-one",
            },
            "response": {
                "response_id": "rsp-variant" if source else "rsp-base",
                "request_id": request_id,
                "thread_id": "thread-one",
                "study_id": "study-one",
                "primary_execution_id": "exec-one",
                "version": 1,
                "published_at_ms": 1,
                "content": {
                    "declarations": [output.to_wire() for output in review.request.outputs],
                    "outputs": outputs,
                },
            },
        }
    )


def chosen(status="completed"):
    return ChosenExecution.model_validate(
        {
            "execution": job("exec-later", status=status),
            "reusable_study": SavedStudy(
                study_id="study-one", source_execution_id="exec-later"
            ).model_dump(mode="json", exclude_none=True),
        }
    )


def test_task_and_run_preserve_the_existing_body_and_id(monkeypatch):
    monkeypatch.delenv("EPOCH_NOTEBOOK_PREFIX", raising=False)
    review = demos.task("msft_fundamentals")
    canonical = json.loads((DEMOS / "cases/msft_fundamentals.json").read_text())
    assert review.request.to_wire() == canonical
    assert review.operation_id == "notebook-demo-msft_fundamentals-desk-v2-01-research"
    client = SimpleNamespace(run=AsyncMock(return_value=completed(review)))
    asyncio.run(demos.run(client, review, interface="headless"))
    client.run.assert_awaited_once_with(
        review.request, operation_id=review.operation_id, interface="headless"
    )


def test_followup_resolves_exact_source_and_preserves_original_answer():
    base, review = demos.task("msft_fundamentals"), demos.task("msft_fundamentals_plain")
    source, answer = completed(base), completed(review, source=True)
    client = SimpleNamespace(
        research_status=AsyncMock(return_value=source), run=AsyncMock(return_value=answer)
    )
    assert asyncio.run(demos.run(client, review, interface="headless")) == answer
    submitted = client.run.await_args.args[0]
    assert submitted.task == review.request.task and submitted.outputs == review.request.outputs
    for identity in ("study-one", "exec-one", "rsp-base", "thread-one"):
        assert identity in submitted.context[-1]
    assert client.run.await_args.kwargs == {
        "operation_id": review.operation_id,
        "thread_id": "thread-one",
        "interface": "headless",
    }
    assert client.research_status.await_count == 2
    client.run.reset_mock()
    client.research_status.return_value = ResearchAccepted(request_id="base")
    with pytest.raises(RuntimeError, match="Complete the base"):
        asyncio.run(demos.run(client, review))
    client.run.assert_not_awaited()


def test_followup_rejects_rebinding_or_original_pin_change():
    base, review = demos.task("msft_fundamentals"), demos.task("msft_fundamentals_plain")
    source, answer = completed(base), completed(review, source=True)
    wrong = answer.model_copy(
        update={"response": answer.response.model_copy(update={"primary_execution_id": "another"})}
    )
    client = SimpleNamespace(
        research_status=AsyncMock(return_value=source), run=AsyncMock(return_value=wrong)
    )
    with pytest.raises(ValueError, match="exact saved source"):
        asyncio.run(demos.run(client, review))
    client.run.return_value = answer
    changed = source.model_copy(
        update={"response": source.response.model_copy(update={"version": 2})}
    )
    client.research_status.side_effect = [source, changed]
    with pytest.raises(ValueError, match="revision changed"):
        asyncio.run(demos.run(client, review))


def test_read_retrieves_all_rows_and_does_not_repeat_the_narrative(capsys):
    review = demos.task("msft_fundamentals")
    result = completed(review)
    part = result.response.content.outputs[0]
    rows = []
    for index, revenue in enumerate((100.0, 110.0, 121.0)):
        previous = 90.0 if index == 0 else rows[-1][2]
        rows.append(
            [
                f"FY{2023 + index}",
                f"{2023 + index}-06-30",
                revenue,
                revenue / previous - 1,
                20.0,
                20.0 / revenue,
                10.0,
                15.0,
                5.0,
                10.0,
                10.0 / revenue,
                1.5,
            ]
        )
    calls = []

    async def pages(*args, **kwargs):
        calls.append((args, kwargs))
        for offset, values in ((0, rows[:2]), (2, rows[2:])):
            yield ResponseTablePage.model_validate(
                {
                    "response_id": result.response.response_id,
                    "version": 1,
                    "name": part.name,
                    "type": "table",
                    "schema": [column.to_wire() for column in part.columns],
                    "rows": values,
                    "offset": offset,
                    "total_rows": 3,
                    "next_offset": 2 if offset == 0 else None,
                }
            )

    answer = asyncio.run(
        demos.read(SimpleNamespace(iter_response_table=pages), review, result, page_size=2)
    )
    assert len(answer.tables["msft_fundamentals"]) == 3
    assert answer.text["analyst_memo"] == "Synthetic test brief."
    assert calls == [(("rsp-base", "msft_fundamentals"), {"version": 1, "page_size": 2})]
    assert "Synthetic test brief" not in repr(answer)
    assert capsys.readouterr().out == ""


def test_execute_keeps_costs_and_uses_a_distinct_stable_later_period_id():
    review = demos.task("aapl_trend_strategy")
    # Only the source identity is needed here; no strategy output is fabricated.
    result = completed(demos.task("msft_fundamentals")).model_copy(
        update={"operation_id": review.operation_id}
    )
    later = date_range("year to date", as_of="2026-10-16")
    client = SimpleNamespace(execute_saved=AsyncMock(return_value=chosen()))
    for _ in range(2):
        assert (
            asyncio.run(demos.execute(client, review, result, period=later)).execution.id
            == "exec-later"
        )
    for call in client.execute_saved.await_args_list:
        assert call.args == (result.reusable_study,)
        assert call.kwargs["execution"] == review.request.parameters.execution
        assert call.kwargs["period"] == later
        assert call.kwargs["operation_id"] == review.execution_id + "-2026-01-01-2026-10-16"
    asyncio.run(demos.execute(client, review, result))
    assert client.execute_saved.await_args.kwargs["operation_id"] == review.execution_id
    assert review.request.parameters.period.end.isoformat() == "2025-12-31"


def test_execute_observes_only_same_native_operation_and_stops_on_failure(monkeypatch):
    review = demos.task("msft_fundamentals")
    client = SimpleNamespace(
        execute_saved=AsyncMock(
            return_value=ExecutionAccepted(
                request_id="req", operation_id=review.execution_id, execution_id="exec-later"
            )
        ),
        execution_operation=AsyncMock(side_effect=[chosen("running"), chosen()]),
    )
    monkeypatch.setattr(demos.asyncio, "sleep", AsyncMock())
    asyncio.run(demos.execute(client, review, completed(review)))
    assert client.execute_saved.await_count == 1
    assert [call.args for call in client.execution_operation.await_args_list] == [
        (review.execution_id,),
        (review.execution_id,),
    ]
    client.execute_saved.return_value = chosen("failed")
    with pytest.raises(RuntimeError, match="failed"):
        asyncio.run(demos.execute(client, review, completed(review)))


def test_execution_wait_cancellation_never_resubmits_or_cancels_server_work():
    async def scenario():
        review = demos.task("msft_fundamentals")
        client = SimpleNamespace(
            execute_saved=AsyncMock(return_value=chosen("running")), execution_operation=AsyncMock()
        )
        observer = asyncio.create_task(demos.execute(client, review, completed(review)))
        await asyncio.sleep(0)
        observer.cancel()
        with pytest.raises(asyncio.CancelledError):
            await observer
        client.execute_saved.assert_awaited_once()
        client.execution_operation.assert_not_awaited()

    asyncio.run(scenario())


def test_dashboard_link_requires_owned_exact_source_and_actual_content(monkeypatch):
    result = completed(demos.task("msft_fundamentals"))
    schema = SimpleNamespace(charts=[], tables=[], snapshot_cards=[], content=None, context=None)
    owner_read, schema_read = AsyncMock(), AsyncMock(return_value=schema)
    client = SimpleNamespace(
        execution=AsyncMock(return_value=SimpleNamespace(id="exec-one", definition_id="study-one")),
        backend=SimpleNamespace(
            studies_definitions=SimpleNamespace(get_a_study_definition_by_id=owner_read),
            studies_dashboard=SimpleNamespace(
                get_dashboard_schema_chart_specs_table_specs_card_values=schema_read
            ),
        ),
    )
    displays = []
    monkeypatch.setattr(demos, "display", displays.append)
    assert asyncio.run(demos.dashboard(client, result, portal_url="https://portal.example")) is None
    assert displays == []
    schema.charts = ["native chart fixture"]
    assert (
        asyncio.run(demos.dashboard(client, result, portal_url="https://portal.example"))
        == "https://portal.example/dashboard/exec-one"
    )
    assert 'href="https://portal.example/dashboard/exec-one"' in displays[0].data
    owner_read.assert_awaited_with("study-one", request_options={"max_retries": 0})
    schema_read.assert_awaited_with("exec-one", request_options={"max_retries": 0})
    with pytest.raises(ValueError, match="without credentials"):
        asyncio.run(demos.dashboard(client, result, portal_url="javascript:alert(1)"))
    client.execution.return_value.definition_id = "another-study"
    with pytest.raises(ValueError, match="differs"):
        asyncio.run(demos.dashboard(client, result, portal_url="https://portal.example"))
