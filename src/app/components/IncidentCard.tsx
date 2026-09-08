import { motion } from "framer-motion";
import { AlertTriangle, AlertCircle, Info, Flame, Activity } from "lucide-react";
import { cn } from "@/lib/utils";

export type Severity = "CRITICAL" | "HIGH" | "MEDIUM" | "LOW" | "INFO";
export type Status = "OPEN" | "ACKNOWLEDGED" | "RESOLVED";

export interface Incident {
  incident_id: number;
  service_id: number;
  severity: Severity;
  status: Status;
  timestamp?: string; 
  service_name?: string; 
  description?: string; 
}

const severityConfig = {
  CRITICAL: {
    icon: Flame,
    color: "text-red-500",
    bg: "bg-red-500/10",
    glow: "glow-red",
    border: "border-red-500/50",
  },
  HIGH: {
    icon: AlertTriangle,
    color: "text-orange-500",
    bg: "bg-orange-500/10",
    glow: "glow-orange",
    border: "border-orange-500/50",
  },
  MEDIUM: {
    icon: AlertCircle,
    color: "text-yellow-500",
    bg: "bg-yellow-500/10",
    glow: "glow-yellow",
    border: "border-yellow-500/50",
  },
  LOW: {
    icon: Info,
    color: "text-blue-500",
    bg: "bg-blue-500/10",
    glow: "glow-blue",
    border: "border-blue-500/50",
  },
  INFO: {
    icon: Activity,
    color: "text-gray-400",
    bg: "bg-gray-500/10",
    glow: "",
    border: "border-gray-500/30",
  },
};

export function IncidentCard({ incident }: { incident: Incident }) {
  const config = severityConfig[incident.severity] || severityConfig.INFO;
  const Icon = config.icon;

  const timeString = incident.timestamp 
    ? new Date(incident.timestamp).toLocaleTimeString() 
    : "Just now";

  return (
    <motion.div
      initial={{ opacity: 0, y: -20, scale: 0.95 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      exit={{ opacity: 0, scale: 0.95 }}
      transition={{ duration: 0.4, type: "spring", bounce: 0.4 }}
      className={cn(
        "glass-card p-5 rounded-xl flex flex-col gap-3 relative overflow-hidden group",
        config.glow
      )}
    >
      <div className={cn("absolute top-0 left-0 w-1 h-full", config.bg, config.border, "border-l-4")} />
      
      <div className="flex justify-between items-start">
        <div className="flex items-center gap-2">
          <div className={cn("p-2 rounded-lg", config.bg)}>
            <Icon className={cn("w-5 h-5", config.color)} />
          </div>
          <div>
            <h3 className={cn("font-bold tracking-tight text-sm", config.color)}>
              {incident.severity} INCIDENT
            </h3>
            <p className="text-gray-200 font-medium text-lg mt-0.5">
              {incident.service_name || `Service #${incident.service_id}`}
            </p>
          </div>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-xs text-gray-400 font-mono bg-black/40 px-2 py-1 rounded-md border border-gray-800">
            ID: {incident.incident_id}
          </span>
          <span className="text-xs text-gray-500 mt-2">
            {timeString}
          </span>
        </div>
      </div>
      
      <div className="mt-1 pl-[3.25rem]">
        <p className="text-gray-300 text-sm leading-relaxed">
          {incident.description || "CPU usage exceeded threshold or anomalous behavior detected."}
        </p>
      </div>
      
      <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent -translate-x-[100%] group-hover:animate-[shimmer_2s_infinite] pointer-events-none" />
    </motion.div>
  );
}
