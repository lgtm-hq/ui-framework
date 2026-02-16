/** App shell with tab navigation. */

import { createSignal, For, Show, lazy, Suspense } from "solid-js";
import type { Component } from "solid-js";
import { reportData } from "./stores/report";
import Summary from "./components/Summary";

const Timeline = lazy(() => import("./components/Timeline"));
const FlowView = lazy(() => import("./components/FlowView"));
const GraphView = lazy(() => import("./components/GraphView"));
const Quality = lazy(() => import("./components/Quality"));
const PageList = lazy(() => import("./components/PageList"));

interface Tab {
  id: string;
  label: string;
  component: Component<{ data: ReturnType<typeof reportData> }>;
}

const TABS: Tab[] = [
  { id: "summary", label: "Dashboard", component: Summary },
  { id: "graph", label: "Site Map", component: GraphView },
  { id: "timeline", label: "Timeline", component: Timeline },
  { id: "flows", label: "Test Flows", component: FlowView },
  { id: "quality", label: "Quality", component: Quality },
  { id: "pages", label: "Page Objects", component: PageList },
];

export default function App() {
  const [activeTab, setActiveTab] = createSignal("summary");
  const data = reportData;

  const currentTab = () => TABS.find((t) => t.id === activeTab()) ?? TABS[0];

  return (
    <div class="app">
      <nav class="tab-bar">
        <div class="tab-bar-brand">
          <strong>Flowscout</strong>
          <Show when={data().meta.version}>
            <span class="version">v{data().meta.version}</span>
          </Show>
        </div>
        <div class="tab-bar-tabs">
          <For each={TABS}>
            {(tab) => (
              <button
                class={`tab-btn ${activeTab() === tab.id ? "active" : ""}`}
                onClick={() => setActiveTab(tab.id)}
              >
                {tab.label}
              </button>
            )}
          </For>
        </div>
      </nav>
      <main class="tab-content">
        <Suspense fallback={<div class="loading">Loading...</div>}>
          {(() => {
            const Tab = currentTab().component;
            return <Tab data={data()} />;
          })()}
        </Suspense>
      </main>
    </div>
  );
}
