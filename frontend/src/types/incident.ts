export interface Incident {
  id: number;
  camera_id: number;
  type: string;
  severity: string;
  status: string;
  confidence: number;
}