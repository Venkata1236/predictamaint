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

function App() {

    const {
        data,
        status,
    } = useWebSocket(
        WS_URL
    )

    const [chartData, setChartData] =
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

            {data && (

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
            )}

            <RealtimeChart
                data={chartData}
            />

        </div>
    )
}

export default App