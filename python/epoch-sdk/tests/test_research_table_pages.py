from __future__ import annotations

import asyncio

from test_response_paging import clients, example

from epoch_sdk.research import EpochClient


def test_research_client_reads_saved_table_pages_without_running_research():
    async def scenario():
        async with clients() as (supervisor, calls, expected):
            sdk = EpochClient(supervisor)
            saved = await sdk.response(example()["response_id"], version=1)
            page = await sdk.response_table(
                saved.response_id, "results", version=saved.version, offset=25000
            )
            assert len(page.rows) == 3 and page.next_offset is None
            actual = []
            async for part in sdk.iter_response_table(
                saved.response_id, "results", version=saved.version, page_size=5000
            ):
                actual.extend(int(row[1]) for row in part.rows)
            assert actual == expected
            assert all(
                call.url.path.startswith("/api/v1/research/responses/")
                or call.url.path.endswith("/response-tables")
                for call in calls
            )

    asyncio.run(scenario())
