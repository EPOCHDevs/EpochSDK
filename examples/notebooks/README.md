# Try the SDK in a notebook

Open **01_research_and_execute.ipynb** first, then
**02_clarification_and_reconnect.ipynb**. Select the **Epoch SDK (local prototype)**
kernel in the prepared local environment. Both notebooks use the same ordinary
Python SDK as scripts and MCP.

The input is synthetic: 2024 sales = 10 USD and 2025 sales = 15 USD. Expect two
table rows, a JSON row count of 2 and a total of 25. No vendor data is needed.
Research cells call the actual model and native engine; setup and saved reads do
not start research. Notebook outputs are left empty so you can run the sequence.

The first notebook researches, displays the saved table/JSON/text answer, executes
the saved study directly through Backend, and repeats the execution ID to verify
attachment. A prepared execution does not replace the original published answer.

The second notebook asks one explicit confirmation question. It disconnects local
observers, reconnects from a new client, accepts a natural-language answer, and
waits for the same operation's saved response. It also explains which cells to
run after restarting the kernel. It does not add crash recovery or retries.

Operation IDs default to `notebook-demo-research`, `notebook-demo-execute` and
`notebook-demo-clarify`. Re-running identical inputs attaches to the same work.
For a different objective or parameters, choose a new readable operation ID and
update the supplied-case value assertions for your new expected results.
`EPOCH_NOTEBOOK_PREFIX` can give a whole walkthrough a separate namespace.

## Another environment

Use Python 3.12 or later and the matching native StratifyX package from its normal
distribution workflow. This walkthrough was prepared with StratifyX 3.3.0rc4 and
Epoch SDK 0.1.0a2. Install this checkout's `python/epoch-sdk[clients,results]`, plus
`ipykernel` and `jupyterlab`, in your selected environment.

Supply only these client settings to the notebook process:

- `EPOCH_BACKEND_URL`: the intended Backend origin.
- `EPOCH_GRAPH_URL`: the intended EpochAI/LangGraph origin.
- `EPOCH_TOKEN`: your Epoch identity token.

Backend retains vendor configuration and EpochAI retains model configuration.
Do not put credentials in notebook cells or commit notebook output containing
credentials. The prepared local notebook server supplies client settings to its
kernels; a notebook opened independently needs its own environment configured.

Epoch identity tokens expire. If the service returns 401, refresh your Epoch
identity through the normal login flow and create a fresh client; keep the same
operation ID to reconnect. Restarting the local notebook launcher refreshes the
prepared environment's token.
