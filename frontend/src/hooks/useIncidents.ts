import { useEffect, useState } from "react";
import { getIncidents } from "../services/incidentService";
import type { Incident } from "../services/incidentService";

export function useIncidents(refreshTrigger = 0) {
  const [incidents, setIncidents] = useState<Incident[]>([]);

  // 1. Core API Fetch Sequence
  useEffect(() => {
    let isMounted = true;

    const load = async () => {
      try {
        const data = await getIncidents();
        if (!isMounted) return;
        
        // FIX: Create a shallow copy via [...data] before calling reverse() 
        // to prevent unexpected mutations to the shared reference.
        setIncidents([...data].reverse());
      } catch (err) {
        console.error("Failed to fetch recent incidents:", err);
      }
    };

    load();

    return () => {
      isMounted = false;
    };
  }, [refreshTrigger]);

  // 2. Real-time Live Sync Channel (WebSocket Intercept)
  useEffect(() => {
    // Connect to the backend WebSocket route setup in your Uvicorn service
    const wsUrl = "ws://127.0.0.1:8000/api/ws";
    const ws = new WebSocket(wsUrl);

    ws.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        
        // Intercept the broadcast message dispatched by IncidentManager
        if (payload.event === "incident_created" && payload.incident) {
          const newIncident: Incident = payload.incident;
          
          setIncidents((currentIncidents) => {
            // Avoid duplicate items if the item was somehow fetched via HTTP simultaneously
            if (currentIncidents.some((item) => item.id === newIncident.id)) {
              return currentIncidents;
            }
            // Prepend the new real-time threat detection to the top of the feed list
            return [newIncident, ...currentIncidents];
          });
        }
      } catch (err) {
        console.error("Error parsing real-time incident broadcast payload:", err);
      }
    };

    ws.onerror = (error) => {
      console.error("Incident feed live sync channel encountered an error:", error);
    };

    return () => {
      ws.close();
    };
  }, []);

  return incidents;
}