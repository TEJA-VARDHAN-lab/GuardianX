import axios from "axios";

const API = "http://127.0.0.1:8000/api/v1";

export interface Incident {
  id: number;
  camera_id: number;
  incident_type: string;
  severity: string;
  confidence: number;
  status: string;
  snapshot: string | null;
  summary?: string | null;
  created_at: string;
}

export async function getIncidents(): Promise<Incident[]> {
  const response = await axios.get<Incident[]>(`${API}/incidents`);
  return response.data;
}

export async function updateIncidentStatus(
  incidentId: number,
  status: string
): Promise<Incident> {
  // Pass the status string wrapped inside a body payload object instead of raw params
  const response = await axios.patch<Incident>(
    `${API}/incidents/${incidentId}/status`,
    {
      status, // This sends {"status": "resolved"} directly in the HTTP request body
    }
  );

  return response.data;
}