export type Outcome = "success" | "no_change" | "validation_error" | "execution_error" | string;

export interface ExplorerConfig {
  readonly start_url: string;
  readonly max_depth: number;
  readonly max_states: number;
  readonly max_actions_per_state: number;
}

export interface FlowState {
  readonly state_id: string;
  readonly depth: number;
  readonly title: string;
  readonly url: string;
  readonly signals: string[];
}

export interface FlowAction {
  readonly action_id: string;
  readonly kind: string;
  readonly label: string;
  readonly selector: string;
  readonly metadata?: Record<string, string>;
}

export interface FlowEdge {
  readonly source_state_id: string;
  readonly target_state_id: string;
  readonly action_id: string;
  readonly outcome: Outcome;
  readonly message: string;
  readonly evidence?: Record<string, string>;
  readonly verdict?: VerdictValue;
  readonly verdict_reason?: string;
  readonly expected?: string;
  readonly actual?: string;
}

export interface GeneratedTestCase {
  readonly case_id: string;
  readonly title: string;
  readonly case_type: "positive" | "negative" | string;
  readonly start_state_id: string;
  readonly end_state_id: string;
  readonly start_state_label?: string;
  readonly end_state_label?: string;
  readonly expected_result: string;
  readonly steps: string[];
  readonly action_ids?: string[];
  readonly edge_signatures?: string[];
}

export interface FlowBundle {
  readonly config: ExplorerConfig;
  readonly started_at: string;
  readonly finished_at: string;
  readonly states: Record<string, FlowState>;
  readonly actions: Record<string, FlowAction>;
  readonly edges: FlowEdge[];
  readonly test_cases?: GeneratedTestCase[];
}

export interface GraphNode {
  readonly id: string;
  readonly label: string;
  readonly depth: number;
  readonly url: string;
}

export interface GraphEdge {
  readonly from: string;
  readonly to: string;
  readonly label: string;
  readonly outcome: Outcome;
}

export type VerdictValue = "pass" | "fail" | "warn" | "inconclusive";

export interface StepVerdictData {
  readonly verdict: VerdictValue;
  readonly reason: string;
  readonly expected: string;
  readonly actual: string;
}

export interface JourneyVerdictData {
  readonly verdict: VerdictValue;
  readonly summary: string;
  readonly pass_count: number;
  readonly fail_count: number;
  readonly warn_count: number;
}

export interface NarrativeStepData {
  readonly step_number: number;
  readonly action_description: string;
  readonly expected: string;
  readonly actual: string;
  readonly verdict: VerdictValue | null;
  readonly gherkin_when: string;
  readonly gherkin_then: string;
}

export interface FlowNarrativeData {
  readonly title: string;
  readonly precondition: string;
  readonly steps: NarrativeStepData[];
  readonly conclusion: string;
  readonly gherkin: string;
}

export interface FlowWithVerdict {
  readonly flow_id: string;
  readonly name: string;
  readonly description: string;
  readonly state_ids: string[];
  readonly action_ids: string[];
  readonly outcomes: string[];
  readonly is_cycle: boolean;
  readonly depth: number;
  readonly verdict?: JourneyVerdictData;
  readonly narrative?: FlowNarrativeData;
}
