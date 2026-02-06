# Lintro Report

## Summary

| Tool         | Issues |
| ------------ | ------ |
| black        | 0      |
| sqlfluff     | 0      |
| markdownlint | 1      |
| clippy       | 0      |
| oxfmt        | 16     |
| prettier     | 2      |
| actionlint   | 0      |
| semgrep      | 0      |
| astro-check  | 0      |
| gitleaks     | 0      |
| mypy         | 0      |
| vue-tsc      | 0      |
| shellcheck   | 0      |
| bandit       | 0      |
| shfmt        | 0      |
| ruff         | 0      |
| oxlint       | 0      |
| yamllint     | 0      |
| rustfmt      | 0      |
| tsc          | 215    |
| hadolint     | 0      |
| taplo        | 0      |
| pydoclint    | 0      |
| cargo_audit  | 0      |

### black (0 issues)

No issues found.

### sqlfluff (0 issues)

No issues found.

### markdownlint (1 issues)

| File      | Line | Code  | Message                                   |
| --------- | ---- | ----- | ----------------------------------------- |
| README.md | 22   | MD032 | Lists should be surrounded by blank lines |

### clippy (0 issues)

No issues found.

### oxfmt (16 issues)

| File                                  | Line | Code   | Message               |
| ------------------------------------- | ---- | ------ | --------------------- |
| eslint.config.js                      | 1    | FORMAT | File is not formatted |
| src/App.tsx                           | 1    | FORMAT | File is not formatted |
| src/components/CommandBar.tsx         | 1    | FORMAT | File is not formatted |
| src/components/JourneyDetailPanel.tsx | 1    | FORMAT | File is not formatted |
| src/components/JourneyList.tsx        | 1    | FORMAT | File is not formatted |
| src/components/JourneyRow.tsx         | 1    | FORMAT | File is not formatted |
| src/components/OutcomePanel.tsx       | 1    | FORMAT | File is not formatted |
| src/components/PageReference.tsx      | 1    | FORMAT | File is not formatted |
| src/components/StateGraph.tsx         | 1    | FORMAT | File is not formatted |
| src/components/StatsSummary.tsx       | 1    | FORMAT | File is not formatted |
| src/components/StepTimeline.tsx       | 1    | FORMAT | File is not formatted |
| src/components/StepTimelineNode.tsx   | 1    | FORMAT | File is not formatted |
| src/lib/flow-utils.ts                 | 1    | FORMAT | File is not formatted |
| src/main.tsx                          | 1    | FORMAT | File is not formatted |
| src/types.ts                          | 1    | FORMAT | File is not formatted |
| vite.config.ts                        | 1    | FORMAT | File is not formatted |

### prettier (2 issues)

| File          | Line | Code   | Message                 |
| ------------- | ---- | ------ | ----------------------- |
| README.md     | 1    | FORMAT | Code style issues found |
| src/index.css | 1    | FORMAT | Code style issues found |

### actionlint (0 issues)

No issues found.

### semgrep (0 issues)

No issues found.

### astro-check (0 issues)

No issues found.

### gitleaks (0 issues)

No issues found.

### mypy (0 issues)

No issues found.

### vue-tsc (0 issues)

No issues found.

### shellcheck (0 issues)

No issues found.

### bandit (0 issues)

No issues found.

### shfmt (0 issues)

No issues found.

### ruff (0 issues)

No issues found.

### oxlint (0 issues)

No issues found.

### yamllint (0 issues)

No issues found.

### rustfmt (0 issues)

No issues found.

### tsc (215 issues)

