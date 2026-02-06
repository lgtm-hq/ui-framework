import type {
  FlowAction,
  FlowBundle,
  FlowEdge,
  FlowState,
  GeneratedTestCase,
  GraphEdge,
  GraphNode,
  Outcome,
} from "../types";

export interface TransitionRow {
  readonly signature: string;
  readonly sourceId: string;
  readonly sourceTitle: string;
  readonly sourcePath: string;
  readonly actionId: string;
  readonly actionLabel: string;
  readonly actionPhrase: string;
  readonly outcome: Outcome;
  readonly targetId: string;
  readonly targetTitle: string;
  readonly targetPath: string;
  readonly details: string;
  readonly screenshotPath: string;
}

export interface CaseFlowSegment {
  readonly signature: string;
  readonly sourceId: string;
  readonly sourceTitle: string;
  readonly sourcePath: string;
  readonly actionId: string;
  readonly actionLabel: string;
  readonly actionPhrase: string;
  readonly targetId: string;
  readonly targetTitle: string;
  readonly targetPath: string;
  readonly outcome: Outcome;
  readonly details: string;
  readonly screenshotPath: string;
  readonly expected?: string;
  readonly actual?: string;
  readonly verdictValue?: string;
}

export interface EnrichedCase {
  readonly testCase: GeneratedTestCase;
  readonly segments: CaseFlowSegment[];
  readonly breadcrumb: string[];
  readonly worst: Outcome;
  readonly outcomes: Set<string>;
}

export const outcomeOrder: Outcome[] = [
  "success",
  "no_change",
  "validation_error",
  "execution_error",
];

export const outcomeColor: Record<string, string> = {
  success: "bg-sage",
  no_change: "bg-warm-gray/50",
  validation_error: "bg-brass",
  execution_error: "bg-sienna",
};

export const outcomeBorderColor: Record<string, string> = {
  success: "border-sage/30",
  no_change: "border-warm-gray/20",
  validation_error: "border-brass/30",
  execution_error: "border-sienna/30",
};

export const outcomeDotColor: Record<string, string> = {
  success: "bg-sage",
  no_change: "bg-warm-gray/60",
  validation_error: "bg-brass",
  execution_error: "bg-sienna",
};

export const outcomeRingColor: Record<string, string> = {
  success: "border-sage",
  no_change: "border-warm-gray/60",
  validation_error: "border-brass",
  execution_error: "border-sienna",
};

export const outcomeEdgeColor: Record<string, string> = {
  success: "#7EA16B",
  no_change: "#B8B0A2",
  validation_error: "#C9A84C",
  execution_error: "#C1666B",
};

export const verdictColor: Record<string, string> = {
  pass: "bg-sage",
  fail: "bg-sienna",
  warn: "bg-brass",
  inconclusive: "bg-warm-gray/50",
};

export const verdictLabel: Record<string, string> = {
  pass: "PASS",
  fail: "FAIL",
  warn: "WARN",
  inconclusive: "N/A",
};

export function buildGraphData(props: {
  readonly states: Record<string, FlowState>;
  readonly edges: FlowEdge[];
  readonly actions: Record<string, FlowAction>;
}): { nodes: GraphNode[]; edges: GraphEdge[] } {
  const nodes: GraphNode[] = Object.values(props.states).map((state) => ({
    id: state.state_id,
    label: state.title || compactPath(state.url),
    depth: state.depth,
    url: state.url,
  }));

  const seen = new Set<string>();
  const graphEdges: GraphEdge[] = [];
  for (const edge of props.edges) {
    const key = `${edge.source_state_id}->${edge.target_state_id}`;
    if (seen.has(key)) continue;
    seen.add(key);
    const action = props.actions[edge.action_id];
    graphEdges.push({
      from: edge.source_state_id,
      to: edge.target_state_id,
      label: action?.label ?? edge.action_id,
      outcome: edge.outcome,
    });
  }

  return { nodes, edges: graphEdges };
}

