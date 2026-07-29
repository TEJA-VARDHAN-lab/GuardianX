import { useEffect, useState } from "react";
import {
  MapContainer,
  TileLayer,
  Marker,
  Popup,
  Polyline,
} from "react-leaflet";
import L from "leaflet";
import "leaflet/dist/leaflet.css";

// -------------------- Icons --------------------

const userIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-blue.png",
  shadowUrl:
    "https://unpkg.com/leaflet/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

const fireIcon = new L.Icon({
  iconUrl:
    "https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-red.png",
  shadowUrl:
    "https://unpkg.com/leaflet/dist/images/marker-shadow.png",
  iconSize: [25, 41],
  iconAnchor: [12, 41],
});

export default function TacticalMap() {
  const [userLocation, setUserLocation] = useState<[number, number]>();

  // Fire / Camera Location
  const fireLocation: [number, number] = [
    17.3850,
    78.4867,
  ];

  useEffect(() => {
    if (!navigator.geolocation) {
      alert("Geolocation is not supported by this browser.");
      return;
    }

    const watchId = navigator.geolocation.watchPosition(
      (position) => {
        console.log("========== GUARDIANX LOCATION ==========");
        console.log("Latitude :", position.coords.latitude);
        console.log("Longitude:", position.coords.longitude);
        console.log("Accuracy :", position.coords.accuracy);

        setUserLocation([
          position.coords.latitude,
          position.coords.longitude,
        ]);
      },

      (err) => {
        console.error("Geolocation Error:", err);

        switch (err.code) {
          case err.PERMISSION_DENIED:
            alert("Location permission denied.");
            break;

          case err.POSITION_UNAVAILABLE:
            alert("Location unavailable.");
            break;

          case err.TIMEOUT:
            alert("Location request timed out.");
            break;

          default:
            alert("Unknown location error.");
        }
      },

      {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
      }
    );

    return () => navigator.geolocation.clearWatch(watchId);
  }, []);

  if (!userLocation) {
    return (
      <div className="h-[500px] flex items-center justify-center text-lg font-semibold">
        Fetching Live Location...
      </div>
    );
  }

  return (
    <MapContainer
      center={userLocation}
      zoom={15}
      style={{ height: "500px", width: "100%" }}
      scrollWheelZoom={true}
    >
      <TileLayer
        attribution="&copy; OpenStreetMap contributors"
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />

      {/* Live User Marker */}
      <Marker position={userLocation} icon={userIcon}>
        <Popup>
          <b>👤 Responder Location</b>
          <br />
          Live Laptop Location
          <br />
          <br />
          <b>Latitude:</b> {userLocation[0].toFixed(6)}
          <br />
          <b>Longitude:</b> {userLocation[1].toFixed(6)}
        </Popup>
      </Marker>

      {/* Fire Marker */}
      <Marker position={fireLocation} icon={fireIcon}>
        <Popup>
          <b>🔥 Fire Detected</b>
          <br />
          Camera 01
          <br />
          Confidence: 98%
          <br />
          Severity: HIGH
        </Popup>
      </Marker>

      {/* Route */}
      <Polyline
        positions={[userLocation, fireLocation]}
        pathOptions={{
          color: "blue",
          weight: 5,
        }}
      />
    </MapContainer>
  );
}