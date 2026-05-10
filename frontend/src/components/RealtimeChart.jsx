import {
    Line,
    LineChart,
    ResponsiveContainer,
    Tooltip,
    XAxis,
    YAxis,
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

            <h2
                style={{
                    marginBottom: "20px",
                }}
            >
                Live Torque Monitoring
            </h2>

            <ResponsiveContainer
                width="100%"
                height={300}
            >

                <LineChart data={data}>

                    <XAxis
                        dataKey="time"
                    />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey="torque"
                        stroke="#3b82f6"
                        strokeWidth={3}
                        dot={false}
                    />

                </LineChart>

            </ResponsiveContainer>

        </div>
    )
}

export default RealtimeChart