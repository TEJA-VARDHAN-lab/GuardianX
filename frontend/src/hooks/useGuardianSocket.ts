import { useEffect, useState, useRef } from "react"
import { useIncidentStore } from "../store/incidentStore"

interface DashboardStats {
  cameras_online: number
  active_incidents: number
  fire_alerts: number
  critical_incidents: number
}

export function useGuardianSocket() {
  const addIncident = useIncidentStore((state) => state.addIncident)

  const [status, setStatus] = useState("Connecting...")
  const [stats, setStats] = useState<DashboardStats>({
    cameras_online: 0,
    active_incidents: 0,
    fire_alerts: 0,
    critical_incidents: 0,
  })

  const wsRef = useRef<WebSocket | null>(null)

  useEffect(() => {
    let isMounted = true
    const ws = new WebSocket("ws://localhost:8000/api/ws")
    wsRef.current = ws

    ws.onopen = () => {
      if (isMounted) {
        setStatus("Connected")
        console.log("🟢 WebSocket link established with FastAPI")
      }
    }

    ws.onmessage = (event) => {
      if (!isMounted) return

      try {
        const message = JSON.parse(event.data)

        if (
          message.cameras_online !== undefined &&
          message.active_incidents !== undefined
        ) {
          setStats(message)
          return
        }

        if (message.event === "incident.created") {
          addIncident(message.payload)
          return
        }

        console.log("Unknown WebSocket message:", message)
      } catch (err) {
        console.error("Error parsing socket payload:", err)
      }
    }

    ws.onclose = (event) => {
      if (isMounted) {
        setStatus("Disconnected")
        console.log(`🔴 WebSocket link closed. Code: ${event.code}`)
      }
    }

    ws.onerror = (error) => {
      if (!isMounted || ws.readyState === WebSocket.CLOSED) return
      console.error("WebSocket error observed:", error)
    }

    return () => {
      isMounted = false
      if (ws.readyState === WebSocket.OPEN || ws.readyState === WebSocket.CONNECTING) {
        ws.close()
      }
      wsRef.current = null
    }
  }, [addIncident])

  return { stats, status }
}