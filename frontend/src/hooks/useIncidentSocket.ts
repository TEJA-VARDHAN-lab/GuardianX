import { useEffect } from "react";

export function useIncidentSocket(
  onIncident: () => void
) {

  useEffect(() => {

    const socket = new WebSocket(
      "ws://127.0.0.1:8000/api/ws"
    );

    socket.onmessage = () => {
      onIncident();
    };

    socket.onerror = (error) => {
      console.error(
        "WebSocket error",
        error
      );
    };


    return () => {
      socket.close();
    };

  }, [onIncident]);

}