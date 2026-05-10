const IncidentLog = ({
    incidents,
}) => {

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
                Incident Timeline
            </h2>

            {
                incidents.length === 0
                ? (
                    <p>
                        No incidents detected
                    </p>
                )
                : (
                    incidents.map(
                        (
                            incident,
                            index
                        ) => (

                        <div
                            key={index}

                            style={{
                                borderBottom:
                                    "1px solid #334155",

                                padding:
                                    "12px 0",
                            }}
                        >

                            <p>
                                <strong>
                                    {
                                        incident.alert_tier
                                    }
                                </strong>
                            </p>

                            <p>
                                Score:
                                {" "}
                                {
                                    incident
                                    .ensemble_score
                                    .toFixed(2)
                                }
                            </p>

                            <p>
                                Features:
                                {" "}
                                {
                                    incident
                                    .anomalous_features
                                    .join(", ")
                                }
                            </p>

                            <p
                                style={{
                                    opacity: 0.7,
                                    fontSize: "14px",
                                }}
                            >
                                {
                                    new Date(
                                        incident.timestamp
                                    ).toLocaleString()
                                }
                            </p>

                        </div>
                    ))
                )
            }

        </div>
    )
}

export default IncidentLog