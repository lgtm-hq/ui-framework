import { useEffect, useRef } from "react";
import { DataSet } from "vis-data";
import { Network } from "vis-network";

import { outcomeEdgeColor } from "../lib/flow-utils";
import type { GraphEdge, GraphNode } from "../types";

interface StateGraphProps {
  readonly nodes: GraphNode[];
  readonly edges: GraphEdge[];
  readonly onNodeClick?: (stateId: string) => void;
  readonly highlightedNodes?: Set<string>;
}

function depthColor(depth: number, maxDepth: number): string {
  const t = maxDepth > 0 ? Math.min(depth / maxDepth, 1) : 0;
  // Interpolate brass (#C9A84C) → verdigris (#5EADA4)
  const r = Math.round(201 + (94 - 201) * t);
  const g = Math.round(168 + (173 - 168) * t);
  const b = Math.round(76 + (164 - 76) * t);
  return `rgb(${r}, ${g}, ${b})`;
}

function CompassRose() {
  return (
    <svg
      className="animate-compass-pulse pointer-events-none absolute right-4 top-4"
      width="64"
      height="64"
      viewBox="0 0 64 64"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <circle cx="32" cy="32" r="30" stroke="#C9A84C" strokeWidth="0.5" opacity="0.2" />
      <circle cx="32" cy="32" r="22" stroke="#C9A84C" strokeWidth="0.3" opacity="0.15" />
      <polygon points="32,4 34,28 32,26 30,28" fill="#C9A84C" opacity="0.2" />
      <polygon points="32,60 30,36 32,38 34,36" fill="#5EADA4" opacity="0.2" />
      <polygon points="4,32 28,30 26,32 28,34" fill="#5EADA4" opacity="0.15" />
      <polygon points="60,32 36,34 38,32 36,30" fill="#C9A84C" opacity="0.15" />
      <circle cx="32" cy="32" r="2" fill="#C9A84C" opacity="0.25" />
      {/* Ordinal points */}
      <line x1="32" y1="2" x2="32" y2="8" stroke="#C9A84C" strokeWidth="0.5" opacity="0.15" />
      <line x1="32" y1="56" x2="32" y2="62" stroke="#C9A84C" strokeWidth="0.5" opacity="0.15" />
      <line x1="2" y1="32" x2="8" y2="32" stroke="#C9A84C" strokeWidth="0.5" opacity="0.15" />
      <line x1="56" y1="32" x2="62" y2="32" stroke="#C9A84C" strokeWidth="0.5" opacity="0.15" />
    </svg>
  );
}

export function StateGraph(props: StateGraphProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const networkRef = useRef<Network | null>(null);
  const { nodes: graphNodes, edges: graphEdges, highlightedNodes, onNodeClick } = props;

  useEffect(() => {
    if (!containerRef.current || graphNodes.length === 0) return;

    const maxDepth = Math.max(...graphNodes.map((n) => n.depth), 1);

    const nodes = new DataSet(
      graphNodes.map((node) => {
        const color = depthColor(node.depth, maxDepth);
        const isHighlighted = highlightedNodes?.has(node.id) ?? false;
        return {
          id: node.id,
          label: node.label.length > 30 ? node.label.slice(0, 28) + "..." : node.label,
          title: `${node.label}\n${node.url}\nDepth: ${node.depth}`,
          shape: "box" as const,
          color: {
            background: isHighlighted ? "rgba(201, 168, 76, 0.25)" : "#1A1D28",
            border: color,
            highlight: {
              background: "rgba(201, 168, 76, 0.2)",
              border: "#C9A84C",
            },
            hover: {
              background: "#22252E",
              border: color,
            },
          },
          borderWidth: isHighlighted ? 2.5 : 1.5,
          borderWidthSelected: 2.5,
          font: {
            color: "#B8B0A2",
            size: 11,
            face: "JetBrains Mono, monospace",
          },
          shadow: {
            enabled: true,
            color: color,
            size: isHighlighted ? 12 : 6,
            x: 0,
            y: 0,
          },
          margin: { top: 8, bottom: 8, left: 12, right: 12 },
        };
      }),
    );

    const edges = new DataSet(
      graphEdges.map((edge, i) => ({
        id: `e-${i}`,
        from: edge.from,
        to: edge.to,
        label: edge.label.length > 20 ? edge.label.slice(0, 18) + "..." : edge.label,
        title: `${edge.label} → ${edge.outcome}`,
        color: {
          color: outcomeEdgeColor[edge.outcome] ?? "#B8B0A2",
          highlight: "#C9A84C",
          hover: "#C9A84C",
          opacity: 0.7,
        },
        arrows: {
          to: { enabled: true, scaleFactor: 0.5 },
        },
        smooth: {
          enabled: true,
          type: "curvedCW" as const,
          roundness: 0.2,
        },
        font: {
          color: "#B8B0A266",
          size: 9,
          face: "JetBrains Mono, monospace",
          strokeWidth: 0,
          align: "top" as const,
        },
        width: 1,
      })),
    );

    const network = new Network(
      containerRef.current,
      { nodes, edges },
      {
        physics: {
          solver: "forceAtlas2Based",
          forceAtlas2Based: {
            gravitationalConstant: -60,
            centralGravity: 0.01,
            springLength: 180,
            springConstant: 0.06,
            damping: 0.4,
          },
          stabilization: {
            enabled: true,
            iterations: 250,
          },
        },
        interaction: {
          hover: true,
          tooltipDelay: 200,
          zoomView: true,
          dragView: true,
        },
        layout: {
          improvedLayout: true,
        },
      },
    );

    network.on("click", (params: { nodes: string[] }) => {
      if (params.nodes.length > 0 && onNodeClick) {
        onNodeClick(params.nodes[0]);
      }
    });

    networkRef.current = network;

    return () => {
      network.destroy();
      networkRef.current = null;
    };
  }, [graphNodes, graphEdges, highlightedNodes, onNodeClick]);

  return (
    <section className="relative overflow-hidden rounded-xl border border-brass/15 bg-surface">
      <div className="flex items-center justify-between border-b border-brass/10 px-4 py-2.5">
        <h3 className="font-sans text-[10px] font-semibold uppercase tracking-[0.2em] text-warm-gray/50">
          State Topology
        </h3>
        <span className="font-mono text-[10px] text-warm-gray/30">
          {props.nodes.length} nodes · {props.edges.length} edges
        </span>
      </div>
      <div className="bg-grid-pattern relative" style={{ height: 500 }}>
        <CompassRose />
        <div ref={containerRef} className="h-full w-full" />
        {props.nodes.length === 0 ? (
          <div className="absolute inset-0 flex items-center justify-center">
            <p className="text-sm text-warm-gray/30">Load a bundle to view the state topology</p>
          </div>
        ) : null}
      </div>
    </section>
  );
}
