import { useEffect } from "react";
import { toast } from "sonner";

export function useIncidentAlerts() {
  useEffect(() => {
    const socket = new WebSocket("ws://127.0.0.1:8000/api/ws");

    socket.onmessage = (event) => {
      console.log("📡 WebSocket message received:", event.data);

      // Heartbeat Safeguard: Exit early if the server sent an empty ping packet
      if (!event.data || event.data.trim() === "") {
        return;
      }

      try {
        const data = JSON.parse(event.data);

        if (data.event === "incident_created") {
          const incident = data.incident;

          toast.error(
            `🚨 ${incident.incident_type.replace(/_/g, " ")} detected`,
            {
              description: `Confidence ${(incident.confidence * 100).toFixed(1)}%`,
            }
          );
        }
      } catch (parseError) {
        console.error("❌ Malformed WebSocket JSON payload payload dropped:", parseError);
      }
    };

    socket.onerror = (error) => {
      console.error("❌ WebSocket connection mistake encountered:", error);
    };

    return () => {
      socket.close();
    };
  }, []);
}