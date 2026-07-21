import { create } from "zustand";

export interface Incident {
  id: number;
  camera_id: number;
  incident_type: string;
  severity: string;
  confidence: number;
  status: string;
  created_at: string;
}

interface IncidentState {
  incidents: Incident[];
  addIncident: (incident: Incident) => void;
}

export const useIncidentStore = create<IncidentState>((set) => ({
  incidents: [],
  addIncident: (incident) =>
    set((state) => ({
      incidents: [incident, ...state.incidents],
    })),
}));