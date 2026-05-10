const MachineStatusCard = ({
    machineId,
    alertTier,
    score,
}) => {

    const getColor = () => {

        if (alertTier === "CRITICAL") {
            return "#ef4444"
        }

        if (alertTier === "ANOMALY") {
            return "#f59e0b"
        }

        return "#22c55e"
    }

    return (
        <div
            style={{
                background: "#1e293b",
                padding: "20px",
                borderRadius: "16px",
                marginBottom: "20px",
                border: `2px solid ${getColor()}`
            }}
        >

            <h2>
                {machineId}
            </h2>

            <p
                style={{
                    color: getColor(),
                    fontWeight: "bold",
                    marginTop: "10px",
                }}
            >
                {alertTier}
            </p>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                Ensemble Score:
                {" "}
                {(
                    score * 100
                ).toFixed(2)}%
            </p>

        </div>
    )
}

export default MachineStatusCard