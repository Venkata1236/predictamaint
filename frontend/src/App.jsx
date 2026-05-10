import {
    useEffect,
    useState,
} from "react"

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
        }

    }, [data])

    return (

        <div
            style={{
                padding: "30px",
                minHeight: "100vh",
                background: "#0f172a",
            }}
        >

            <h1
                style={{
                    marginBottom: "20px",
                }}
            >
                PredictaMaint
            </h1>

            <p
                style={{
                    marginBottom: "20px",
                }}
            >
                WebSocket Status:
                {" "}
                {status}
            </p>

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
                            display: "flex",
                            gap: "20px",
                            marginBottom: "20px",
                            flexWrap: "wrap",
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

            <RealtimeChart
                data={chartData}
            />

            <IncidentLog
                incidents={incidents}
            />

        </div>
    )
}

export default App