export function parseFlowBundle(payload: unknown): FlowBundle {
  if (!isObject(payload)) {
    throw new Error("Flow bundle must be an object.");
  }
  if (!isObject(payload.config)) {
    throw new Error('Flow bundle missing "config" object.');
  }
  if (!isObject(payload.states)) {
    throw new Error('Flow bundle missing "states" map.');
  }
  if (!isObject(payload.actions)) {
    throw new Error('Flow bundle missing "actions" map.');
  }
  if (!Array.isArray(payload.edges)) {
    throw new Error('Flow bundle missing "edges" list.');
  }
  const configPayload = payload.config as Record<string, unknown>;
  const config = {
    start_url: typeof configPayload.start_url === "string" ? configPayload.start_url : "",
    max_depth: typeof configPayload.max_depth === "number" ? configPayload.max_depth : 0,
    max_states: typeof configPayload.max_states === "number" ? configPayload.max_states : 0,
    max_actions_per_state:
      typeof configPayload.max_actions_per_state === "number"
        ? configPayload.max_actions_per_state
        : 0,
  };
  return {
    config,
    started_at: typeof payload.started_at === "string" ? payload.started_at : "",
    finished_at: typeof payload.finished_at === "string" ? payload.finished_at : "",
    states: payload.states as FlowBundle["states"],
    actions: payload.actions as FlowBundle["actions"],
    edges: payload.edges as FlowBundle["edges"],
    test_cases: Array.isArray(payload.test_cases)
      ? (payload.test_cases as FlowBundle["test_cases"])
      : [],
  };
}

export function isObject(value: unknown): value is Record<string, unknown> {
  return typeof value === "object" && value !== null && !Array.isArray(value);
}

