import axios from "axios";

const API = "http://127.0.0.1:8000/api/v1";

export interface DashboardStats {
  cameras_online: number;
  active_incidents: number;
  fire_alerts: number;
  critical_incidents: number;
}

export async function getDashboardStats(): Promise<DashboardStats> {
  const response = await axios.get<DashboardStats>(
    `${API}/dashboard/stats`
  );

  return response.data;
}