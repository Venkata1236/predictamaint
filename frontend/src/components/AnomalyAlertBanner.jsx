const AnomalyAlertBanner = ({
    alertTier,
    anomalousFeatures,
}) => {

    if (alertTier === "NORMAL") {
        return null
    }

    const isCritical =
        alertTier === "CRITICAL"

    return (

        <div
            style={{
                background:
                    isCritical
                    ? "#7f1d1d"
                    : "#78350f",

                border:
                    isCritical
                    ? "2px solid #ef4444"
                    : "2px solid #f59e0b",

                padding: "24px",

                borderRadius: "18px",

                marginBottom: "20px",

                animation:
                    isCritical
                    ? "pulseCritical 1.5s infinite"
                    : "none",
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

                    <h2
                        style={{
                            fontSize: "28px",
                        }}
                    >
                        {
                            isCritical
                            ? "CRITICAL INCIDENT"
                            : "ANOMALY DETECTED"
                        }
                    </h2>

                    <p
                        style={{
                            marginTop: "10px",
                            opacity: 0.9,
                        }}
                    >
                        AI monitoring system
                        detected abnormal
                        industrial behavior.
                    </p>

                </div>

                <div
                    style={{
                        background:
                            isCritical
                            ? "#ef4444"
                            : "#f59e0b",

                        padding:
                            "12px 18px",

                        borderRadius:
                            "999px",

                        fontWeight:
                            "bold",

                        color: "white",
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

                <p>
                    <strong>
                        Affected Sensors:
                    </strong>
                </p>

                <div
                    style={{
                        display: "flex",
                        gap: "10px",
                        flexWrap: "wrap",
                        marginTop: "12px",
                    }}
                >

                    {
                        anomalousFeatures.map(
                            (feature) => (

                            <div
                                key={feature}

                                style={{
                                    background:
                                        "#0f172a",

                                    padding:
                                        "8px 14px",

                                    borderRadius:
                                        "999px",

                                    border:
                                        "1px solid #475569",
                                }}
                            >
                                {feature}
                            </div>
                        ))
                    }

                </div>

            </div>

        </div>
    )
}

export default AnomalyAlertBanner