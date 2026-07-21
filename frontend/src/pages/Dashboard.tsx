import { useState } from "react";
import type { Incident } from "../services/incidentService";
import IncidentDetails from "../components/dashboard/IncidentDetails";
import LiveCamera from "../components/dashboard/LiveCamera";
import StatCard from "../components/dashboard/StatCard";
import IncidentFeed from "../components/dashboard/IncidentFeed";
import TacticalMap from "../components/dashboard/TacticalMap";
import { useDashboardStats } from "../hooks/useDashboardStats";
import { useIncidentAlerts } from "../hooks/useIncidentAlerts";

export default function Dashboard() {
  // 🚀 Mount the live websocket alert and notification pipeline cleanly
  useIncidentAlerts();

  // Extract the stats payload and handle potential custom hook response structures
  const statsResponse = useDashboardStats();
  
  // Safeguard against hooks returning data wrappers vs direct query states
  const stats = "data" in statsResponse ? (statsResponse as any).data : statsResponse;
  const refreshStats = "mutate" in statsResponse ? (statsResponse as any).mutate : 
                       "refresh" in statsResponse ? (statsResponse as any).refresh : null;

  const [selectedIncident, setSelectedIncident] = useState<Incident | null>(null);

  // Unified callback event handler for handling incident mutations
  const handleIncidentUpdated = (updatedIncident?: Incident) => {
    if (updatedIncident && updatedIncident.status === "resolved") {
      // Clear the target details panel if the threat is completely cleared
      setSelectedIncident(null);
    } else if (updatedIncident) {
      // Otherwise, update the state block to match the fresh schema values
      setSelectedIncident(updatedIncident);
    } else {
      setSelectedIncident(null);
    }

    // Force data revalidation to instantly update the aggregate top-cards
    if (typeof refreshStats === "function") {
      refreshStats();
    }
  };

  return (
    <main className="min-h-screen bg-muted/30 p-6 space-y-6">

      {/* Header Controls */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold tracking-tight">
            GuardianX
          </h1>
          <p className="text-sm text-muted-foreground">
            AI Security Monitoring Platform
          </p>
        </div>

        <span className="px-4 py-2 rounded-full bg-green-100 text-green-700 text-sm font-semibold">
          ● System Online
        </span>
      </div>

      {/* Aggregated Analytical Statistics */}
      <div className="grid grid-cols-4 gap-5">
        <StatCard
          title="Cameras"
          value={stats?.cameras_online ?? 0}
        />
        <StatCard
          title="Active Incidents"
          value={stats?.active_incidents ?? 0}
        />
        <StatCard
          title="Fire Alerts"
          value={stats?.fire_alerts ?? 0}
        />
        <StatCard
          title="Critical"
          value={stats?.critical_incidents ?? 0}
        />
      </div>

      {/* Primary Field Video Feeds */}
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <LiveCamera />
        </div>

        <div>
          <TacticalMap />
        </div>
      </div>

      {/* Live Logging Feeds and Action Centers */}
      <div className="grid grid-cols-3 gap-6">
        <div className="col-span-2">
          <IncidentFeed
            onSelect={setSelectedIncident}
            selectedId={selectedIncident?.id}
          />
        </div>

        <div>
          <IncidentDetails
            incident={selectedIncident}
            onUpdated={handleIncidentUpdated}
          />
        </div>
      </div>

    </main>
  );
}