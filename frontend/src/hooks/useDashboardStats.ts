import { useEffect, useState } from "react";

import { getDashboardStats } from "../services/dashboardService";
import type { DashboardStats } from "../services/dashboardService";

export function useDashboardStats() {
  const [stats, setStats] = useState<DashboardStats>({
    cameras_online: 0,
    active_incidents: 0,
    fire_alerts: 0,
    critical_incidents: 0,
  });

  async function load() {
    try {
      setStats(await getDashboardStats());
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    load();

    const timer = setInterval(load, 1000);

    return () => clearInterval(timer);
  }, []);

  return stats;
}