| File                                  | Line | Code    | Message                                                                                                                                                                  |
| ------------------------------------- | ---- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| src/App.tsx                           | 3    | TS6142  | Module './components/CommandBar' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/CommandBar.tsx', but '--jsx' is not set.                 |
| src/App.tsx                           | 4    | TS6142  | Module './components/JourneyDetailPanel' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyDetailPanel.tsx', but '--jsx' is not set. |
| src/App.tsx                           | 5    | TS6142  | Module './components/JourneyList' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyList.tsx', but '--jsx' is not set.               |
| src/App.tsx                           | 6    | TS6142  | Module './components/OutcomePanel' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/OutcomePanel.tsx', but '--jsx' is not set.             |
| src/App.tsx                           | 7    | TS6142  | Module './components/PageReference' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/PageReference.tsx', but '--jsx' is not set.           |
| src/App.tsx                           | 8    | TS6142  | Module './components/StateGraph' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StateGraph.tsx', but '--jsx' is not set.                 |
| src/App.tsx                           | 9    | TS6142  | Module './components/StatsSummary' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StatsSummary.tsx', but '--jsx' is not set.             |
| src/App.tsx                           | 89   | TS2802  | Type 'Set<string>' can only be iterated through when using the '--downlevelIteration' flag or with a '--target' of 'es2015' or higher.                                   |
| src/App.tsx                           | 242  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 244  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 246  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 259  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 261  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 262  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 272  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 274  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 288  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 290  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 297  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 299  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 300  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 309  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 310  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 315  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/App.tsx                           | 323  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 14   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 21   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 22   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 23   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 24   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 25   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 26   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 27   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 28   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 29   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 30   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 31   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 40   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 41   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 42   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 43   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 48   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 49   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 54   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 59   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 60   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 61   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 69   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 83   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/CommandBar.tsx         | 84   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 6    | TS6142  | Module './StepTimeline' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StepTimeline.tsx', but '--jsx' is not set.                        |
| src/components/JourneyDetailPanel.tsx | 50   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 52   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 53   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 54   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 55   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 65   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 70   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 73   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 76   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 77   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 78   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 81   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 82   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 87   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 97   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 98   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyDetailPanel.tsx | 101  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 4    | TS6142  | Module './JourneyRow' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/JourneyRow.tsx', but '--jsx' is not set.                            |
| src/components/JourneyList.tsx        | 20   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 21   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 22   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 25   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 30   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 32   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 45   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 51   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyList.tsx        | 52   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 18   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 19   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 20   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 21   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 27   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 28   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 29   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 34   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 35   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 45   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 54   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 56   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 57   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 60   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 66   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/JourneyRow.tsx         | 72   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 19   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 20   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 25   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 32   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 33   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 34   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 35   | TS2550  | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later.           |
| src/components/OutcomePanel.tsx       | 37   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 41   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 42   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 51   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 56   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 58   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 70   | TS2550  | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later.           |
| src/components/OutcomePanel.tsx       | 76   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 78   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 96   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/OutcomePanel.tsx       | 105  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 15   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 16   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 19   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 21   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 25   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 28   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 29   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 32   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/PageReference.tsx      | 37   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 26   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 34   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 35   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 36   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 37   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 38   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 39   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 40   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 42   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 43   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 44   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 45   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 177  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 178  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 179  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 182  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 186  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 187  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 188  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 190  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StateGraph.tsx         | 191  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 19   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 20   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 23   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 26   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 27   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 46   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 47   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 50   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 51   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 52   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 53   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 54   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 56   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 57   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 58   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 59   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 60   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 61   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 63   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 64   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 65   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 68   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 69   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StatsSummary.tsx       | 70   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 2    | TS6142  | Module './StepTimelineNode' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/components/StepTimelineNode.tsx', but '--jsx' is not set.                |
| src/components/StepTimeline.tsx       | 11   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 18   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 22   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 30   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 39   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 41   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 43   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 45   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 46   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 48   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 49   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 52   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 55   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimeline.tsx       | 62   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 13   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 20   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 24   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 40   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 42   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 45   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 46   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 49   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 50   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 51   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 54   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 57   | TS2550  | Property 'replaceAll' does not exist on type 'string'. Do you need to change your target library? Try changing the 'lib' compiler option to 'es2021' or later.           |
| src/components/StepTimelineNode.tsx   | 61   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 62   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 63   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 65   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 66   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 69   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 74   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 80   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 82   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 82   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 85   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 85   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 88   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 96   | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 108  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/components/StepTimelineNode.tsx   | 109  | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/main.tsx                          | 4    | TS5097  | An import path can only end with a '.tsx' extension when 'allowImportingTsExtensions' is enabled.                                                                        |
| src/main.tsx                          | 4    | TS6142  | Module './App.tsx' was resolved to '/Users/eiteldagnin/Code/ui-framework/report-ui/src/App.tsx', but '--jsx' is not set.                                                 |
| src/main.tsx                          | 7    | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| src/main.tsx                          | 8    | TS17004 | Cannot use JSX unless the '--jsx' flag is provided.                                                                                                                      |
| vite.config.ts                        | 2    | TS2307  | Cannot find module '@vitejs/plugin-react' or its corresponding type declarations.                                                                                        |
| vite.config.ts                        | 3    | TS2307  | Cannot find module '@tailwindcss/vite' or its corresponding type declarations.                                                                                           |

### hadolint (0 issues)

No issues found.

### taplo (0 issues)

No issues found.

### pydoclint (0 issues)

No issues found.

### cargo_audit (0 issues)

No issues found.