export function compactPath(url: string): string {
  if (!url) {
    return "unknown-url";
  }
  return url.replace(/^https?:\/\//, "").replace(/\/$/, "");
}

export function describeState(props: {
  readonly state: FlowState | undefined;
  readonly fallbackId: string;
}): { title: string; path: string } {
  if (!props.state) {
    return {
      title: `Unknown page (${props.fallbackId})`,
      path: "unknown-url",
    };
  }
  const safeTitle =
    props.state.title.trim() === "" ? `Untitled page (${props.state.state_id})` : props.state.title;
  return {
    title: safeTitle,
    path: compactPath(props.state.url),
  };
}

export function describeAction(props: {
  readonly action: FlowAction | undefined;
  readonly fallbackId: string;
}): string {
  if (!props.action) {
    return `Execute unknown action (${props.fallbackId})`;
  }
  if (props.action.kind === "click") {
    return `Click "${props.action.label}"`;
  }
  if (props.action.kind === "submit_form") {
    const formName = props.action.metadata?.form_name;
    const scenarioLabel = props.action.metadata?.scenario_label;
    if (formName && scenarioLabel) {
      return `Submit ${formName} (${scenarioLabel})`;
    }
    return `Submit form "${props.action.label}"`;
  }
  return `Execute "${props.action.label}"`;
}

export function buildReadableCaseSteps(props: {
  readonly testCase: GeneratedTestCase;
  readonly actionsById: Record<string, FlowAction>;
  readonly statesById: Record<string, FlowState>;
}): string[] {
  const signatures = props.testCase.edge_signatures ?? [];
  if (signatures.length === 0) {
    return props.testCase.steps;
  }
  const parsed = signatures
    .map((signature) => parseEdgeSignature(signature))
    .filter(
      (value): value is { sourceId: string; actionId: string; targetId: string } => value !== null,
    );
  if (parsed.length === 0) {
    return props.testCase.steps;
  }

  const steps: string[] = [];
  const firstSource = describeState({
    state: props.statesById[parsed[0].sourceId],
    fallbackId: parsed[0].sourceId,
  });
  steps.push(`Start on ${firstSource.title} (${firstSource.path}).`);

  for (const segment of parsed) {
    const actionPhrase = describeAction({
      action: props.actionsById[segment.actionId],
      fallbackId: segment.actionId,
    });
    const target = describeState({
      state: props.statesById[segment.targetId],
      fallbackId: segment.targetId,
    });
    steps.push(`${actionPhrase} and land on ${target.title} (${target.path}).`);
  }
  return steps;
}

export function parseEdgeSignature(
  signature: string,
): { sourceId: string; actionId: string; targetId: string } | null {
  const parts = signature.split("->");
  if (parts.length !== 3) {
    return null;
  }
  return {
    sourceId: parts[0],
    actionId: parts[1],
    targetId: parts[2],
  };
}

export function buildEdgeSignature(props: {
  readonly sourceId: string;
  readonly actionId: string;
  readonly targetId: string;
}): string {
  return `${props.sourceId}->${props.actionId}->${props.targetId}`;
}

export function buildCaseFlowSegments(props: {
  readonly testCase: GeneratedTestCase;
  readonly edgeBySignature: Map<string, FlowEdge>;
  readonly statesById: Record<string, FlowState>;
  readonly actionsById: Record<string, FlowAction>;
}): CaseFlowSegment[] {
  const signatures = props.testCase.edge_signatures ?? [];
  const segments: CaseFlowSegment[] = [];
  for (const signature of signatures) {
    const parsed = parseEdgeSignature(signature);
    if (!parsed) {
      continue;
    }
    const edge = props.edgeBySignature.get(signature);
    const source = describeState({
      state: props.statesById[parsed.sourceId],
      fallbackId: parsed.sourceId,
    });
    const target = describeState({
      state: props.statesById[parsed.targetId],
      fallbackId: parsed.targetId,
    });
    const action = props.actionsById[parsed.actionId];
    const edgeRecord = edge as
      | (FlowEdge & { verdict?: string; expected?: string; actual?: string })
      | undefined;
    segments.push({
      signature,
      sourceId: parsed.sourceId,
      sourceTitle: source.title,
      sourcePath: source.path,
      actionId: parsed.actionId,
      actionLabel: action?.label ?? parsed.actionId,
      actionPhrase: describeAction({
        action,
        fallbackId: parsed.actionId,
      }),
      targetId: parsed.targetId,
      targetTitle: target.title,
      targetPath: target.path,
      outcome: edge?.outcome ?? "no_change",
      details: edge?.message ?? "No details available",
      screenshotPath: edge?.evidence?.screenshot_path ?? "",
      expected: edgeRecord?.expected ?? "",
      actual: edgeRecord?.actual ?? "",
      verdictValue: edgeRecord?.verdict ?? "",
    });
  }
  return segments;
}

export function buildJourneyBreadcrumb(props: {
  readonly testCase: GeneratedTestCase;
  readonly statesById: Record<string, FlowState>;
  readonly actionsById: Record<string, FlowAction>;
}): string[] {
  const signatures = props.testCase.edge_signatures ?? [];
  const parsed = signatures
    .map((sig) => parseEdgeSignature(sig))
    .filter((v): v is { sourceId: string; actionId: string; targetId: string } => v !== null);
  if (parsed.length === 0) {
    return [];
  }

  const crumbs: string[] = [];
  const firstSource = describeState({
    state: props.statesById[parsed[0].sourceId],
    fallbackId: parsed[0].sourceId,
  });
  crumbs.push(firstSource.title);

  for (const segment of parsed) {
    const action = props.actionsById[segment.actionId];
    const target = describeState({
      state: props.statesById[segment.targetId],
      fallbackId: segment.targetId,
    });
    const shortAction = action
      ? action.kind === "click"
        ? action.label
        : action.kind === "submit_form"
          ? `submit ${action.label}`
          : action.label
      : segment.actionId;
    crumbs.push(shortAction);
    crumbs.push(target.title);
  }
  return crumbs;
}

export function worstOutcome(segments: CaseFlowSegment[]): Outcome {
  const priority: Record<string, number> = {
    execution_error: 0,
    validation_error: 1,
    no_change: 2,
    success: 3,
  };
  let worst: Outcome = "success";
  let worstPriority = 3;
  for (const seg of segments) {
    const p = priority[seg.outcome] ?? 1;
    if (p < worstPriority) {
      worstPriority = p;
      worst = seg.outcome;
    }
  }
  return worst;
}
