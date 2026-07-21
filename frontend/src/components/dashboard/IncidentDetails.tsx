import { updateIncidentStatus } from "../../services/incidentService";
import type { Incident } from "../../services/incidentService";

interface Props {
  incident: Incident | null;
  onUpdated: (updatedIncident: Incident) => void;
}

export default function IncidentDetails({
  incident,
  onUpdated,
}: Props) {

  if (!incident) {
    return (
      <div className="rounded-xl border bg-white p-6 shadow-sm flex flex-col items-center justify-center text-center min-h-[250px]">
        <p className="text-gray-400 font-medium">
          Select an active threat from the feed to view operational analytics.
        </p>
      </div>
    );
  }

  async function resolveIncident() {
    if (!incident) return;

    try {
      // 1. Send the data payload directly to the FastAPI server endpoint
      const updatedData = await updateIncidentStatus(
        incident.id,
        "resolved"
      );

      // 2. Pass the fresh server response state back up to the parent dashboard context loop
      onUpdated(updatedData);

    } catch (error) {
      console.error(
        "Failed to resolve system incident entry:",
        error
      );
    }
  }

  return (
    <div className="rounded-xl border bg-white p-6 space-y-5 shadow-sm">
      
      {/* Target Camera Feed Frame Snapshot Capture */}
      {incident.snapshot && (
        <div className="overflow-hidden rounded-lg border border-gray-100 bg-gray-50">
          <img
            src={`http://127.0.0.1:8000/${incident.snapshot}`}
            alt="Security environment anomaly snapshot flag"
            className="w-full h-48 object-cover object-center"
          />
        </div>
      )}

      <div>
        <h2 className="text-xl font-bold tracking-tight capitalize text-gray-900">
          {incident.incident_type.replace("_", " ")}
        </h2>
      </div>

      <div className="grid grid-cols-2 gap-x-4 gap-y-2 text-sm border-t border-b border-gray-100 py-3 text-gray-600">
        <p>
          <strong className="text-gray-900 font-semibold">ID:</strong> #{incident.id}
        </p>

        <p>
          <strong className="text-gray-900 font-semibold">Source Unit:</strong> Cam {incident.camera_id}
        </p>

        <p className="capitalize">
          <strong className="text-gray-900 font-semibold">Severity:</strong> {incident.severity}
        </p>

        <p>
          <strong className="text-gray-900 font-semibold">Model Confidence:</strong>{" "}
          {(incident.confidence * 100).toFixed(1)}%
        </p>

        <p className="capitalize">
          <strong className="text-gray-900 font-semibold">Status:</strong> {incident.status}
        </p>

        <p>
          <strong className="text-gray-900 font-semibold">Timestamp:</strong>{" "}
          {new Date(incident.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
        </p>
      </div>

      {/* Conditional Mitigation Trigger Button Action Drawer */}
      {incident.status !== "resolved" && (
        <button
          onClick={resolveIncident}
          className="w-full rounded-lg bg-emerald-600 text-white py-2.5 font-semibold transition-colors hover:bg-emerald-700 shadow-sm"
        >
          Close Incident Vector
        </button>
      )}

    </div>
  );
}