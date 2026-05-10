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

                padding: "20px",

                borderRadius: "16px",

                marginBottom: "20px",

                animation:
                    isCritical
                    ? "pulse 1s infinite"
                    : "none",
            }}
        >

            <h2>
                {isCritical
                    ? "CRITICAL MACHINE ALERT"
                    : "ANOMALY DETECTED"}
            </h2>

            <p
                style={{
                    marginTop: "10px",
                }}
            >
                Detected abnormal
                sensor behavior in:
            </p>

            <ul
                style={{
                    marginTop: "10px",
                    paddingLeft: "20px",
                }}
            >

                {anomalousFeatures.map(
                    (feature) => (

                    <li key={feature}>
                        {feature}
                    </li>
                ))}

            </ul>

        </div>
    )
}

export default AnomalyAlertBanner