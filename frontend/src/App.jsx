import {
    useEffect,
    useState,
} from "react"

import Sidebar from
"./components/Sidebar"

import MachineStatusCard from
"./components/MachineStatusCard"

import RealtimeChart from
"./components/RealtimeChart"

import useWebSocket from
"./hooks/useWebSocket"

import { WS_URL } from
"./services/api"

import SensorMetricCard from
"./components/SensorMetricCard"

import AnomalyAlertBanner from
"./components/AnomalyAlertBanner"

import IncidentLog from
"./components/IncidentLog"

import MaintenanceTicket from
"./components/MaintenanceTicket"

import DiagnosticReportModal from
"./components/DiagnosticReportModal"

import LoadingScreen from
"./components/LoadingScreen"

import LiveAlertToast from
"./components/LiveAlertToast"

function App() {

    const {
        data,
        status,
    } = useWebSocket(
        WS_URL
    )

    const [chartData, setChartData] =
        useState([])

    const [incidents, setIncidents] =
        useState([])

    const [
        toastIncident,
        setToastIncident,
    ] = useState(null)

    useEffect(() => {

        if (!data) return

        setChartData((prev) => {

            const updated = [
                ...prev,
                {
                    time:
                        new Date(
                            data.timestamp
                        ).toLocaleTimeString(),

                    torque:
                        data.readings
                        .torque,

                    air_temp:
                        data.readings
                        .air_temp,

                    process_temp:
                        data.readings
                        .process_temp,

                    rotational_speed:
                        data.readings
                        .rotational_speed,
                },
            ]

            return updated.slice(-20)
        })

        if (
            data.alert_tier !== "NORMAL"
        ) {

            setIncidents((prev) => [

                {
                    ...data,
                },

                ...prev,

            ].slice(0, 10))

            setToastIncident(data)

            setTimeout(() => {

                setToastIncident(null)

            }, 5000)
        }

    }, [data])

    if (
        status !== "connected"
    ) {

        return (
            <LoadingScreen />
        )
    }

    return (

        <div
            style={{
                display:
                    window.innerWidth < 1000
                    ? "block"
                    : "flex",

                background: "#0f172a",
            }}
        >

            <Sidebar />

            <div
                style={{
                    flex: 1,
                    padding: "30px",
                    minHeight: "100vh",
                    color: "white",
                }}
            >

                <div
                    style={{
                        display: "flex",
                        justifyContent:
                            "space-between",

                        alignItems: "center",

                        flexWrap: "wrap",

                        gap: "20px",

                        marginBottom: "20px",
                    }}
                >

                    <div>

                        <h1>
                            PredictaMaint
                        </h1>

                        <p
                            style={{
                                opacity: 0.7,
                                marginTop: "5px",
                            }}
                        >
                            Real-Time Industrial
                            Predictive Maintenance
                            Platform
                        </p>

                        <p
                            style={{
                                marginTop: "10px",
                                color: "#f59e0b",
                                fontWeight: "bold",
                            }}
                        >
                            Active Incidents:
                            {" "}
                            {incidents.length}
                        </p>

                    </div>

                    <div
                        style={{
                            background: "#1e293b",
                            padding: "12px 18px",
                            borderRadius: "12px",
                            display: "flex",
                            alignItems: "center",
                            gap: "8px",
                        }}
                    >

                        <div
                            style={{
                                width: "10px",
                                height: "10px",
                                borderRadius: "50%",

                                background:
                                    status ===
                                    "connected"
                                    ? "#22c55e"
                                    : "#ef4444",
                            }}
                        />

                        <span
                            style={{
                                color:
                                    status ===
                                    "connected"
                                    ? "#22c55e"
                                    : "#ef4444",

                                fontWeight: "bold",
                            }}
                        >
                            {status}
                        </span>

                    </div>

                </div>

                {
                    data && (

                        <AnomalyAlertBanner
                            alertTier={
                                data.alert_tier
                            }

                            anomalousFeatures={
                                data.anomalous_features
                            }
                        />
                    )
                }

                {
                    data && (

                        <MachineStatusCard
                            machineId={
                                data.machine_id
                            }

                            alertTier={
                                data.alert_tier
                            }

                            score={
                                data.ensemble_score
                            }
                        />
                    )
                }

                {
                    data && (

                        <div
                            style={{
                                display: "grid",

                                gridTemplateColumns:
                                    window.innerWidth < 900
                                    ? "1fr"
                                    : "repeat(auto-fit, minmax(220px, 1fr))",

                                gap: "20px",

                                marginBottom: "20px",
                            }}
                        >

                            <SensorMetricCard
                                title="Air Temperature"
                                value={
                                    data.readings
                                    .air_temp
                                }
                                unit="K"
                                status="normal"
                            />

                            <SensorMetricCard
                                title="Process Temperature"
                                value={
                                    data.readings
                                    .process_temp
                                }
                                unit="K"
                                status="normal"
                            />

                            <SensorMetricCard
                                title="Rotational Speed"
                                value={
                                    data.readings
                                    .rotational_speed
                                }
                                unit="RPM"
                                status="normal"
                            />

                            <SensorMetricCard
                                title="Torque"
                                value={
                                    data.readings
                                    .torque
                                }
                                unit="Nm"
                                status={
                                    data.alert_tier
                                    === "ANOMALY"
                                    ? "warning"
                                    : "normal"
                                }
                            />

                        </div>
                    )
                }

                {
                    chartData.length > 0 && (

                        <div
                            style={{
                                display: "grid",

                                gridTemplateColumns:
                                    window.innerWidth < 1200
                                    ? "1fr"
                                    : "2fr 1fr",

                                gap: "20px",

                                marginTop: "20px",
                            }}
                        >

                            <div>

                                <RealtimeChart
                                    data={chartData}
                                />

                            </div>

                            <div>

                                <MaintenanceTicket
                                    incident={
                                        incidents[0]
                                    }
                                />

                                <DiagnosticReportModal
                                    incident={
                                        incidents[0]
                                    }
                                />

                                <IncidentLog
                                    incidents={
                                        incidents
                                    }
                                />

                            </div>

                        </div>
                    )
                }

                <LiveAlertToast
                    incident={
                        toastIncident
                    }
                />

            </div>

        </div>
    )
}

export default App