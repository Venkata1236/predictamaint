const SensorMetricCard = ({
    title,
    value,
    unit,
    status,
}) => {

    const getStatusColor = () => {

        if (status === "critical") {
            return "#ef4444"
        }

        if (status === "warning") {
            return "#f59e0b"
        }

        return "#22c55e"
    }

    return (

        <div
            style={{
                background: "#1e293b",
                borderRadius: "16px",
                padding: "20px",
                border: `2px solid ${getStatusColor()}`,
                minWidth: "220px",
            }}
        >

            <p
                style={{
                    fontSize: "14px",
                    opacity: 0.7,
                }}
            >
                {title}
            </p>

            <h2
                style={{
                    marginTop: "10px",
                    fontSize: "32px",
                }}
            >
                {value}
                {" "}
                <span
                    style={{
                        fontSize: "16px",
                    }}
                >
                    {unit}
                </span>
            </h2>

            <p
                style={{
                    marginTop: "12px",
                    color: getStatusColor(),
                    fontWeight: "bold",
                    textTransform:
                        "uppercase",
                }}
            >
                {status}
            </p>

        </div>
    )
}

export default SensorMetricCard