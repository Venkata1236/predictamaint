const DiagnosticReportModal = ({
    incident,
}) => {

    if (!incident) {
        return null
    }

    const generateInsight = () => {

        const features =
            incident
            .anomalous_features

        if (
            features.includes(
                "torque"
            )
        ) {

            return (
                "Abnormal torque " +
                "behavior may indicate " +
                "mechanical resistance " +
                "or spindle wear."
            )
        }

        if (
            features.includes(
                "tool_wear"
            )
        ) {

            return (
                "Tool wear exceeded " +
                "normal operational " +
                "thresholds."
            )
        }

        if (
            features.includes(
                "rotational_speed"
            )
        ) {

            return (
                "Unexpected RPM changes " +
                "detected during " +
                "machine operation."
            )
        }

        return (
            "AI system detected " +
            "abnormal sensor patterns."
        )
    }

    return (

        <div
            style={{
                background: "#1e293b",
                padding: "20px",
                borderRadius: "16px",
                marginTop: "20px",
            }}
        >

            <h2
                style={{
                    marginBottom: "20px",
                }}
            >
                AI Diagnostic Insights
            </h2>

            <p
                style={{
                    lineHeight: "1.8",
                    opacity: 0.9,
                }}
            >
                {generateInsight()}
            </p>

            <div
                style={{
                    marginTop: "20px",
                    padding: "16px",
                    background: "#0f172a",
                    borderRadius: "12px",
                }}
            >

                <p>
                    <strong>
                        Recommended Action:
                    </strong>
                </p>

                <p
                    style={{
                        marginTop: "10px",
                    }}
                >
                    Schedule preventive
                    inspection within
                    the next maintenance
                    cycle.
                </p>

            </div>

        </div>
    )
}

export default DiagnosticReportModal