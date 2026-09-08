"use client";
import { useState, useEffect, useRef } from "react";
import { AnimatePresence } from "framer-motion";
import { Activity, BellRing, Wifi, WifiOff, LogOut, Loader2 } from "lucide-react";
import { Incident, IncidentCard } from "./IncidentCard";
import { fetchApi, clearAuthToken } from "@/lib/api";

const WS_URL = "ws://127.0.0.1:8000/api/v1/ws/events";

export default function Dashboard({ onLogoutAction }: { onLogoutAction: () => void }) {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [serviceNames, setServiceNames] = useState<Record<number, string>>({});
  const [connected, setConnected] = useState(false);
  const [loading, setLoading] = useState(true);
  
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  // Initial Data Fetch
  useEffect(() => {
    async function fetchInitialData() {
      try {
        setLoading(true);
        // 1. Fetch Services
        const services = await fetchApi("/services");
        const serviceMap: Record<number, string> = {};
        services.forEach((s: any) => {
          serviceMap[s.id] = s.name;
        });
        setServiceNames(serviceMap);

        // 2. Fetch Existing Open Incidents
        const existingIncidents = await fetchApi("/incidents");
        // Sort by ID descending (newest first) assuming ID correlates with time
        const sorted = existingIncidents.sort((a: any, b: any) => b.id - a.id);
        
        // Map to our frontend format
        const formatted = sorted.map((inc: any) => ({
          incident_id: inc.id,
          service_id: inc.service_id,
          severity: inc.severity,
          status: inc.status,
          timestamp: inc.started_at,
          service_name: serviceMap[inc.service_id] || `Service #${inc.service_id}`,
          description: inc.title || inc.description,
        }));
        
        setIncidents(formatted);
      } catch (err) {
        console.error("Failed to load initial data:", err);
      } finally {
        setLoading(false);
      }
    }

    fetchInitialData();
  }, []);

  // WebSocket Connection
  useEffect(() => {
    let isMounted = true;

    const connect = () => {
      // Prevent creating multiple connections if one is already opening or open
      if (
        wsRef.current?.readyState === WebSocket.OPEN ||
        wsRef.current?.readyState === WebSocket.CONNECTING
      ) {
        return;
      }

      console.log("Connecting to WebSocket:", WS_URL);
      const socket = new WebSocket(WS_URL);
      wsRef.current = socket;

      socket.onopen = () => {
        if (!isMounted) {
          socket.close();
          return;
        }
        console.log("Connected to Realtime Events");
        setConnected(true);
        if (reconnectTimeoutRef.current) {
          clearTimeout(reconnectTimeoutRef.current);
        }
      };

      socket.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          console.log("Realtime event received:", data);

          if (data.type === "INCIDENT_CREATED" && data.payload) {
            setServiceNames((currentServiceNames) => {
              const newIncident: Incident = {
                ...data.payload,
                timestamp: new Date().toISOString(),
                service_name: currentServiceNames[data.payload.service_id] || `Service #${data.payload.service_id}`,
              };
              
              setIncidents((prev) => {
                if (prev.some(i => i.incident_id === newIncident.incident_id)) return prev;
                return [newIncident, ...prev].slice(0, 50);
              });
              
              return currentServiceNames;
            });
          }
        } catch (err) {
          console.error("Failed to parse websocket message:", err);
        }
      };

      socket.onclose = () => {
        console.log("Disconnected from Realtime Events");
        if (isMounted) {
          setConnected(false);
          // Auto reconnect after 5 seconds
          reconnectTimeoutRef.current = setTimeout(() => {
            connect();
          }, 5000);
        }
      };

      socket.onerror = (error) => {
        console.error("WebSocket error:", error);
        // The socket will be closed automatically or we can close it, which triggers onclose
      };
    };

    connect();

    return () => {
      isMounted = false;
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const handleLogout = () => {
    clearAuthToken();
    onLogoutAction();
  };

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="flex flex-col items-center text-indigo-400 gap-4">
          <Loader2 className="w-10 h-10 animate-spin" />
          <p className="text-gray-400 font-medium tracking-wide">Loading AI Platform...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full max-w-4xl mx-auto p-6 space-y-8 mt-10">
      <div className="flex items-center justify-between border-b border-gray-800 pb-6">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-gradient-to-br from-indigo-500/20 to-purple-500/20 rounded-xl border border-indigo-500/20 shadow-[0_0_15px_rgba(99,102,241,0.2)]">
            <Activity className="w-8 h-8 text-indigo-400" />
          </div>
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white flex items-center gap-3">
              Live Incidents
            </h1>
            <p className="text-gray-400 mt-1">Real-time alerts from Alert Engine</p>
          </div>
        </div>
        <div className="flex items-center gap-4">
          <div className="flex items-center gap-2 bg-black/40 px-4 py-2 rounded-full border border-gray-800">
            {connected ? (
              <>
                <Wifi className="w-4 h-4 text-emerald-400" />
                <span className="text-emerald-400 text-sm font-medium">Connected</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-red-400" />
                <span className="text-red-400 text-sm font-medium">Disconnected</span>
              </>
            )}
          </div>
          <button 
            onClick={handleLogout}
            className="p-2.5 rounded-full bg-gray-800/50 hover:bg-gray-700/80 border border-gray-700 text-gray-300 transition-colors"
            title="Log out"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      </div>

      <div className="min-h-[400px] flex flex-col gap-4">
        <AnimatePresence mode="popLayout">
          {incidents.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-64 text-gray-500 glass-card rounded-xl border-dashed">
              <BellRing className="w-12 h-12 mb-4 opacity-50" />
              <p className="text-lg font-medium">No active incidents</p>
              <p className="text-sm mt-2">Waiting for new events...</p>
            </div>
          ) : (
            incidents.map((inc, i) => (
              <IncidentCard key={`${inc.incident_id}-${i}`} incident={inc} />
            ))
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}
