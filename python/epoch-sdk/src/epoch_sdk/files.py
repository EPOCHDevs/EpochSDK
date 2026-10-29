"""Persistent Files and Space operations over the generated native client.

These methods do not invoke a graph, agent, or model. Resource references come
from Backend; organization never creates a second dataset or study identity.
"""
from __future__ import annotations

import hashlib

from pydantic import TypeAdapter
from stratifyx import AsyncStratifyX
from stratifyx.types import (
    DatasetPreviewPage,
    DatasetReviewRequest,
    DatasetReviewResponse,
    DatasetSourceDescriptor,
    SavedDataset,
    SavedDatasetListPage,
    SpaceFolder,
    SpaceFolderRequest,
    SpacePage,
    SpacePlacementRequest,
    SpaceResourceItem,
    SpaceResourceRef,
    StructuredFileInspection,
    StructuredImportList,
    StructuredImportRequest,
    StructuredImportResult,
    UserFileDescriptor,
    UserFileDetails,
    UserFileListPage,
)

_RESOURCE = TypeAdapter(SpaceResourceRef)
_IMPORT = TypeAdapter(StructuredImportRequest)
_REVIEW = TypeAdapter(DatasetReviewRequest)


class FileClient:
    """Native resource methods shared by EpochClient and AgentToolsClient."""

    backend: AsyncStratifyX

    async def upload_file(self, content: bytes, *, name: str, media_type: str) -> UserFileDescriptor:
        """Upload exact bytes in Backend-selected chunks, then verify completion.

        An uncertain call may be repeated with the same bytes: Backend owns the
        content identity, upload generation and idempotent completion.
        """
        if type(content) is not bytes:
            raise TypeError("File content must be bytes")
        session = await self.backend.user_files.init_file_upload(
            name=name,
            media_type=media_type,
            size_bytes=len(content),
            content_sha256=hashlib.sha256(content).hexdigest(),
            request_options={"max_retries": 0},
        )
        if session.status != "uploading":
            return (await self.file(session.file_ref)).file
        for part in range(session.part_count):
            start = part * session.chunk_size_bytes
            await self.backend.user_files.upload_file_part(
                session.file_ref,
                upload_id=session.upload_id,
                part_index=part,
                request=content[start:start + session.chunk_size_bytes],
                request_options={"max_retries": 0},
            )
        return await self.backend.user_files.complete_file_upload(
            session.file_ref, upload_id=session.upload_id, request_options={"max_retries": 0}
        )

    async def file(self, file_ref: str) -> UserFileDetails:
        return await self.backend.user_files.get_user_file(
            file_ref, request_options={"max_retries": 0}
        )

    async def rename_file(self, file_ref: str, *, name: str) -> UserFileDescriptor:
        return await self.backend.user_files.rename_user_file(
            file_ref, name=name, request_options={"max_retries": 0}
        )

    async def delete_file(self, file_ref: str) -> None:
        await self.backend.user_files.delete_user_file(file_ref, request_options={"max_retries": 0})

    async def delete_dataset(self, dataset_ref: str) -> None:
        await self.backend.user_files.delete_saved_dataset(
            dataset_ref, request_options={"max_retries": 0}
        )

    async def list_files(
        self, *, query: str | None = None, cursor: str | None = None,
        limit: int = 100, include_archived: bool = False,
    ) -> UserFileListPage:
        if type(limit) is not int or not 1 <= limit <= 1000:
            raise ValueError("File page limit must be an integer in 1..1000")
        if type(include_archived) is not bool:
            raise ValueError("include_archived must be a boolean")
        return await self.backend.user_files.list_user_files(
            query=query, cursor=cursor, limit=limit, include_archived=include_archived,
            request_options={"max_retries": 0},
        )

    async def inspect_file(self, file_ref: str, *, format: str) -> StructuredFileInspection:
        return await self.backend.user_files.inspect_structured_file(
            file_ref=file_ref, format=format, request_options={"max_retries": 0}
        )

    async def prepare_dataset(self, request: StructuredImportRequest) -> StructuredImportResult:
        """Prepare a deterministic import; retain request_id for safe retries."""
        value = _IMPORT.validate_python(request)
        return await self.backend.user_files.prepare_structured_import(
            file_ref=value.file_ref, request_id=value.request_id, name=value.name,
            options=value.options, purpose=value.purpose, metadata=value.metadata,
            request_options={"max_retries": 0},
        )

    async def import_drafts(self) -> StructuredImportList:
        return await self.backend.user_files.list_import_drafts(request_options={"max_retries": 0})

    async def review_datasets(self, request: DatasetReviewRequest) -> DatasetReviewResponse:
        """Accept/name or reject each exact draft. Backend owns replay semantics."""
        value = _REVIEW.validate_python(request)
        return await self.backend.user_files.review_structured_import(
            decisions=value.decisions, request_options={"max_retries": 0}
        )

    async def list_datasets(
        self, *, query: str | None = None, cursor: str | None = None, limit: int = 100,
    ) -> SavedDatasetListPage:
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Dataset page limit must be an integer in 1..100")
        return await self.backend.user_files.list_saved_datasets(
            query=query, cursor=cursor, limit=limit, request_options={"max_retries": 0}
        )

    async def dataset(self, dataset_ref: str) -> SavedDataset:
        return await self.backend.user_files.describe_saved_dataset(
            dataset_ref, request_options={"max_retries": 0}
        )

    async def dataset_source(self, source_ref: str) -> DatasetSourceDescriptor:
        return await self.backend.user_files.describe_dataset_source(
            source_ref, request_options={"max_retries": 0}
        )

    async def preview_dataset(
        self, dataset_ref: str, *, offset: int = 0, limit: int = 100,
    ) -> DatasetPreviewPage:
        if type(offset) is not int or offset < 0:
            raise ValueError("Preview offset must be a nonnegative integer")
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Preview limit must be an integer in 1..100")
        return await self.backend.user_files.preview_saved_dataset(
            dataset_ref, offset=offset, limit=limit, request_options={"max_retries": 0}
        )

    async def download_dataset(self, dataset_ref: str) -> bytes:
        """Read a complete verified prepared Arrow IPC file, draft or saved.

        Use pyarrow.ipc.open_file on these bytes. Unlike previews, this includes
        every row and preserves native types, precision, nulls and duplicates.
        """
        data = bytearray()
        async with self.backend.user_files.with_raw_response.download_prepared_dataset(
            dataset_ref, request_options={"max_retries": 0}
        ) as response:
            async for chunk in response.data:
                data.extend(chunk)
        return bytes(data)

    async def create_folder(self, name: str, *, parent_folder_ref: str | None = None) -> SpaceFolder:
        request = SpaceFolderRequest(name=name, parent_folder_ref=parent_folder_ref)
        return await self.backend.space.create_space_folder(
            name=request.name, parent_folder_ref=request.parent_folder_ref,
            request_options={"max_retries": 0},
        )

    async def update_folder(
        self, folder_ref: str, *, name: str, parent_folder_ref: str | None = None,
    ) -> SpaceFolder:
        """Rename/move a folder, preserving its identity and all descendants.

        None parent moves to root; pass the existing parent to rename in place.
        """
        request = SpaceFolderRequest(name=name, parent_folder_ref=parent_folder_ref)
        return await self.backend.space.update_space_folder(
            folder_ref, name=request.name, parent_folder_ref=request.parent_folder_ref,
            request_options={"max_retries": 0},
        )

    async def delete_folder(self, folder_ref: str) -> None:
        """Delete an empty folder. Backend rejects nonempty folders with 409."""
        await self.backend.space.delete_space_folder(folder_ref, request_options={"max_retries": 0})

    async def place_resource(
        self, resource: SpaceResourceRef, *, folder_ref: str | None = None, name: str | None = None,
    ) -> SpaceResourceItem:
        """Place/move a saved resource, optionally setting its Space display name.

        Omitting name preserves any existing display name across the move.
        """
        request = SpacePlacementRequest(
            resource=_RESOURCE.validate_python(resource), folder_ref=folder_ref, name=name,
        )
        return await self.backend.space.place_space_resource(
            resource=request.resource, folder_ref=request.folder_ref, name=request.name,
            request_options={"max_retries": 0},
        )

    async def unplace_resource(self, resource: SpaceResourceRef) -> SpaceResourceRef:
        """Remove organization only; the underlying resource remains saved."""
        request = _RESOURCE.validate_python(resource)
        return await self.backend.space.unplace_space_resource(
            kind=request.kind, ref=request.ref, request_options={"max_retries": 0}
        )

    async def browse_space(
        self, *, folder_ref: str | None = None, recursive: bool = False,
        query: str | None = None, cursor: str | None = None, limit: int = 100,
    ) -> SpacePage:
        """Browse folders and explicitly placed resources in one selected hierarchy."""
        if type(limit) is not int or not 1 <= limit <= 100:
            raise ValueError("Space page limit must be an integer in 1..100")
        if type(recursive) is not bool:
            raise ValueError("recursive must be a boolean")
        return await self.backend.space.browse_space(
            folder_ref=folder_ref, recursive=recursive, query=query, cursor=cursor, limit=limit,
            request_options={"max_retries": 0},
        )
