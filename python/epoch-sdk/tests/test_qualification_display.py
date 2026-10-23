"""Qualifying facts stay visible without changing the answer's output parts."""
from __future__ import annotations

import asyncio
from io import StringIO
from types import SimpleNamespace

import pytest

from epoch_sdk.research import ResearchCompleted
from epoch_sdk.responses import SavedResearchResponse


def result():
    return ResearchCompleted(request_id='request', response=SavedResearchResponse.model_validate({
        'response_id':'answer','request_id':'request','thread_id':'thread',
        'version':1,'published_at_ms':1,'primary_execution_id':'execution','study_id':'study',
        'response_plan':{'plan_id':'rpl_'+'a'*64,'version':1},
        'content':{
            'declarations':[{'name':'answer','type':'text','instructions':'Answer briefly.'}],
            'outputs':[{'name':'answer','type':'text','format':'plain','value':'Computed result.'}],
            'qualifications':[
                {'name':'coverage','description':'Observed <source> coverage',
                 'value':{'observed':7,'expected':8,'unknown':None,'zero':0,'available':False}},
                {'name':'unknown_basis','description':'Unknown basis','value':None},
            ],
        },
    }))


def test_terminal_renders_qualifications_without_dropping_unknowns_or_answer():
    pytest.importorskip('rich')
    pytest.importorskip('prompt_toolkit')
    from rich.console import Console
    from epoch_sdk.terminal import TerminalView
    stream=StringIO()
    view=TerminalView(SimpleNamespace(operation_id='example'),console=Console(file=stream,width=100))
    asyncio.run(view._answer(result()))
    output=stream.getvalue()
    assert 'Observed <source> coverage' in output
    assert '"observed": 7' in output and '"expected": 8' in output
    assert '"unknown": null' in output and '"zero": 0' in output and '"available": false' in output
    assert 'Unknown basis' in output and 'Computed result.' in output


def test_notebook_renders_escaped_basis_and_all_bound_facts(monkeypatch):
    pytest.importorskip('ipywidgets')
    pytest.importorskip('IPython')
    from epoch_sdk import notebook
    displayed=[]
    monkeypatch.setattr(notebook,'display',displayed.append)
    view=notebook.NotebookView(SimpleNamespace(operation_id='example'))
    asyncio.run(view._answer(result()))
    html='\n'.join(str(item.data)for item in displayed if hasattr(item,'data'))
    assert 'Observed &lt;source&gt; coverage' in html
    assert any(getattr(item,'data',None)=={'observed':7,'expected':8,'unknown':None,'zero':0,'available':False}for item in displayed)
    assert 'Unknown basis' in html and '<pre>null</pre>' in html
    assert 'Computed result.' in html
