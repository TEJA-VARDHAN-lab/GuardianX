import { useIncidents } from "../../hooks/useIncidents";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import type { Incident } from "../../services/incidentService";
import { cn } from "@/lib/utils"; 
import { useState } from "react";

interface Props {
  onSelect: (incident: Incident) => void;
  selectedId?: number | string; 
}

function IncidentSnapshot({ src, alt }: { src: string; alt: string }) {
  const [error, setError] = useState(false);

  if (error) {
    return (
      <div className="w-full h-full flex flex-col items-center justify-center text-muted-foreground bg-muted text-xs p-3 gap-1">
        <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="w-5 h-5 opacity-60">
          <path strokeLinecap="round" strokeLinejoin="round" d="m2.25 15.75 5.159-5.159a2.25 2.25 0 0 1 3.182 0l5.159 5.159m-1.5-1.5 1.409-1.409a2.25 2.25 0 0 1 3.182 0l2.909 2.909m-18 3.75h16.5a1.5 1.5 0 0 0 1.5-1.5V6a1.5 1.5 0 0 0-1.5-1.5H3.75A1.5 1.5 0 0 0 2.25 6v12a1.5 1.5 0 0 0 1.5 1.5Zm10.5-11.25h.008v.008h-.008V8.25Zm.375 0a.375 0 1 1-.75 0 .375 0 0 1 .75 0Z" />
        </svg>
        <span>Image Unavailable</span>
      </div>
    );
  }

  return (
    <img
      src={src}
      alt={alt}
      className="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
      onError={() => setError(true)}
    />
  );
}

export default function IncidentFeed({ onSelect, selectedId }: Props) {
  const incidents = useIncidents() || []; 
  const [search, setSearch] = useState("");
  const [severityFilter, setSeverityFilter] = useState("all");
  const [statusFilter, setStatusFilter] = useState("all");
  
  const filteredIncidents = incidents.filter((incident) => {
    const matchesSearch = incident.incident_type
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchesSeverity =
      severityFilter === "all" ||
      incident.severity.toLowerCase() === severityFilter;

    const matchesStatus =
      statusFilter === "all" ||
      incident.status.toLowerCase() === statusFilter;

    return matchesSearch && matchesSeverity && matchesStatus;
  });

  const getSeverityStyle = (severity: string) => {
    switch (severity?.toLowerCase()) {
      case "critical":
        return "bg-red-600 text-white border-red-600";
      case "high":
        return "bg-orange-500 text-white border-orange-500";
      case "medium":
        return "bg-yellow-400 text-black border-yellow-400";
      case "low":
        return "bg-gray-200 text-gray-800 border-gray-200";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  return (
    <Card className="rounded-2xl border bg-background shadow-sm overflow-hidden">
      <CardHeader className="pb-3 border-b">
        <CardTitle className="text-lg font-semibold tracking-tight">Recent Incidents</CardTitle>
      </CardHeader>
      
      <CardContent className="pt-4">
        {/* Filter Operations Panel */}
        <div className="flex flex-col gap-2 sm:flex-row sm:gap-3 mb-4">
          <input
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            placeholder="Search incidents..."
            className="border rounded-lg px-3 py-2 flex-1 text-sm bg-background focus:outline-none focus:ring-1 focus:ring-primary"
          />

          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm bg-background cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary"
          >
            <option value="all">All Severity</option>
            <option value="critical">Critical</option>
            <option value="high">High</option>
            <option value="medium">Medium</option>
            <option value="low">Low</option>
          </select>

          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border rounded-lg px-3 py-2 text-sm bg-background cursor-pointer focus:outline-none focus:ring-1 focus:ring-primary"
          >
            <option value="all">All Status</option>
            <option value="detected">Detected</option>
            <option value="resolved">Resolved</option>
          </select>
        </div>

        {/* Dynamic Card Feed Scroller Container */}
        <ScrollArea className="h-[500px] pr-4">
          <div className="space-y-4">
            {filteredIncidents.map((incident) => {
              const isSelected = incident.id === selectedId;
              
              return (
                <div
                  key={incident.id}
                  onClick={() => onSelect(incident)} // <-- RESTORED: Vital user interaction action link
                  className={cn(
                    "group relative overflow-hidden border rounded-xl p-4 transition-all duration-200 hover:shadow-md bg-card cursor-pointer",
                    incident.severity === "critical" && "ring-2 ring-red-500/80 shadow-md",
                    incident.severity === "critical" && !isSelected && "animate-pulse",
                    isSelected 
                      ? "border-primary ring-1 ring-primary bg-accent/30" 
                      : "hover:border-muted-foreground/30"
                  )}
                >
                  {incident.snapshot && (
                    <div className="relative overflow-hidden rounded-lg mb-3 bg-muted aspect-video max-h-44 border border-border/50">
                      <IncidentSnapshot 
                        src={`http://127.0.0.1:8000/${incident.snapshot}`}
                        alt={`Incident snapshot for #${incident.id}`}
                      />
                    </div>
                  )}

                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-mono text-muted-foreground font-medium">
                      #{incident.id.toString().substring(0, 8)}
                    </span>
                    <div className="flex gap-2">
                      <Badge className={cn("capitalize shadow-none", getSeverityStyle(incident.severity))}>
                        {incident.severity}
                      </Badge>
                      <Badge variant="outline" className="capitalize bg-background">
                        {incident.status}
                      </Badge>
                    </div>
                  </div>

                  <div className="space-y-1">
                    <h4 className="text-base font-semibold tracking-tight text-foreground capitalize">
                      {incident.incident_type.replace("_", " ")}
                    </h4>
                    <div className="text-sm text-muted-foreground flex items-center justify-between">
                      <span>AI Confidence</span>
                      <span className="font-mono font-medium text-foreground">
                        {(incident.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              );
            })}

            {/* Accurate Empty State Intercept */}
            {filteredIncidents.length === 0 && (
              <div className="flex flex-col items-center justify-center py-12 text-center text-muted-foreground border border-dashed rounded-xl">
                <p className="text-sm font-medium">No threats match the current filtering parameters.</p>
              </div>
            )}
          </div>
        </ScrollArea>
      </CardContent>
    </Card>
  );
}