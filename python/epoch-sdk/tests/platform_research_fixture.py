"""Compose separate native/lifecycle clients over a fixture's shared HTTP server.

A real front door routes the same paths to distinct owners. The native HTTP
mock stays reused here so existing workflow cases retain their fixtures; route
ownership itself is covered by test_research_operations.py and Platform tests.
"""
from epoch_sdk.research_operations import ResearchOperationsClient
from epoch_sdk.supervisor import SupervisorClient


def supervisor_with_research(graph, backend, **options):
    wrapper = backend._client_wrapper
    header = wrapper.get_headers().get('Authorization', '')
    operations = ResearchOperationsClient(wrapper.get_base_url(), header.removeprefix('Bearer ') or None,
        http=wrapper.httpx_client.httpx_client)
    return SupervisorClient(graph, backend, research_operations=operations, **options)
