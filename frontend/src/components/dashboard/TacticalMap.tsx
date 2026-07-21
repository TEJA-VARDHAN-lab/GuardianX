import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// FIX 1: Overcome the Leaflet asset bundling issue where default marker pins break
// by explicitly injecting public CDN icon asset paths.
const DefaultIcon = L.icon({
  iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
  iconRetinaUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png",
  shadowUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

export default function TacticalMap() {
  return (
    <div className="rounded-2xl border bg-background shadow-sm overflow-hidden w-full">
      
      {/* Header Section */}
      <div className="px-5 py-4 border-b">
        <h2 className="font-semibold text-lg tracking-tight">
          Tactical Map
        </h2>
        <p className="text-xs text-muted-foreground">
          Real-time camera locations and operational security alerts
        </p>
      </div>

      {/* Map Dynamic Frame Area */}
      <div className="h-[450px] w-full relative">
        <MapContainer
          center={[17.385, 78.4867]}
          zoom={13}
          scrollWheelZoom={true}
          className="h-full w-full z-0"
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          <Marker position={[17.385, 78.4867]}>
            <Popup className="font-sans">
              <div className="p-1">
                <p className="font-medium text-sm">GuardianX Camera 1</p>
                <p className="text-xs text-muted-foreground mt-0.5">Status: Operational</p>
              </div>
            </Popup>
          </Marker>
        </MapContainer>
      </div>

    </div>
  );
}