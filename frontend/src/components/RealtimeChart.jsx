import {
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
    Legend,
    CartesianGrid,
} from "recharts"

const RealtimeChart = ({
    data,
}) => {

    return (

        <div
            style={{
                background: "#1e293b",
                padding: "20px",
                borderRadius: "16px",
            }}
        >

            <div
                style={{
                    display: "flex",
                    justifyContent:
                        "space-between",

                    alignItems: "center",

                    marginBottom: "20px",
                }}
            >

                <div>

                    <h2>
                        Live Sensor Monitoring
                    </h2>

                    <p
                        style={{
                            opacity: 0.7,
                            marginTop: "6px",
                        }}
                    >
                        Real-time industrial
                        telemetry stream
                    </p>

                </div>

            </div>

            <ResponsiveContainer
                width="100%"
                height={380}
            >

                <LineChart data={data}>

                    <CartesianGrid
                        strokeDasharray="3 3"
                        stroke="#334155"
                    />

                    <XAxis
                        dataKey="time"
                        stroke="#94a3b8"
                    />

                    <YAxis
                        stroke="#94a3b8"
                    />

                    <Tooltip
                        contentStyle={{
                            background:
                                "#0f172a",

                            border:
                                "1px solid #334155",

                            borderRadius:
                                "12px",

                            color: "white",
                        }}
                    />

                    <Legend />

                    <Line
                        type="monotone"
                        dataKey="torque"
                        stroke="#3b82f6"
                        strokeWidth={3}
                        dot={false}
                        name="Torque"
                    />

                    <Line
                        type="monotone"
                        dataKey="air_temp"
                        stroke="#22c55e"
                        strokeWidth={2}
                        dot={false}
                        name="Air Temp"
                    />

                    <Line
                        type="monotone"
                        dataKey="process_temp"
                        stroke="#f59e0b"
                        strokeWidth={2}
                        dot={false}
                        name="Process Temp"
                    />

                    <Line
                        type="monotone"
                        dataKey="rotational_speed"
                        stroke="#ef4444"
                        strokeWidth={2}
                        dot={false}
                        name="RPM"
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>
    )
}

export default RealtimeChart