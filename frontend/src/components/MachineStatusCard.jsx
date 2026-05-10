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

    const isCritical =
        alertTier === "CRITICAL"

    return (

        <div
            style={{
                background: "#1e293b",

                padding: "24px",

                borderRadius: "18px",

                marginBottom: "20px",

                border:
                    `2px solid ${getColor()}`,

                animation:
                    isCritical
                    ? "pulseCritical 1.5s infinite"
                    : "none",

                transition:
                    "all 0.3s ease",
            }}
        >

            <div
                style={{
                    display: "flex",
                    justifyContent:
                        "space-between",

                    alignItems: "center",
                }}
            >

                <div>

                    <h2>
                        {machineId}
                    </h2>

                    <p
                        style={{
                            marginTop: "8px",
                            opacity: 0.7,
                        }}
                    >
                        Industrial CNC Unit
                    </p>

                </div>

                <div
                    style={{
                        background:
                            getColor(),

                        color: "white",

                        padding:
                            "10px 16px",

                        borderRadius:
                            "999px",

                        fontWeight:
                            "bold",
                    }}
                >
                    {alertTier}
                </div>

            </div>

            <div
                style={{
                    marginTop: "20px",
                }}
            >

                <p
                    style={{
                        opacity: 0.7,
                    }}
                >
                    Ensemble Risk Score
                </p>

                <h1
                    style={{
                        marginTop: "10px",
                        fontSize: "42px",
                    }}
                >
                    {
                        (
                            score * 100
                        ).toFixed(1)
                    }%
                </h1>

            </div>

        </div>
    )
}

export default MachineStatusCard