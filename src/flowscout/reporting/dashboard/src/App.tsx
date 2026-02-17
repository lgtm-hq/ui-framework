/** App shell with tab navigation. */

import { createSignal, lazy, Suspense } from "solid-js";
import type { Component } from "solid-js";
import { reportData } from "./stores/report";
import AppShell from "./components/layout/AppShell";
import TabBar from "./components/layout/TabBar";
import Summary from "./components/tabs/Summary";

const Timeline = lazy(() => import("./components/tabs/Timeline"));
const FlowView = lazy(() => import("./components/tabs/FlowView"));
const GraphView = lazy(() => import("./components/tabs/GraphView"));
const Quality = lazy(() => import("./components/tabs/quality/QualityTab"));
const PageList = lazy(() => import("./components/tabs/PageList"));

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
    <AppShell
      version={data().meta.version}
      tabBar={<TabBar tabs={TABS} activeTab={activeTab} onTabChange={setActiveTab} />}
    >
      <Suspense fallback={<div class="py-12 text-center text-text-secondary">Loading...</div>}>
        {(() => {
          const Tab = currentTab().component;
          return <Tab data={data()} />;
        })()}
      </Suspense>
    </AppShell>
  );
}
