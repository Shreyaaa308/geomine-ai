import React from 'react';
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const MapPanel = ({ scenario }) => {
  const center = [21.8, 80.2];

  const mapData = {
    normal: {
      zoneA: { color: '#10b981', label: 'Zone A - Active Mining', text: 'Operations normal. No safety risks.' },
      zoneB: { color: '#f59e0b', label: 'Zone B - Surveying', text: 'Routine checks ongoing.' }
    },
    rain: {
      zoneA: { color: '#ef4444', label: 'Zone A - FLOOD WARNING', text: 'Evacuate immediately! Water level rising rapidly.' },
      zoneB: { color: '#10b981', label: 'Zone B - Elevated (Safe)', text: 'Safe zone. Shift all machinery here.' }
    },
    machine: {
      zoneA: { color: '#10b981', label: 'Zone A - Active Mining', text: 'Operations normal.' },
      zoneB: { color: '#ef4444', label: 'Zone B - EXCAVATOR DOWN', text: 'Haul route blocked. Dispatch maintenance crew.' }
    }
  };

  const currentMap = mapData[scenario] || mapData.normal;

  return (
    <div className="w-full h-[500px] rounded-xl overflow-hidden shadow-2xl relative z-0 border border-slate-700 transition-all duration-500">
      <MapContainer center={center} zoom={9} style={{ height: '100%', width: '100%' }}>
        <TileLayer
          url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          attribution='&copy; OpenStreetMap'
          className="map-tiles"
        />
        
        <CircleMarker 
          center={[21.85, 80.15]} 
          pathOptions={{ fillColor: currentMap.zoneA.color, color: currentMap.zoneA.color, fillOpacity: 0.6 }} 
          radius={45}
        >
          <Popup>
            <div className="font-sans text-slate-800">
              <strong style={{ color: currentMap.zoneA.color }} className="text-lg">{currentMap.zoneA.label}</strong><br/>
              {currentMap.zoneA.text}
            </div>
          </Popup>
        </CircleMarker>

         <CircleMarker 
          center={[21.65, 80.35]} 
          pathOptions={{ fillColor: currentMap.zoneB.color, color: currentMap.zoneB.color, fillOpacity: 0.6 }} 
          radius={30}
        >
          <Popup>
            <div className="font-sans text-slate-800">
              <strong style={{ color: currentMap.zoneB.color }} className="text-lg">{currentMap.zoneB.label}</strong><br/>
              {currentMap.zoneB.text}
            </div>
          </Popup>
        </CircleMarker>
      </MapContainer>
    </div>
  );
};

export default MapPanel;