# Document and web dataset review

`prepare_dataset` is the supervisor's shared capability for an owned document or
retained web research. `search_sources` and `read_source` handle discovery and
reading for both. SDK and MCP use that same agent; they do not select a different
set of model tools.

There are two interruptions. The first contains the proposed name, instruction
and exact schema. Only **Build preview** starts preparation; Cancel starts no
extraction. The second contains the immutable native operation, bounded preview,
coverage, limitations and allowed result actions. **Save dataset**, **Save
available data**, **Edit** and **Don't save** are explicit choices. Editing stays
local until another Build preview. No choice is selected automatically.

The envelopes and responses are owned by EpochAI's
`agent_src/presentation/dataset_reviews.py`. Its exported JSON Schema is checked
against `epoch_sdk.dataset_reviews` and copied unchanged into the TypeScript
package. Native operations, requests and previews come from the generated
StratifyX SDK. Do not construct replacement Backend model classes.

For Python applications, a `NeedsInput` result exposes the real interrupt IDs:

```python
from epoch_sdk.dataset_reviews import dataset_response
from epoch_sdk.supervisor import NeedsInput

result = await epoch.run("Prepare reported revenue from my uploaded report",
                         operation_id="report-revenue")
if isinstance(result, NeedsInput):
    item = result.interrupts[0]
    review = item.dataset_review()
    # Display review and collect an explicit choice. A configuration Build uses
    # its reviewed request; a result Save/decline carries no replacement request.
    response = dataset_response(review, selected_action, reviewed_request)
    result = await epoch.resume("report-revenue", {item.id: response})
```

Supply responses for every pending interrupt, keyed by its real ID. Use `Answers`
for ordinary questions and the dataset response models for dataset reviews.
Notebook widgets and terminal commands implement these choices over the same
session. Leaving a widget, terminal or browser keeps the operation waiting.
MCP's existing `epoch_resume` accepts the same closed response union; it adds no
source-specific polling or decision tool.

The SDK confirms native Save/Don't save before delivering the decision to the
agent. The graph then reads the native outcome independently. An unknown Save
blocks competing decisions. If native Save succeeds but graph delivery fails,
reopen the same operation and deliver its confirmed outcome; do not extract or
save again. `continue` delivers a confirmed saved/discarded/expired/stopped result
without a new native mutation. A changed schema/result or foreign owner is not
accepted as the displayed review.

Explicit edits create a new native operation with an exact `replaces` identity.
The prior preview remains retained and its native replacement edge lets another
client reopen the current revision. Editing preserves the Table/JSON/text/scalar
kind and the exact validation that the caller's editor cannot represent.

Direct document/web SDK preparation methods remain available for applications
that own their own form. They return an unsaved native draft. Call
`act_document_preparation` with the exact attempt, review, schema and result
identity to save or decline. Manual operations need no graph or conversation.
Preparation results expose `dataset_ref` only after native Save succeeds.

The default same-agent MCP also inspects pending data through `epoch_read`:
use `draft_ref` from the review with `offset` and `page_size` (up to 100) for
Table continuation. For complete JSON/text/scalar or Arrow bytes, supply
`full_content=true` and the review draft descriptor's `content_sha256` as
`expected_sha256`, then read the returned typed resource. Every resource read
rechecks native authorization, content format and the digest. An earlier link
never grants access after expiry or owner denial. This read path saves nothing
and starts no provider work. Python applications use the same client's
`preview_dataset` and `download_dataset` methods; TypeScript callers retain their
versioned native client's preview/download routes.
