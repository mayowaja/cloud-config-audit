# Cloud Config Audit

Review a saved inventory of storage resources against three example security policies. Every result includes the resource, the setting checked and the action an engineer can take. The tool works offline with Python 3.11+ and the standard library.

## Run the demo

From this directory:

```sh
python audit.py examples/storage.json
python audit.py examples/storage.json --json
python -m unittest discover -s tests -v
```

The sample yields six passes, two failures and one unknown. The customer export store allows public reads and has logging disabled. The backup store has no recorded encryption result. An engineer can investigate that evidence gap separately from a confirmed failure.

## Inputs and decisions

| Rule | Input field | Expected value |
| --- | --- | --- |
| ST-01 | public_read | false |
| ST-02 | encrypted | true |
| ST-03 | access_logging | true |

Supply a JSON array with a unique string `id` per storage resource. Settings accept JSON booleans. A missing or null setting produces an unknown result. Strings such as `"false"` are rejected to prevent ambiguous interpretation. The JSON report includes both expected and observed values so downstream callers can explain the decision.

For a pipeline, run `python audit.py examples/storage.json --gate`. Exit code 0 means every check passed, 1 means at least one check failed or lacks evidence, and 2 means invalid input. The supplied mixed example intentionally exits 1 with this option.

## Scope

This project evaluates three fields in a simplified inventory. It takes the supplied values at face value. It does not query a cloud account, resolve effective permissions or determine whether encryption keys are appropriately managed. All examples are fictional.
