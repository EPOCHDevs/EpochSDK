"""Source operations shared by research and MCP clients, over the Python service."""

from epoch_sources.client import AsyncSourcesClient
from epoch_sources.models import (
    ConnectionList,
    CreateConnection,
    PreparedSnapshot,
    PrepareSnapshot,
    ReviewedSnapshot,
    ReviewSnapshot,
    SelectStreams,
    SourceConnection,
    SourceSnapshot,
    SourceSync,
    StartSync,
    StreamList,
    SyncList,
)


class SourceClient:
    source_connections: AsyncSourcesClient | None = None

    def _sources(self) -> AsyncSourcesClient:
        if self.source_connections is None:
            raise ValueError("Configure the source client with the Epoch Python gateway URL")
        return self.source_connections

    async def list_source_connections(self) -> ConnectionList:
        return await self._sources().list()

    async def create_postgres_connection(self, request: CreateConnection) -> SourceConnection:
        return await self._sources().create(request)

    async def source_connection(self, connection_ref: str) -> SourceConnection:
        return await self._sources().get(connection_ref)

    async def delete_source_connection(self, connection_ref: str) -> None:
        await self._sources().delete(connection_ref)

    async def source_streams(self, connection_ref: str) -> StreamList:
        return await self._sources().streams(connection_ref)

    async def select_source_streams(self, connection_ref: str,
                                    request: SelectStreams) -> SourceConnection:
        return await self._sources().select(connection_ref, request)

    async def list_source_syncs(self, connection_ref: str, *, cursor: str | None = None,
                                limit: int = 100) -> SyncList:
        return await self._sources().syncs(connection_ref, cursor=cursor, limit=limit)

    async def start_source_sync(self, connection_ref: str, request: StartSync) -> SourceSync:
        return await self._sources().start(connection_ref, request)

    async def source_sync(self, connection_ref: str, sync_ref: str) -> SourceSync:
        return await self._sources().sync(connection_ref, sync_ref)

    async def cancel_source_sync(self, connection_ref: str, sync_ref: str) -> SourceSync:
        return await self._sources().cancel(connection_ref, sync_ref)

    async def prepare_source_snapshot(self, connection_ref: str, sync_ref: str,
                                      request: PrepareSnapshot) -> PreparedSnapshot:
        return await self._sources().prepare(connection_ref, sync_ref, request)

    async def source_snapshot(self, snapshot_ref: str) -> SourceSnapshot:
        return await self._sources().snapshot(snapshot_ref)

    async def review_source_snapshot(self, snapshot_ref: str,
                                     request: ReviewSnapshot) -> ReviewedSnapshot:
        return await self._sources().review(snapshot_ref, request)
