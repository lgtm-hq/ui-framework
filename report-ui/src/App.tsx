import { type ChangeEvent, useEffect, useMemo, useState } from "react";

import { CommandBar } from "./components/CommandBar";
import { JourneyDetailPanel } from "./components/JourneyDetailPanel";
import { JourneyList } from "./components/JourneyList";
import { OutcomePanel } from "./components/OutcomePanel";
import { PageReference } from "./components/PageReference";
import { StateGraph } from "./components/StateGraph";
import { StatsSummary } from "./components/StatsSummary";
import {
  buildCaseFlowSegments,
  buildEdgeSignature,
  buildGraphData,
  buildJourneyBreadcrumb,
  type EnrichedCase,
  outcomeOrder,
  parseFlowBundle,
  worstOutcome,
} from "./lib/flow-utils";
import type { FlowAction, FlowBundle, FlowEdge, FlowState, GeneratedTestCase } from "./types";

function App() {
  const [bundle, setBundle] = useState<FlowBundle | null>(null);
  const [sourceLabel, setSourceLabel] = useState<string>("No file loaded");
  const [error, setError] = useState<string>("");
  const [outcomeFilter, setOutcomeFilter] = useState<string>("all");
  const [searchText, setSearchText] = useState<string>("");
  const [caseFilter, setCaseFilter] = useState<string>("all");
  const [showTechnicalIds, setShowTechnicalIds] = useState<boolean>(false);
  const [selectedCaseId, setSelectedCaseId] = useState<string | null>(null);
  const [selectedNodeId, setSelectedNodeId] = useState<string | null>(null);

  useEffect(() => {
    const loadDefaultBundle = async (): Promise<void> => {
      try {
        const response = await fetch("/flow_bundle.json");
        if (!response.ok) {
          return;
        }
        const payload: unknown = await response.json();
        const parsed = parseFlowBundle(payload);
        setBundle(parsed);
        setSourceLabel("Loaded /flow_bundle.json");
      } catch {
        // Ignore: optional auto-load path for local dev.
      }
    };
    void loadDefaultBundle();
  }, []);

  const statesById = useMemo<Record<string, FlowState>>(() => bundle?.states ?? {}, [bundle]);
  const actionsById = useMemo<Record<string, FlowAction>>(() => bundle?.actions ?? {}, [bundle]);
  const edges = useMemo<FlowEdge[]>(() => bundle?.edges ?? [], [bundle]);
  const testCases = useMemo<GeneratedTestCase[]>(() => bundle?.test_cases ?? [], [bundle]);

  const edgeBySignature = useMemo<Map<string, FlowEdge>>(() => {
    const map = new Map<string, FlowEdge>();
    for (const edge of edges) {
      const signature = buildEdgeSignature({
        sourceId: edge.source_state_id,
        actionId: edge.action_id,
        targetId: edge.target_state_id,
      });
      if (!map.has(signature)) {
        map.set(signature, edge);
      }
    }
    return map;
  }, [edges]);

  const outcomes = useMemo<string[]>(() => {
    const dynamic = new Set(edges.map((edge) => edge.outcome));
    const standard = outcomeOrder.filter((entry) => dynamic.has(entry));
    const additional = [...dynamic].filter((entry) => !outcomeOrder.includes(entry));
    return ["all", ...standard, ...additional];
  }, [edges]);

  const outcomeCounts = useMemo<Record<string, number>>(() => {
    const counts: Record<string, number> = {};
    for (const edge of edges) {
      counts[edge.outcome] = (counts[edge.outcome] ?? 0) + 1;
    }
    return counts;
  }, [edges]);

  const enrichedCases = useMemo<EnrichedCase[]>(() => {
    return testCases.map((tc) => {
      const segments = buildCaseFlowSegments({
        testCase: tc,
        edgeBySignature,
        statesById,
        actionsById,
      });
      const breadcrumb = buildJourneyBreadcrumb({
        testCase: tc,
        statesById,
        actionsById,
      });
      const worst = worstOutcome(segments);
      const outcomeSet = new Set(segments.map((s) => s.outcome));
      return {
        testCase: tc,
        segments,
        breadcrumb,
        worst,
        outcomes: outcomeSet,
      };
    });
  }, [testCases, edgeBySignature, statesById, actionsById]);

  const filteredCases = useMemo<EnrichedCase[]>(() => {
    return enrichedCases.filter((enriched) => {
      if (caseFilter !== "all" && enriched.testCase.case_type !== caseFilter) {
        return false;
      }
      if (outcomeFilter !== "all" && !enriched.outcomes.has(outcomeFilter)) {
        return false;
      }
      if (searchText.trim() !== "") {
        const needle = searchText.trim().toLowerCase();
        const haystack = [
          enriched.testCase.title,
          enriched.testCase.expected_result,
          enriched.testCase.start_state_label ?? "",
          enriched.testCase.end_state_label ?? "",
          ...enriched.testCase.steps,
          ...enriched.breadcrumb,
        ]
          .join(" ")
          .toLowerCase();
        if (!haystack.includes(needle)) {
          return false;
        }
      }
      return true;
    });
  }, [enrichedCases, caseFilter, outcomeFilter, searchText]);

  const selectedCase = useMemo<GeneratedTestCase | null>(() => {
    if (!selectedCaseId) {
      return null;
    }
    return testCases.find((tc) => tc.case_id === selectedCaseId) ?? null;
  }, [selectedCaseId, testCases]);

  const selectedSegments = useMemo(() => {
    if (!selectedCase) {
      return [];
    }
    return buildCaseFlowSegments({
      testCase: selectedCase,
      edgeBySignature,
      statesById,
      actionsById,
    });
  }, [actionsById, edgeBySignature, selectedCase, statesById]);

  const sortedStates = useMemo<FlowState[]>(() => {
    return Object.values(statesById).sort(
      (left, right) => left.depth - right.depth || left.state_id.localeCompare(right.state_id),
    );
  }, [statesById]);

  const graphData = useMemo(() => {
    return buildGraphData({
      states: statesById,
      edges,
      actions: actionsById,
    });
  }, [statesById, edges, actionsById]);

  const highlightedNodes = useMemo<Set<string>>(() => {
    if (!selectedCase) return new Set();
    const ids = new Set<string>();
    ids.add(selectedCase.start_state_id);
    ids.add(selectedCase.end_state_id);
    for (const seg of selectedSegments) {
      ids.add(seg.sourceId);
      ids.add(seg.targetId);
    }
    return ids;
  }, [selectedCase, selectedSegments]);

  const handleFileInput = async (event: ChangeEvent<HTMLInputElement>): Promise<void> => {
    const file = event.target.files?.[0];
    if (!file) {
      return;
    }
    try {
      const payload: unknown = JSON.parse(await file.text());
      const parsed = parseFlowBundle(payload);
      setBundle(parsed);
      setSourceLabel(`Loaded ${file.name}`);
      setError("");
      setSelectedCaseId(null);
      setSelectedNodeId(null);
    } catch (loadError) {
      setError(
        loadError instanceof Error ? loadError.message : "Failed to parse flow bundle JSON.",
      );
    }
  };

  const handleNodeClick = (stateId: string) => {
    setSelectedNodeId(stateId === selectedNodeId ? null : stateId);
  };

  const isDetailOpen = selectedCase !== null;
  const timestamp = bundle?.started_at ? new Date(bundle.started_at).toLocaleString() : undefined;

  return (
    <div className="flex h-screen flex-col bg-bg-deep text-warm-gray">
      {/* Noise texture overlay */}
      <div className="bg-noise pointer-events-none fixed inset-0 z-50" />

      <CommandBar
        sourceLabel={sourceLabel}
        onFileLoad={(event) => {
          void handleFileInput(event);
        }}
        error={error}
        showTechnicalIds={showTechnicalIds}
        onToggleTechnicalIds={() => {
          setShowTechnicalIds(!showTechnicalIds);
        }}
        timestamp={timestamp}
      />

      <div className="flex min-h-0 flex-1">
        {/* Left Rail */}
        <nav className="flex w-[280px] shrink-0 flex-col gap-6 overflow-auto border-r border-brass/15 bg-bg-mid/50 p-5">
          <StatsSummary
            stateCount={Object.keys(statesById).length}
            transitionCount={edges.length}
            journeyCount={testCases.length}
            actionCount={Object.keys(actionsById).length}
            passCount={edges.filter((e) => e.verdict === "pass").length}
            failCount={edges.filter((e) => e.verdict === "fail").length}
            warnCount={edges.filter((e) => e.verdict === "warn").length}
          />

          <div className="h-px bg-brass/10" />

          <OutcomePanel
            outcomes={outcomes}
            activeOutcome={outcomeFilter}
            onOutcomeChange={setOutcomeFilter}
            caseFilter={caseFilter}
            onCaseFilterChange={setCaseFilter}
            searchText={searchText}
            onSearchChange={setSearchText}
            resultCount={filteredCases.length}
            totalCount={enrichedCases.length}
            outcomeCounts={outcomeCounts}
            totalEdges={edges.length}
          />

          <div className="h-px bg-brass/10" />

          <PageReference states={sortedStates} showTechnicalIds={showTechnicalIds} />
        </nav>

        {/* Main Canvas */}
        <main className="flex min-w-0 flex-1 flex-col overflow-auto">
          {/* State Graph */}
          <div className="p-5 pb-0">
            <StateGraph
              nodes={graphData.nodes}
              edges={graphData.edges}
              onNodeClick={handleNodeClick}
              highlightedNodes={highlightedNodes}
            />
          </div>

          {/* Journeys section */}
          <div className="flex min-h-0 flex-1 p-5">
            <div className={`transition-all duration-300 ${isDetailOpen ? "w-[40%]" : "w-full"}`}>
              <JourneyList
                cases={filteredCases}
                onSelectCase={setSelectedCaseId}
                selectedCaseId={selectedCaseId}
              />
            </div>

            {isDetailOpen ? (
              <JourneyDetailPanel
                testCase={selectedCase}
                caseFlowSegments={selectedSegments}
                statesById={statesById}
                actionsById={actionsById}
                showTechnicalIds={showTechnicalIds}
                onClose={() => {
                  setSelectedCaseId(null);
                }}
              />
            ) : null}
          </div>
        </main>
      </div>
    </div>
  );
}

export default App;
