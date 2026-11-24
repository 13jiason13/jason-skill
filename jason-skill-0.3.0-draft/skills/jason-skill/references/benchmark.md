# Historical benchmark scope

Date: 2026-11-20. Platform: one macOS host and an owned SwiftUI fixture.

Each driver performed read, background action, and application verification in alternating order, three rounds per task. The table reports median driver-loop time. No screenshot was used and foreground focus was preserved in those samples. Cua 0.55.0 used persistent MCP; agent-desktop 1.2.0 used its CLI. Cold startup and model reasoning time were excluded.

| Task | Cua Driver | agent-desktop | Verified result |
| --- | ---: | ---: | --- |
| Button counter | 0.4934 s | 1.5125 s | 3/3 passed each; 3.07× elapsed-time ratio |
| Checkbox | 0.5015 s | 1.6130 s | 3/3 passed each |
| Text input | 1.2535 s | No valid comparable result | Cua type_text passed 3/3; the other attempted background route did not update the model |
| Input, checkbox, save | 1.8146 s | No valid comparable result | Cua saved output passed 3/3 |

These samples do not establish a general speed advantage, model accuracy, subscription savings, or performance on another computer. Built-in Computer Use end-to-end timing and attributable model usage were not measured.

A new comparison should use the same model, task, context conditions, and acceptance criteria. Include reading skill instructions, observations, reasoning, retries, and verification in end-to-end time. Record unknown token or quota measurements as unknown.
